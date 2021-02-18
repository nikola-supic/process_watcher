"""
Created on Fri Wed 17 18:57:11 2020

@author: Sule
@name: database.py
@description: ->
    DOCSTRING:
"""

from datetime import datetime, timedelta
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='process_watcher'
        )
    mycursor = mydb.cursor()
except mysql.connector.errors.InterfaceError: 
    print('[-] Cant connect to DB.')
    sys.exit()

def new_process(name, caption, typ):
	sql = "INSERT INTO apps (name, caption, type) VALUES (%s, %s, %s)"
	val = (name, caption, typ, )

	mycursor.execute(sql, val)
	mydb.commit()