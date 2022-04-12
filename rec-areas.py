import json
import sqlite3
import unittest
import os
import requests
import csv

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

def get_rec_data(longitude, latitude, radius=50.0, limit=25):
    offset = 0
    names = []
    url = f'https://ridb.recreation.gov/api/v1/recareas?limit={limit}&offset={offset}&latitude={latitude}&longitude={longitude}&radius={radius}'

    try: 
        if longitude != "Invalid city name" and latitude != "Invalid city name":
            resp = requests.get(url, headers = {'apikey':'4e51cb7e-cbb7-4cad-bffb-9e5ddc264234'})
            data = json.loads(resp.text)
            count = data["METADATA"]["RESULTS"]["TOTAL_COUNT"]
            for dict in data['RECDATA']:
                names.append(dict['RecAreaName'])

            offset = 25
            while len(names) > offset:
                url = f'https://ridb.recreation.gov/api/v1/recareas?limit={limit}offset={offset}&latitude={latitude}longitude={longitude}&radius={radius}'
                resp = requests.get(url, headers = {'apikey':'4e51cb7e-cbb7-4cad-bffb-9e5ddc264234'})
                data = json.loads(resp.text)
                for dict in data['RECDATA']:
                    names.append(dict['RecAreaName'])
                offset += 25
            return names
        else:
            print("Invalid city")
            return None
    except: 
        print('Exception')
        return None
    
def createRecIdTable(cur,conn,cities):
    cur.execute("CREATE TABLE IF NOT EXISTS RecIds (id INTEGER PRIMARY KEY, name TEXT)")
    recs = []
    for city in cities:
        longitude = get_long(cur,conn,city)
        latitude = get_lat(cur,conn,city)
        names = get_rec_data(longitude, latitude)
        try:
            for name in names:
                recs.append(name)
        except:
            continue
    try:
        for i in range(1, len(recs)):
            cur.execute("INSERT OR IGNORE INTO RecIds (id,name) VALUES (?,?)",(i,recs[i-1]))
            conn.commit()
    except:
        pass

def create_rec_table(cur,conn,cities):
    cur.execute('CREATE TABLE IF NOT EXISTS recAreas (rec_id INT, city_id INT)')
    count = []
    for city in cities:
        longitude = get_long(cur,conn,city)
        latitude = get_lat(cur,conn,city)
        names = get_rec_data(longitude, latitude)
        try:
            for name in names:
                cur.execute('SELECT city_id FROM CityQoL WHERE name = ?', (city,))
                city_id = cur.fetchall()[0][0]
                cur.execute('SELECT id FROM RecIds WHERE name = ?', (name,))
                rec_id = cur.fetchall()[0][0]
                cur.execute('INSERT OR IGNORE INTO recAreas (rec_id, city_id) VALUES (?,?)', (rec_id, city_id))
                conn.commit()
        except:
            continue
    return None

def create_count_table(cur,conn,cities):
    header = ['City', 'Recreation Count', 'Average Quality of Life']
    with open('rec_count.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for city in cities:
            longitude = get_long(cur,conn,city)
            latitude = get_lat(cur,conn,city)
            names = get_rec_data(longitude, latitude)
            try:
                count = len(names)
                cur.execute('SELECT name FROM CityQol WHERE name = ?', (city,))
                city = cur.fetchall()[0][0]
                data = [city, count]
                writer.writerow(data)
            except:
                pass
    return None



#table: rec area name, city ID
#count table: city, count of areas

def main():
    cur, conn = setUpDatabase('database.db')
    cities = get_cities(cur,conn)
    createRecIdTable(cur,conn,cities)
    create_rec_table(cur,conn,cities)
    create_count_table(cur,conn,cities)
    print('Done')

    
if __name__ == "__main__":
    main()
