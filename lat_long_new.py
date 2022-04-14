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

    cur.execute("DROP TABLE IF EXISTS cityInformation")

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
        city_full_name = lat_long[0].text
        regex = '^(.+?),'
        city_name = re.findall(regex, city_full_name)[0]
        print((city_name, float(lat),float(long)))

        cur.execute("""
        INSERT INTO cityInformation (city, latitude, longitude)
        VALUES (?,?,?)
        """, (city_name, lat, long)) 
        conn.commit()

    my_list = [['Albuquerque', 35.0844, -106.6504], ['Portland, OR', 45.5152, -122.6784], ['Orlando', 28.5384, -81.3789], ['Atlanta', 33.7490, -84.3880], ['Austin', 30.2672, -97.7431], ['Baltimore', 39.2904, -76.6122], ['Boston', 42.3601, -71.0589], ['Boulder', 40.0150, -105.2705], ['Anchorage', 61.2181, -149.9003], ['Asheville', 35.5951, -82.5515], ['Buffalo', 42.8864, -78.8784], ['Calgary', 51.0447, -114.0719],['Charlotte', 35.2271, -80.8431], ['Chicago', 41.8781, -87.6298], ['Cincinnati', 39.1031, -84.5120],['Charleston', 32.7765, -79.9311], ['Cleveland', 41.4993, -81.6944], ['Denver', 39.7392, -104.9903], ['Milwaukee', 43.0389, -87.9065], ['Nashville', 36.1627, -86.7816], ['Portland, ME', 43.6591, -70.2568], ['Seattle', 47.6062, -122.3321], ['Dallas', 32.7767, -96.7970], ['Des Moines', 41.5868, -93.6250], ['Honolulu', 21.3069, -157.8583], ['Houston', 29.7604, -95.3698], ['Indianapolis', 39.7684, -86.1581], ['Jacksonville', 30.3322, -81.6557], ['Kansas City', 39.0997, -94.5786], ['Las Vegas', 36.1699, -115.1398], ['Los Angeles', 34.0522, -118.2437], ['Louisville', 38.2527, -85.7585], ['Madison', 43.0722, -89.4008], ['Memphis', 35.1495, -35.1495], ['Miami', 25.7617, -80.1918], ['Minneapolis Saint-Paul', 44.9375, -93.2010], ['New Orleans', 29.9511, -90.0715], ['New York', 40.7128, -74.0060], ['Omaha', 41.2565, -95.9345], ['Palo Alto', 37.4419, -122.1430], ['Philadelphia', 39.9526, -75.1652], ['Phoenix', 33.4484, -112.0740], ['Providence', 41.8240, -71.4128], ['Raleigh', 35.7796, -78.6382], ['Richmond', 37.5407, -77.4360], ['Rochester', 43.1566, -77.6088], ['San Diego', 32.7157, -117.1611], ['St. Louis', 38.6270, -90.1994], ['Tampa Bay Area', 27.9506, -82.4572], ['Washington D.C.', 38.9072, -77.0369]]
    for c in my_list:
        cur.execute("""
        INSERT INTO cityInformation (city, latitude, longitude)
        VALUES (?,?,?)
        """, (c[0], c[1], c[2])) 
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