# database.py
import mysql.connector

search_list = ['steam.exe', 'sublime_text.exe', 'msedge.exe', 'ConEmuC64.exe', 'GitHubDesktop.exe', 'vlc.exe']
search_names = ['Steam', 'Sublime Text', 'MS Edge', 'CMD', 'GitHub', 'VLC']
search_types = ['Gaming', 'Learning', 'Browsing', 'Learning', 'Learning', 'Learning']

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


for caption, name, s_type in zip(search_list, search_names, search_types):
	sql = "INSERT INTO apps (name, caption, type) VALUE (%s, %s, %s)"
	val = (name, caption, s_type)
	
	mycursor.execute(sql, val)
	mydb.commit()