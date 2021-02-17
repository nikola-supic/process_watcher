"""
Created on Fri Wed 17 18:04:39 2020

@author: Sule
@name: process_watcher.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.core.window import Window

class WelcomeWindow(Screen):
    """
    DOCSTRING:

    """


class MainWindow(Screen):
    """
    DOCSTRING:

    """


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
        # self.icon = 'images/icon.png'
        self.title = 'PW // Process Watcher'


if __name__ == '__main__':
    # Config.set('kivy', 'exit_on_escape', '0')
    Config.set('graphics', 'resizable', False)
    Config.write()

    Window.size = (480, 480)
    Application().run()