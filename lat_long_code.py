from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os

#be sure to follow city, state
def find_lat_long(city):
    resp = requests.get('https://batchgeo.com/map/latitude-longitude')
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

    cur.execute("DROP TABLE IF EXISTS cityInformation")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cityInformation (city TEXT, latitude FLOAT, longitude FLOAT)
    """)

    resp = requests.get(website_url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    div_tag = soup.find('div', class_ = 'center')
    tr_tags = div_tag.find_all('tr')

    print(tr_tags)
    for c in tr_tags[2:]:
        city_info = c.find_all('td')
        full_name = city_info[0].text
        if 'Can' not in full_name:
            regex = '[\w\s]+'
            city_name = re.findall(regex, full_name)[0]
            if city_name == 'Portland': 
                if 'Maine' in full_name:
                    city_name = 'Portland, ME' 
                else:
                    city_name = 'Portland, OR'
            elif city_name == 'Minneapolis':
                city_name = 'Minneapolis Saint-Paul'
            elif city_name == 'San Francisco':
                city_name = 'San Francisco Bay Area'
            elif city_name == 'St':
                city_name = 'St. Louis'
            elif city_name == 'Tampa':
                city_name = 'Tampa Bay Area'
            elif city_name == 'Washington':
                city_name = 'Washington D.C.'
            elif city_name == 'Miami':
                city_name = 'Miama'
            elif city_name == 'Grand Junction':
                city_name = 'Colorado Springs'

        print(city_name)
        lat = city_info[1].text
        long = city_info[3].text
        print((float(lat),float(long)))

        cur.execute("""
            INSERT INTO cityInformation (city, latitude, longitude)
            VALUES (?,?,?)
            """, (city_name, lat, long)) 
        conn.commit()
    
database_creation('database.db', 'https://www.infoplease.com/us/geography/latitude-and-longitude-us-and-canadian-cities')



