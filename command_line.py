"""
Created on Fri Feb 17 11:25:2503 2021

@author: Sule
@name: process_watcher.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

# Importing the libraries
from threading import Timer
from sys import exit
from datetime import datetime
import wmi
import pythoncom
import mysql.connector

class Process():
    """
    DOCSTRING:

    """
    def __init__(self, id, name, caption, type, date, daily, monthly, yearly, all_time):
        """
        DOCSTRING:

        """
        self.id = id
        self.name = name
        self.caption = caption
        self.type = type
        self.date = date
        self.daily = daily
        self.monthly = monthly
        self.yearly = yearly
        self.all_time = all_time

        self.time_started = datetime.now()
        self.active = False

    def check_date(self, mydb, mycursor):
        """
        DOCSTRING:

        """
        today = datetime.now()
        if today.day != self.date.day:
            self.daily = 0
        if today.month != self.date.month:
            self.monthly = 0
        if today.year != self.date.year:
            self.yearly = 0

        sql = "UPDATE apps SET daily=%s, monthly=%s, yearly=%s WHERE id=%s"
        val = (self.daily, self.monthly, self.yearly, self.id, )
        mycursor.execute(sql, val)
        mydb.commit()


class App():
    """
    DOCSTRING:

    """
    def __init__(self, mydb, mycursor):
        """
        DOCSTRING:

        """
        self.mydb = mydb
        self.mycursor = mycursor
        self.caption_list = self.get_captions_from_db()
        self.process_list = self.get_processes_from_db()
        self.check_date()


    def check_date(self):
        """
        DOCSTRING:

        """
        for process in self.process_list:
            process.check_date(self.mydb, self.mycursor)

    def get_captions_from_db(self):
        """
        DOCSTRING:

        """
        caption_list = {}
        self.mycursor.execute("SELECT id, caption FROM apps")
        result = self.mycursor.fetchall()
        for row in result:
            caption_list[row[1]] = row[0]
        return caption_list


    def get_processes_from_db(self):
        """
        DOCSTRING:

        """
        process_list = []
        self.mycursor.execute("SELECT * FROM apps")
        result = self.mycursor.fetchall()
        for row in result:
            process = Process(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            process_list.append(process)
        return process_list


    def check_for_change(self):
        """
        DOCSTRING:

        """
        c = wmi.WMI()
        active_list = [x for x in self.process_list if x.active]
        inactive_list = [x for x in self.process_list if not x.active]

        for tmp in self.process_list:
            tmp.active = False

        for process in c.Win32_Process(["Caption"]):
            if process.Caption in self.caption_list:
                id = self.caption_list[process.Caption] - 1
                current_proc = self.process_list[id]
                if not current_proc.active:
                    current_proc.active = True

        for tmp in active_list:
            if not self.process_list[tmp.id-1].active:
                self.process_shutdown(tmp)

        for tmp in inactive_list:
            if self.process_list[tmp.id-1].active:
                self.process_start(tmp)

        return [x for x in self.process_list if x.active], [x for x in self.process_list if not x.active]


    def process_start(self, process):
        """
        DOCSTRING:

        """
        process.time_started = datetime.now()
        print(f'[+] Starting {process.name}...')


    def process_shutdown(self, process):
        """
        DOCSTRING:

        """
        time_finished = datetime.now()
        duration = int((time_finished - process.time_started).total_seconds())

        date = datetime.now()
        process.daily += duration
        process.monthly += duration
        process.yearly += duration
        process.all_time += duration

        sql = "UPDATE apps SET date=%s, daily=%s, monthly=%s, yearly=%s, all_time=%s WHERE id=%s"
        val = (date, process.daily, process.monthly, process.yearly, process.all_time, process.id, )
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        print(f'[-] Shuting down {process.name}... ({duration}s)')


    def run(self):
        """
        DOCSTRING:

        """
        pythoncom.CoInitialize()
        active_list, inactive_list = self.check_for_change()

        timer = Timer(9.0, self.run)
        timer.start()


def main():
    """
    DOCSTRING:

    """
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
        exit()

    app = App(mydb, mycursor)
    app.run()



if __name__ == '__main__':
    main()
