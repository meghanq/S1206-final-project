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

def database_creation(db_filename, website_url):
    full_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()

    #cur.execute("DROP TABLE IF EXISTS cityInformation")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cityInformation (city TEXT, latitude FLOAT, longitude FLOAT)
    """)

    resp = requests.get(website_url)

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
        INSERT INTO cityInformation (city, latitude, longitude)
        VALUES (?,?,?)
        """, (city_name[:-9], lat, long)) 
        conn.commit()

database_creation('database.db', 'https://www.latlong.net/category/cities-236-15.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-2.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-3.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-3.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-4.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-5.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-6.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-7.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-9.html')
database_creation('database.db', 'https://www.latlong.net/category/cities-236-15-10.html')



