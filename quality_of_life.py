import json
import unittest
import os
import requests

#base_url = 'https://api.teleport.org/api/'

    
def get_city_data(city, dictionary, city_name_dict):
    url = f'https://api.teleport.org/api/urban_areas/slug:{city}/scores/'

    try: 
        resp = requests.get(url)
        data = json.loads(resp.text)
        dictionary[city] = data['categories']

    except: 
        print('Exception')
        return None


    
def read_cache(CACHE_FNAME):
    try: 
        file = open(CACHE_FNAME, 'r')
        data = file.read()
        file.close()
        info = json.loads(data)
    except: 
        info = {}

    return info

def write_cache(CACHE_FNAME, CACHE_DICT):
    json_data = json.dumps(CACHE_DICT)
    with open(CACHE_FNAME, 'w') as file:
        file.write(json_data)
        


def get_cache_data(city, CACHE_FNAME):
    cache_data = read_cache(CACHE_FNAME)

    if city in cache_data:
        print('Using cache for '+city)
        return cache_data[city]

    #print('Fetching data for '+city)


def get_city_avg(city):
    pass



    

class Tests(unittest.TestCase):
    def setUp(self):
        pass
     


def main():

    city_dictionary = {}
    city_name_dict = {'Albuquerque':'albuquerque', 'Anchorage':'anchorage', 'Asheville':'asheville', 'Atlanta':'atlanta', 'Austin': 'austin', 'Baltimore':'baltimore', 'Boise':'boise', 'Boston':'boston', 'Boulder':'boulder', 'Buffalo':'buffalo', 'Calgary':'calgary', 'Charleston':'charleston', 
    'Charlotte':'charlotte', 'Chicago':'chicago', 'Cincinnati':'cincinnati', 'Cleveland':'cleveland', 'Colorado Springs': 'colorado-springs', 'Columbus': 'columbus', 'Dallas': 'dallas', 'Denver': 'denver', 'Des Moines': 'des moines', 'Detroit':'detroit', 'Honolulu': 'honolulu', 'Houston': 'houston', 
    'Indianapolis': 'indianapolis', 'Jacksonville': 'jacksonville', 'Kansas City': 'kansas-city', 'Knoxville':'knoxville', 'Las Vagas': 'las-vegas', 'Los Angeles': 'los-angeles', 'Louisville':'louisville', 'Madison':'madison', 'Memphis':'memphis', 'Miama':'miami', 'Milwaukee':'milwaukee', 
    'Minneapolis Saint-Paul': 'minneapolis-saint-paul', 'Nashville': 'nashville', 'New Orleans': 'new-orleans', 'New York':'new-york', 'Oklahoma City':'oklahoma-city', 'Omaha':'omaha', 'Orlando':'orlando', 'Palo Alto': 'palo-alto', 'Philadelphia':'philadelphia', 'Pheonix':'pheonix', 
    'Pittsburgh':'pittsburgh', 'Portland, ME': 'portland-me', 'Portland, OR': 'portland-or', 'Providence':'providence', 'Raleigh':'raleigh', 'Richmond':'richmond', 'Rochester': 'rochester', 'Salt Lake City': 'salt-lake-city', 'San Antonio':'san-antonio', 'San Diego':'san-diego', 
    'San Francisco Bay Area':'san-francisco-bay-area', 'Seattle': 'seattle', 'St. Louis': 'st-louis', 'Tampa Bay Area':'tampa-bay-area', 'Washington D.C.': 'washington-dc'}
    #get_city_data('minneapolis-saint-paul', city_dictionary)

    print(len(city_name_dict))
    for city in city_name_dict: 
        get_city_data(city_name_dict[city], city_dictionary)

    print(city_dictionary)


    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # CACHE_FNAME = dir_path + 'quality_of_life_city_data.json'
    # write_cache(CACHE_FNAME, city_dictionary)




main()