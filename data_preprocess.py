import requests
import re
import unidecode
import pandas as pd
from pandas.io.json.normalize import json_normalize

pd.set_option('display.max_row',400,'display.max_columns', 10)

URL_ENTRIES = 'https://data.ratp.fr/api/v2/catalog/datasets/trafic-annuel-entrant-par-station-du-reseau-ferre-2015/exports/json?rows=-1&pretty=false&timezone=UTC'
URL_POSITIONS = 'https://data.ratp.fr/api/v2/catalog/datasets/accessibilite-des-gares-et-stations-metro-et-rer-ratp/exports/json?rows=-1&pretty=false&timezone=UTC'

r_entries = requests.get(URL_ENTRIES)
r_positions = requests.get(URL_POSITIONS)

df_entries = json_normalize(r_entries.json())[['station', 'trafic', 'reseau']]
df_entries = df_entries[df_entries['reseau']=='Métro']
df_entries.sort_values('station', inplace = True)

df_positions = json_normalize(r_positions.json())[['nomptar', 'coord.lon', 'coord.lat']]
df_positions.columns = ['station', 'longitude', 'latitude']

def findMostSimilar(str,df):
    """Function that check for the station names from the DataFrame 'df' and returns the most similar to 'str'.
    Stations from the entries and positions datasets were not uniformly named by RATP, this function handles this problem. """
    expr = re.split(' |-',str)
    max_similarity = 0
    most_similar_station = ''
    max_index = 0
    for index, row in df.iterrows():
        regularized_name = unidecode.unidecode(row['station'].lower()).replace('(','').replace(')','')
        station_similarity = 0
        for word in expr:
            if re.match('.*('+word.lower()+').*',regularized_name):
                station_similarity += 5
        if len(expr)!=len(regularized_name.split(' ')):
            station_similarity -= 1
        if station_similarity > max_similarity:
            max_similarity = station_similarity
            most_similar_station = regularized_name
            max_index = index
    return most_similar_station, max_similarity, max_index

for index,row in df_entries.iterrows():
    station, similarity, index_in_df_positions = findMostSimilar(row['station'], df_positions)
    df_positions.ix[index_in_df_positions,'station2'] = row['station']
    df_entries.ix[index,'station2'] = station
    df_entries.ix[index,'similarity'] = similarity

df_positions.dropna(inplace = True)
