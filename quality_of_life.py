import json
import unittest
import os
import requests
import sqlite3
import matplotlib

#base_url = 'https://api.teleport.org/api/'

    
def get_city_data(city):
    url = f'https://api.teleport.org/api/urban_areas/slug:{city}/scores/'

    try: 
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data['categories']

    except: 
        print('Exception')
        return None

def createCityIdTable(city_dict, db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cities = list(city_dict.keys())
    cur.execute("CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, name TEXT)")
    for i in range(len(cities)):
        cur.execute("INSERT INTO Cities (id,name) VALUES (?,?)",(i,cities[i]))
    conn.commit()



def createQoLCityTable(city_dict, db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS CityQoL (city_id INTEGER PRIMARY KEY, name TEXT, Housing_score NUMBER, Living_Cost_score NUMBER, 
    Startup_score NUMBER, Venture_Capital_score NUMBER, Travel_score NUMBER, Commute_score NUMBER, Business_Freedom_score NUMBER, 
    Safety_score NUMBER, Healthcare_score NUMBER, Education_score NUMBER, Environmental_Quality_score NUMBER, Economy_score NUMBER, 
    Taxation_score NUMBER, Internet_Access_score NUMBER, Leisure_Culture_score NUMBER, Tolerance_score NUMBER, Outdoors_score NUMBER, avgQoL NUMBER)''')

    cur.execute('SELECT city_id FROM CityQoL WHERE city_id  = (SELECT MAX(city_id) FROM CityQoL)')
    start = cur.fetchone()
    if (start != None):
        start = start[0] + 1
    else:
        start = 0

    count = 0
    cities = list(city_dict.keys())

    for city in cities[start:start+19]:


        url_city = city_dict[city]
        data = get_city_data(url_city)

        city_id = count + start
        name = city
        Housing_score = data[0]['score_out_of_10']
        Living_Cost_score = data[1]['score_out_of_10']
        Startup_score = data[2]['score_out_of_10']
        Venture_Capital_score = data[3]['score_out_of_10']
        Travel_score = data[4]['score_out_of_10']
        Commute_score = data[5]['score_out_of_10']
        Business_Freedom_score = data[6]['score_out_of_10']
        Safety_score = data[7]['score_out_of_10']
        Healthcare_score = data[8]['score_out_of_10']
        Education_score = data[9]['score_out_of_10']
        Environmental_Quality_score = data[10]['score_out_of_10']
        Economy_score = data[11]['score_out_of_10']
        Taxation_score = data[12]['score_out_of_10']
        Internet_Access_score = data[13]['score_out_of_10']
        Leisure_Culture_score = data[14]['score_out_of_10']
        Tolerance_score = data[15]['score_out_of_10']
        Outdoors_score = data[16]['score_out_of_10']
        avgQoL = get_city_avg('database.db', city)

       
        cur.execute('''INSERT INTO CityQoL (city_id, name, Housing_score, Living_Cost_score, Startup_score, Venture_Capital_score, Travel_score, Commute_score, Business_Freedom_score, 
                    Safety_score, Healthcare_score, Education_score, Environmental_Quality_score, Economy_score, Taxation_score, Internet_Access_score, 
                    Leisure_Culture_score, Tolerance_score, Outdoors_score, avgQoL) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (city_id, name, Housing_score, Living_Cost_score, Startup_score, Venture_Capital_score, Travel_score, Commute_score, Business_Freedom_score, 
                    Safety_score, Healthcare_score, Education_score, Environmental_Quality_score, Economy_score, Taxation_score, Internet_Access_score, 
                    Leisure_Culture_score, Tolerance_score, Outdoors_score, avgQoL))

        count +=1

    conn.commit()
    

    

def get_city_avg(db_filename, city):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('''SELECT Housing_score, Living_Cost_score, Startup_score, Venture_Capital_score, Travel_score, Commute_score, Business_Freedom_score, 
                    Safety_score, Healthcare_score, Education_score, Environmental_Quality_score, Economy_score, Taxation_score, Internet_Access_score, 
                    Leisure_Culture_score, Tolerance_score, Outdoors_score FROM CityQoL WHERE name = ?''', (city,))
    scores = cur.fetchall()
    print(scores)

    total = 0
    count = 0
    for score in scores:
        for num in score: 
            print(num)
            total += float(num)
            count += 1

    avg = total / count
    # print(count)
    return avg




def main():

    city_data_dictionary = {}
    city_name_dict = {'Albuquerque':'albuquerque', 'Anchorage':'anchorage', 'Asheville':'asheville', 'Atlanta':'atlanta', 'Austin': 'austin', 'Baltimore':'baltimore', 'Boise':'boise', 'Boston':'boston', 'Boulder':'boulder', 'Buffalo':'buffalo', 'Charleston':'charleston', 
    'Charlotte':'charlotte', 'Chicago':'chicago', 'Cincinnati':'cincinnati', 'Cleveland':'cleveland', 'Colorado Springs': 'colorado-springs', 'Columbus': 'columbus', 'Dallas': 'dallas', 'Denver': 'denver', 'Des Moines': 'des-moines', 'Detroit':'detroit', 'Honolulu': 'honolulu', 'Houston': 'houston', 
    'Indianapolis': 'indianapolis', 'Jacksonville': 'jacksonville', 'Kansas City': 'kansas-city', 'Knoxville':'knoxville', 'Las Vegas': 'las-vegas', 'Los Angeles': 'los-angeles', 'Louisville':'louisville', 'Madison':'madison', 'Memphis':'memphis', 'Miami':'miami', 'Milwaukee':'milwaukee', 
    'Minneapolis Saint-Paul': 'minneapolis-saint-paul', 'Nashville': 'nashville', 'New Orleans': 'new-orleans', 'New York':'new-york', 'Oklahoma City':'oklahoma-city', 'Omaha':'omaha', 'Orlando':'orlando', 'Palo Alto': 'palo-alto', 'Philadelphia':'philadelphia', 'Phoenix':'phoenix', 
    'Pittsburgh':'pittsburgh', 'Portland, ME': 'portland-me', 'Portland, OR': 'portland-or', 'Providence':'providence', 'Raleigh':'raleigh', 'Richmond':'richmond', 'Rochester': 'rochester', 'Salt Lake City': 'salt-lake-city', 'San Antonio':'san-antonio', 'San Diego':'san-diego', 
    'San Francisco':'san-francisco-bay-area', 'Seattle': 'seattle', 'St. Louis': 'st-louis', 'Tampa Bay Area':'tampa-bay-area', 'Washington D.C.': 'washington-dc'}
    
    createCityIdTable(city_name_dict, 'database.db')
    createQoLCityTable(city_name_dict, 'database.db')
    


main()

