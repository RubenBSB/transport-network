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
df_entries= df_entries[df_entries['station'] != 'FUNICULAIRE']              # Useless station

df_positions = json_normalize(r_positions.json())[['nomptar', 'coord.lon', 'coord.lat']]
df_positions.columns = ['station', 'longitude', 'latitude']
df_positions.drop_duplicates('station', inplace = True)
df_positions.replace('L1se Michel', 'Louise Michel', inplace = True)        # Error in RATP database
df_positions.replace('L1s Blanc', 'Louis Blanc', inplace = True)        # Error in RATP database
df_positions.replace('Villejuif-L1s Aragon', 'Villejuif-Louis Aragon', inplace = True)        # Error in RATP database

df_positions = df_positions[df_positions['station'] != 'Saint-Maur Créteil']
df_positions = df_positions[df_positions['station'] != 'Le Parc de Saint-Maur']

def find_most_similar(str,df):
    """Function that checks for the station names from the DataFrame 'df' and returns the most similar to 'str'.
    Stations from the entries and positions datasets were not uniformly named by RATP, this function handles this problem.
    It returns nothing if there is no possible match between both DataFrames. """
    expr = re.split(' |-', str)
    max_similarity = 0
    most_similar_station = ''
    max_index = 0
    for index, row in df.iterrows():
        regularized_name = unidecode.unidecode(row['station'].lower())
        regularized_name = re.sub(' \(.*\)', '', regularized_name)
        station_similarity = 0
        for word in expr:
            if re.match('(^|.* |.*-)(' + word.lower() + ').*', regularized_name):
                station_similarity += 5
        if len(expr) != len(re.split(' |-', regularized_name)):
            station_similarity -= 1
        if station_similarity > max_similarity:
            max_similarity = station_similarity
            most_similar_station = regularized_name
            max_index = index
    return most_similar_station, max_index

for index, row in df_entries.iterrows():
    station_in_df_positions, index_in_df_positions = find_most_similar(row['station'], df_positions)
    df_positions.ix[index_in_df_positions, 'station'] = station_in_df_positions.upper()
    df_entries.ix[index, 'station'] = station_in_df_positions.upper()

df_stations = pd.merge(df_positions,df_entries).drop('reseau', axis=1).sort_values('station')
df_stations.reset_index(drop=True, inplace=True)                            # Final DataFrame