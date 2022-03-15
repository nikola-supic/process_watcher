"""
Created on Wed Feb 17 18:04:39 2020

@author: Sule
@name: process_watcher.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

# Importing the libraries
from datetime import datetime, timedelta
import wmi

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock

import database as DB


class Process():
    """
    DOCSTRING:

    """
    def __init__(self, row):
        """
        DOCSTRING:

        """
        self.sql_id = row[0]
        self.name = row[1]
        self.caption = row[2]
        self.type = row[3]
        self.date = row[4]
        self.daily = row[5]
        self.monthly = row[6]
        self.yearly = row[7]
        self.all_time = row[8]

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
        val = (self.daily, self.monthly, self.yearly, self.sql_id, )
        mycursor.execute(sql, val)
        mydb.commit()


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


class MainWindow(Screen):
    """
    DOCSTRING:

    """


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
        self.event = None

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
            process = Process(row)
            process_list.append(process)
        return process_list

    def check_for_change(self):
        """
        DOCSTRING:

        """
        c_list = wmi.WMI()
        active_list = [x for x in self.process_list if x.active]
        inactive_list = [x for x in self.process_list if not x.active]

        for tmp in self.process_list:
            tmp.active = False

        for process in c_list.Win32_Process(["Caption"]):
            if process.Caption in self.caption_list:
                sql_id = self.caption_list[process.Caption] - 1
                current_proc = self.process_list[sql_id]
                if not current_proc.active:
                    current_proc.active = True

        output = []
        for tmp in active_list:
            if not self.process_list[tmp.sql_id-1].active:
                output.append(self.process_shutdown(tmp))

        for tmp in inactive_list:
            if self.process_list[tmp.sql_id-1].active:
                output.append(self.process_start(tmp))

        return output

    def process_start(self, process):
        """
        DOCSTRING:

        """
        process.time_started = datetime.now()
        sql = "UPDATE apps SET time_started=%s WHERE id=%s"
        val = (process.time_started, process.sql_id)
        DB.mycursor.execute(sql, val)
        DB.mydb.commit()

        return f'[+] Starting {process.name}...'

    def process_shutdown(self, proc):
        """
        DOCSTRING:

        """
        time_finished = datetime.now()
        duration = int((time_finished - proc.time_started).total_seconds())

        date = datetime.now()
        proc.daily += duration
        proc.monthly += duration
        proc.yearly += duration
        proc.all_time += duration
        proc.time_started = None
        proc.active = False

        sql = "UPDATE apps SET date=%s, daily=%s, monthly=%s, yearly=%s, all_time=%s, time_started=NULL WHERE id=%s"
        val = (date, proc.daily, proc.monthly, proc.yearly, proc.all_time, proc.sql_id, )
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        return f'[-] Shuting down {proc.name}... ({timedelta(seconds=duration)}s)'

    def checking(self, dt):
        """
        DOCSTRING:

        """
        output_text = self.check_for_change()
        for item in output_text:
            self.output.text += item + '\n'

    def run(self):
        """
        DOCSTRING:

        """
        self.running = True
        self.checking(None)
        self.event = Clock.schedule_interval(self.checking, 15)

    def stop(self):
        """
        DOCSTRING:

        """
        self.running = False
        self.event.cancel()
        for process in self.process_list:
            if process.active:
                self.output.text += self.process_shutdown(process) + '\n'

    def start_stop_button(self):
        """
        DOCSTRING:

        """
        if self.running:
            self.output.text += '\n[*] STOPING PROCESS WACHER\n'
            self.stop()
            self.output_button.text = 'START ALL PROCESS (START WATCHING)'

        else:
            self.output.text += '\n[*] STARTING PROCESS WACHER\n'
            self.run()
            self.output_button.text = 'SHUTDOWN ALL PROCESS (STOP WATCHING)'


class AddProcess(MainWindow):
    """
    DOCSTRING:

    """
    proc_name = ObjectProperty(None)
    proc_caption = ObjectProperty(None)
    proc_type = ObjectProperty(None)

    def add_process(self):
        """
        DOCSTRING:

        """
        DB.new_process(self.proc_name.text, self.proc_caption.text, self.proc_type.text)

        self.proc_name.text = ''
        self.proc_caption.text = ''
        self.proc_type.text = ''

        show_popup('info', 'Successfuly added new process to DB.')


class OverallStats(MainWindow):
    """
    DOCSTRING:

    """
    stats_output = ObjectProperty(None)

    def get_stats(self):
        """
        DOCSTRING:

        """
        stats_text = DB.get_stats()
        self.stats_output.text = stats_text


class AppUsage(MainWindow):
    """
    DOCSTRING:

    """
    app_input = ObjectProperty(None)
    app_output = ObjectProperty(None)

    def get_usage(self):
        """
        DOCSTRING:

        """
        output_text = DB.get_usage(self.app_input.text)
        self.app_input.text = ''

        if not output_text:
            show_popup('error', 'Wrong application name.')
        else:
            self.app_output.text = output_text


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
        """
        DOCSTRING:

        """
        show_popup('quit', 'Are you sure you want to quit?')
        return True


def show_popup(type, txt):
    """
    DOCSTRING:

    """
    if type == 'error':
        popup = PopupError()
        popup.ids.error_label.text = txt
        popup.open()
    elif type == 'info':
        popup = PopupInfo()
        popup.ids.info_label.text = txt
        popup.open()
    elif type == 'quit':
        popup = PopupQuit()
        popup.ids.quit_label.text = txt
        popup.open()
    else:
        show_popup(type='error', txt='Trying to create wrong type of popup screen.')

if __name__ == '__main__':
    # Config.set('kivy', 'exit_on_escape', '0')
    # Config.set('graphics', 'resizable', False)
    # Config.write()

    Window.size = (480, 360)
    Application().run()
