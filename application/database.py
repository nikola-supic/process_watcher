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

def get_stats():
	mycursor.execute("SELECT * FROM apps ORDER BY type")
	result = mycursor.fetchall()
	output = ''
	for row in result:
		output += f'{row[1]} - {row[3]} - Usage: {timedelta(seconds=row[8])}\n'
	return output

def get_usage(name):
	sql = "SELECT * FROM apps WHERE name=%s LIMIT 1"
	val = (name, )
	mycursor.execute(sql, val)
	row = mycursor.fetchone()
	if row:
		return f'Name: {row[1]} ({row[2]})\nType: {row[3]}\nLast time used: {row[4]}\nDaily usage: {row[5]}\nMonthly usage: {row[6]}\nYearly: {row[7]}\nOverall usage: {row[8]}'
	return False