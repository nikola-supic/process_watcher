"""
Created on Wed Feb 17 18:04:39 2020

@author: Sule
@name: process_watcher.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

# Importing the libraries
from threading import Timer, Thread
from datetime import datetime, timedelta
import wmi
import pythoncom
import time

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import database as DB

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

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


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

class CustomPopup(Popup):
    """
    DOCSTRING:

    """


class PopupError(CustomPopup):
    """
    DOCSTRING:

    """


class PopupInfo(CustomPopup):
    """
    DOCSTRING:

    """


class PopupQuit(CustomPopup):
    """
    DOCSTRING:

    """
    def quit_app(self):
        DB.update_on_quit()


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class MainWindow(Screen):
    """
    DOCSTRING:

    """

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

class OutputWindow(MainWindow):
    """
    DOCSTRING:

    """
    output = ObjectProperty(None)
    output_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        DOCSTRING:

        """
        super().__init__(**kwargs)

        self.mydb = DB.mydb
        self.mycursor = DB.mycursor
        self.caption_list = self.get_captions_from_db()
        self.process_list = self.get_processes_from_db()
        self.check_date()
        self.running = False


    def on_pre_enter(self):
        """
        DOCSTRING:

        """
        DB.reset_start_time()

        if not self.running:
            self.run()

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

        output = []
        for tmp in active_list:
            if not self.process_list[tmp.id-1].active:
                output.append(self.process_shutdown(tmp))

        for tmp in inactive_list:
            if self.process_list[tmp.id-1].active:
                output.append(self.process_start(tmp))

        return output


    def process_start(self, process):
        """
        DOCSTRING:

        """
        process.time_started = datetime.now()
        sql = "UPDATE apps SET time_started=%s WHERE id=%s"
        val = (process.time_started, process.id)
        DB.mycursor.execute(sql, val)
        DB.mydb.commit()

        return f'[+] Starting {process.name}...'


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
        process.time_started = None
        process.active = False

        sql = "UPDATE apps SET date=%s, daily=%s, monthly=%s, yearly=%s, all_time=%s, time_started=NULL WHERE id=%s"
        val = (date, process.daily, process.monthly, process.yearly, process.all_time, process.id, )
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        return f'[-] Shuting down {process.name}... ({timedelta(seconds=duration)}s)'


    def run_thread(self):
        """
        DOCSTRING:

        """
        pythoncom.CoInitialize()
        while self.running:
            output_text = self.check_for_change()

            for item in output_text:
                self.output.text += item + '\n'

            time.sleep(60) 


    def run(self):
        """
        DOCSTRING:

        """
        self.running = True
        self.thread = Thread(target = self.run_thread)
        self.thread.daemon = True
        self.thread.start()


    def start_stop_button(self):
        """
        DOCSTRING:

        """
        if self.running:
            self.output.text += '\n[*] STOPING PROCESS WACHER\n'

            self.running = False
            self.output_button.text = 'START ALL PROCESS (START WATCHING)'

            output_text = ''
            for process in self.process_list:
                if process.active:
                    output_text += self.process_shutdown(process) + '\n'

            self.output.text += output_text

        else:
            self.output.text += '\n[*] STARTING PROCESS WACHER\n'
            self.run()
            self.output_button.text = 'SHUTDOWN ALL PROCESS (STOP WATCHING)'


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class AddProcess(MainWindow):
    """
    DOCSTRING:

    """
    proc_name = ObjectProperty(None)
    proc_caption = ObjectProperty(None)
    proc_type = ObjectProperty(None)

    def add_process(self):
        DB.new_process(self.proc_name.text, self.proc_caption.text, self.proc_type.text)

        self.proc_name.text = ''
        self.proc_caption.text = ''
        self.proc_type.text = ''

        show_popup('info', 'Successfuly added new process to DB.')


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class OverallStats(MainWindow):
    """
    DOCSTRING:

    """
    stats_output = ObjectProperty(None)

    def get_stats(self):
        stats_text = DB.get_stats()
        self.stats_output.text = stats_text

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class AppUsage(MainWindow):
    """
    DOCSTRING:

    """
    app_input = ObjectProperty(None)
    app_output = ObjectProperty(None)

    def get_usage(self):
        output_text = DB.get_usage(self.app_input.text)
        self.app_input.text = ''
        
        if not output_text:
            show_popup('error', 'Wrong application name.')
        else:
            self.app_output.text = output_text

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

class WindowManager(ScreenManager):
    """
    DOCSTRING:

    """

class Application(MDApp):
    """
    DOCSTRING:

    """
    def build(self):
        """
        DOCSTRING:

        """
        self.icon = 'images/icon.png'
        self.title = 'PW // Process Watcher'
        Window.bind(on_request_close=self.on_request_close)

    def on_request_close(self, *args):
        show_popup('quit', 'Are you sure you want to quit?')
        return True


def show_popup(type, text):
    """
    DOCSTRING:

    """
    if type == 'error':
        popup = PopupError()
        popup.ids.error_label.text = text
        popup.open()
    elif type == 'info':
        popup = PopupInfo()
        popup.ids.info_label.text = text
        popup.open()
    elif type == 'quit':
        popup = PopupQuit()
        popup.ids.quit_label.text = text
        popup.open()
    else:
        show_popup(type='error', text='Trying to create wrong type of popup screen.')

if __name__ == '__main__':
    # Config.set('kivy', 'exit_on_escape', '0')
    # Config.set('graphics', 'resizable', False)
    # Config.write()

    Window.size = (480, 360)
    Application().run()