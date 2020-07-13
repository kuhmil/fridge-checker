import sqlite3 as lite
import sys
from sensors import read_temp 
con = lite.connect('sensorsData.db')
print("reading temp")
#print(read_temp())
temp = 2
with con:
    cur = con.cursor()
    cur.execute(INSERT INTO sensor_data VALUES(datetime('now'), temp))
    print("reading temp")
    print(read_temp())