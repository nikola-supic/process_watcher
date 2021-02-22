"""
Created on Wed Feb 17 18:57:11 2020

@author: Sule
@name: database.py
@description: ->
	DOCSTRING:
"""

from datetime import datetime, timedelta
import mysql.connector
from time import sleep

while True:
	try:
		mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='',
			database='process_watcher'
			)
		mycursor = mydb.cursor()
		break
	except mysql.connector.errors.InterfaceError: 
		print('[-] Cant connect to DB.')
		sleep(5)

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

def reset_start_time():
	mycursor.execute("UPDATE apps SET time_started=NULL")
	mydb.commit()


def update_on_quit():
	mycursor.execute("SELECT id, daily, monthly, yearly, all_time, time_started FROM apps WHERE time_started != '0000-00-00 00:00:00'")
	result = mycursor.fetchall()
	for row in result:
		proc_id = row[0]
		daily = row[1]
		monthly = row[2]
		yearly = row[3]
		all_time = row[4]
		time_started = row[5]
		# print(proc_id, daily, monthly, yearly, all_time, time_started)

		time_finished = datetime.now()
		duration = int((time_finished - time_started).total_seconds())
		date = datetime.now()
		daily += duration
		monthly += duration
		yearly += duration
		all_time += duration

		sql = "UPDATE apps SET date=%s, daily=%s, monthly=%s, yearly=%s, all_time=%s, time_started=NULL WHERE id=%s"
		val = (date, daily, monthly, yearly, all_time, proc_id, )
		mycursor.execute(sql, val)
		mydb.commit()

		print(f'[-] Shuting down (ID: {proc_id})... ({duration}s)')