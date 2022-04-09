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

def get_cities(cur,conn):
    cur.execute('SELECT name FROM CityQoL')
    res = cur.fetchall()
    city_list = []
    for tup in res:
        city_list.append(tup[0])
    return city_list

def get_lat(cur,conn,name):
    cur.execute('SELECT latitude FROM cityInformation WHERE city = ?', (name,))
    conn.commit()
    try:
        return cur.fetchone()[0]
    except:
        return "Invalid city name"
def get_long(cur,conn,name):
    cur.execute('SELECT longitude FROM cityInformation WHERE city = ?', (name,))
    conn.commit()
    try:
        return cur.fetchone()[0]
    except:
        return "Invalid city name"

# rec areas name, city id -> city table
# city name (long/lat from laurens)  and number of rec areas
def get_rec_data(longitude, latitude, radius=50.0, limit=25):
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

def create_rec_table(cur,conn,cities):
    cur.execute('CREATE TABLE IF NOT EXISTS recAreas (name TEXT, city_id INT)')
    count = []
    for city in cities:
        longitude = get_long(cur,conn,city)
        latitude = get_lat(cur,conn,city)
        data = get_rec_data(longitude, latitude)
        names = get_rec_names_in_radius(data)
        count.append((city, len(names)))
        for name in names:
            cur.execute('SELECT city_id FROM CityQol WHERE name=?', (city,))
            city_id = cur.fetchone()[0]
            cur.execute('INSERT INTO recAreas (name,city_id) VALUES (?,?)', (name, city_id))
            conn.commit()
    return count


# can change to SQL select city by city_id (join)
def create_count_table(cur,conn, count):
    cur.execute('CREATE TABLE IF NOT EXISTS countNearCity (name TEXT, number INT)')
    for tup in count:
        cur.execute('INSERT INTO countNearCity (name,number) VALUES(?,?)', (tup[0],tup[1]))
    conn.commit()
    pass


#table: rec area name, city ID
#count table: city, count of areas

def main():
    cur, conn = setUpDatabase('database.db')
    cities = get_cities(cur,conn)
    count = create_rec_table(cur,conn,cities)
    create_count_table(cur,conn, count)

    
if __name__ == "__main__":
    main()
