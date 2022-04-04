from bs4 import BeautifulSoup
import requests
import re

#be sure to follow city, state
def find_lat_long(city):
    resp = requests.get('https://www.latlong.net/category/cities-236-15.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    tr_tags = soup.find_all('tr')
    #print(tr_tags)
    for c in tr_tags[1:]:
        city_name = c.find('a').text

        #print(city_name)
        if city_name[:-5] == city:
            lat_long = c.find_all('td')
            lat = lat_long[1].text
            long = lat_long[2].text
            print((float(lat),float(long)))
find_lat_long('Herrin, IL')
