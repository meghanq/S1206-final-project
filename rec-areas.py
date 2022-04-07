import json
import sqlite3
import unittest
import os
import requests

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    # conn = connection to database
    conn = sqlite3.connect(path+'/'+db_name)
    # cur = what you use to execute commands
    cur = conn.cursor()
    return cur, conn 

def createCityIdTable(cur,conn):
    #rewrite city list based on meghan's data
    cities = ["Chicago", "San Fransisco"]
    cur.execute("DROP TABLE IF EXISTS Cities")
    cur.execute("CREATE TABLE Cities (id INTEGER PRIMARY KEY, name TEXT)")
    for i in range(len(cities)):
        cur.execute("INSERT INTO Cities (id,name) VALUES (?,?)",(i,cities[i]))
    conn.commit()
    pass

# rec areas name, city id -> city table
# city name (long/lat from laurens)  and number of rec areas
def get_rec_data(longitude, latitude, radius, limit=25):
    url = f'https://ridb.recreation.gov/api/v1/recareas?limit={limit}&latitude={latitude}longitude={longitude}&radius={radius}'

    try: 
        resp = requests.get(url, headers = {'apikey':'4e51cb7e-cbb7-4cad-bffb-9e5ddc264234'})
        data = json.loads(resp.text)
       # print(data)
    except: 
        print('Exception')
        return None
    return data
    
    
def get_rec_names_in_radius(data):
    names = []
    for dict in data['RECDATA']:
        names.append(dict['RecAreaName'])
    return names

# can change to SQL select city by city_id (join)
def get_count_in_area(names):
    return len(names)

#table: rec area name, city ID
#count table: city, count of areas

def main():
    cur, conn = setUpDatabase('database.db')
    createCityIdTable(cur, conn)
    #replace lat long w data from table
    data = get_rec_data(114.39, -84.89, 50.0, limit=25)
    names = get_rec_names_in_radius(data)
    count = get_count_in_area(names)

    
if __name__ == "__main__":
    main()
