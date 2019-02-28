# transport-network 
## Motivations
This is a school project carried out in 2017.	

The goal is to understand how does public transportation networks are thought to be efficients in terms of travel time and building cost.


## Problem modelisation

We want to answer the following problem :

Given the geographical localisations of several subway stations, we would like to know how to find a "good" graph to connect them.

Here, "good" means that the average travel time and the building cost of the network should be reasonably lows.

In order to understand each of the following notations, please look at the formal definition of the problem from the [report document](https://rubenbsb.github.io/pdfs/transport-network.pdf). 

However, here is an overview to help you get a quick mathematical understanding of the problem :

![def](https://latex.codecogs.com/svg.latex?%5Ctext%7BFor%20a%20graph%20%7DG%3D%28S%2CE%29%5Ctext%7B%20we%20define%20its%20average%20travel%20time%20%7DT%28G%29%5Ctext%7B%20and%20its%20building%20cost%20%7DC%28G%29%5Ctext%7B%20as%20follows%20%3A%7D)

>![travel-time](https://latex.codecogs.com/svg.latex?T%28G%29%20%3D%20%5Csum_%7B%28i%2Cj%29%5Cin%20S%5E2%7D%5Cfrac%7B%5Cdelta_%7Bij%7D%7D%7BV%7D%5Cfrac%7Bf_if_j%7D%7BF%5E2%7D)

>![cost](https://latex.codecogs.com/svg.latex?C%28G%29%3D%5Csum_%7B%28i%2Cj%29%5Cin%20E%7Dl_%7Bij%7D%5Calpha)

Then the problem sum up to : 

>![min](https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%20%26%20%5Chspace%7B2.3cm%7D%5Cunderset%7BG%3D%28S%2CE%29%7D%7B%5Ctext%7Bmin%7D%7D%20%26%20%26%20T%28G%29%20%5C%5C%20%26%20%5Chspace%7B1.8cm%7D%5Ctext%7Bsubject%20to%7D%20%26%20%26%20C%28G%29%20%5Cle%20R%20%5C%5C%20%26%20%26%20%26%20G%20%5Ctext%7B%20connected%7D%5C%5C%20%26%20%26%20%26%20S%20%3D%20S_%7B0%7D%20%5Cend%7Baligned%7D)

![](https://latex.codecogs.com/svg.latex?%5Ctext%7Bwhere%20%7DS_%7B0%7D%5Ctext%7B%20denotes%20our%20fixed%20set%20of%20stations.%7D)
## Data

We use data from [Open Data RATP](https://data.ratp.fr/explore/?sort=modified) to get, for each station of the Parisian subway, its localisation and its frequentation over one year.

After preprocessing the raw data, we get a dataframe of 302 stations that looks like this :


|    Station name   |    Longitude    |     Latitude    | Entries over one year |
|:-----------------:|:---------------:|:---------------:|:---------------------:|
|     'Abbesses'    | 2.3387128116588 | 48.884417645184 |        2417881        |
|      'Alésia'     | 2.3267456737192 | 48.828398514348 |        5124204        |   
| 'Alexandre Dumas' | 2.3949898158233 | 48.856174448968 |        3780611        |

## Strategy

Minimizing both the building cost and the average travel time of a transport network is an impossible problem because these two objectives are contradictory.

Here, we try a first strategy which is to start from the optimal solution for the cost : a minimal spanning tree. 
