from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os

#be sure to follow city, state
def find_lat_long(city):
    resp = requests.get('https://www.latlong.net/category/cities-236-15.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    tr_tags = soup.find_all('tr')
    #print(tr_tags)
    for c in tr_tags[1:]:
        city_name = c.find('a').text

        #print(city_name)
        if city_name[:-9] == city:
            lat_long = c.find_all('td')
            lat = lat_long[1].text
            long = lat_long[2].text
            print((float(lat),float(long)))
find_lat_long('Herrin')

def database_creation(db_filename):
    full_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS cityInfo")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cityInfo (city TEXT, latitude FLOAT, longitude FLOAT)
    """)

    resp = requests.get('https://www.latlong.net/category/cities-236-15.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    tr_tags = soup.find_all('tr')
    #print(tr_tags)
    for c in tr_tags[1:]:
        city_name = c.find('a').text

        lat_long = c.find_all('td')
        lat = lat_long[1].text
        long = lat_long[2].text
        print((float(lat),float(long)))

        cur.execute("""
        INSERT INTO cityInfo (city, latitude, longitude)
        VALUES (?,?,?)
        """, (city_name[:-9], lat, long)) 
        conn.commit()
    
database_creation('database.db')

