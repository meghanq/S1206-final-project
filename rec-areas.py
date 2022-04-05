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
def get_rec_data(longitude, latitude, radius):
    pass

def main():
    cur, conn = setUpDatabase('database.db')
    createCityIdTable(cur, conn)

    
if __name__ == "__main__":
    main()