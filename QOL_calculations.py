import json
import os
import requests
import sqlite3
import matplotlib


def createCityIdTable(city_dict, db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cities = list(city_dict.keys())
    cur.execute("CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, name TEXT)")
    for i in range(len(cities)):
        cur.execute("INSERT OR IGNORE INTO Cities (id,name) VALUES (?,?)",(i,cities[i]))
    conn.commit()



def get_city_avg(db_filename, city):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('''SELECT Housing_score, Living_Cost_score, Startup_score, Venture_Capital_score, Travel_score, Commute_score, Business_Freedom_score, 
                    Safety_score, Healthcare_score, Education_score, Environmental_Quality_score, Economy_score, Taxation_score, Internet_Access_score, 
                    Leisure_Culture_score, Tolerance_score, Outdoors_score FROM CityQoL WHERE name = ?''', (city,))
    scores = cur.fetchall()

    total = 0
    count = 0
    for score in scores:
        for num in score: 
            total += float(num)
            count += 1

    avg = total / count

    return avg



def addAvgQoL(db_filename, city_dict):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cities = list(city_dict.keys())
    for city in cities: 
        avg = get_city_avg(db_filename, city)
        cur.execute("UPDATE CityQoL SET avgQoL = ? WHERE name = ?", (avg, city))

    conn.commit()
    return None


def main(): 
    city_name_dict = {'Albuquerque':'albuquerque', 'Anchorage':'anchorage', 'Asheville':'asheville', 'Atlanta':'atlanta', 'Austin': 'austin', 'Baltimore':'baltimore', 'Boise':'boise', 'Boston':'boston', 'Boulder':'boulder', 'Buffalo':'buffalo', 'Charleston':'charleston', 
    'Charlotte':'charlotte', 'Chicago':'chicago', 'Cincinnati':'cincinnati', 'Cleveland':'cleveland', 'Colorado Springs': 'colorado-springs', 'Columbus': 'columbus', 'Dallas': 'dallas', 'Denver': 'denver', 'Des Moines': 'des-moines', 'Detroit':'detroit', 'Honolulu': 'honolulu', 'Houston': 'houston', 
    'Indianapolis': 'indianapolis', 'Jacksonville': 'jacksonville', 'Kansas City': 'kansas-city', 'Knoxville':'knoxville', 'Las Vegas': 'las-vegas', 'Los Angeles': 'los-angeles', 'Louisville':'louisville', 'Madison':'madison', 'Memphis':'memphis', 'Miami':'miami', 'Milwaukee':'milwaukee', 
    'Minneapolis Saint-Paul': 'minneapolis-saint-paul', 'Nashville': 'nashville', 'New Orleans': 'new-orleans', 'New York':'new-york', 'Oklahoma City':'oklahoma-city', 'Omaha':'omaha', 'Orlando':'orlando', 'Palo Alto': 'palo-alto', 'Philadelphia':'philadelphia', 'Phoenix':'phoenix', 
    'Pittsburgh':'pittsburgh', 'Portland, ME': 'portland-me', 'Portland, OR': 'portland-or', 'Providence':'providence', 'Raleigh':'raleigh', 'Richmond':'richmond', 'Rochester': 'rochester', 'Salt Lake City': 'salt-lake-city', 'San Antonio':'san-antonio', 'San Diego':'san-diego', 
    'San Francisco':'san-francisco-bay-area', 'Seattle': 'seattle', 'St. Louis': 'st-louis', 'Tampa Bay Area':'tampa-bay-area', 'Washington D.C.': 'washington-dc'}

    createCityIdTable(city_name_dict, 'database.db')
    addAvgQoL('database.db', city_name_dict)


main()
