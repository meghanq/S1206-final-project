import json
import unittest
import os
import requests

#base_url = 'https://api.teleport.org/api/'

    
def get_city_data(city, dictionary):
    url = f'https://api.teleport.org/api/urban_areas/slug:{city}/scores/'

    try: 
        resp = requests.get(url)
        data = json.loads(resp.text)
        dictionary[city] = data['categories']
        #print(dictionary)

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
    city_list = ['san-francisco-bay-area', 'chicago', 'new-york', 'colorado-springs', 'boulder', 'las-vegas', 'kansas-city', 'seattle', 'miami']
    for city in city_list: 
        get_city_data(city, city_dictionary)

    print(city_dictionary)


    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + 'quality_of_life_city_data.json'
    #write_cache(CACHE_FNAME, city_dictionary)




main()