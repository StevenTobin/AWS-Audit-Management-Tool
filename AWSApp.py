#!/usr/bin/python3

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListItemButton
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.adapters.dictadapter import DictAdapter
import pluginManager
import core
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
import boto3

class HomeScreen(Screen):
    text = StringProperty('')

    # overwrite the switch_to function to control the
    #   screenmanager from here
    def switch_to(self, text):
        self.manager.transition.direction = 'right'
        self.manager.current = text
        self.current = text

class PluginsScreen(Screen):
    text = StringProperty('')

    # overwrite the switch_to function to control the
    #   screenmanager from here
    def switch_to(self, text):
        self.manager.transition.direction = 'left'
        self.manager.current = text
        self.current = text

class MyScreenManager(ScreenManager):
    pass

class StudentListButton(ListItemButton):
    pass

class Listview(ListView):
    pass

class MainWindow(GridLayout):
    student_list = ObjectProperty()
    manager = ObjectProperty(None)
    text = StringProperty('')
    data = ListProperty([])

    # Parse the plugin data and populate the listview
    def update(self):
        s3Data = pluginManager.getS3Plugs()
        tData = []
        keys = s3Data.keys()
        for k in keys:
            tData.append(k)
            for d in s3Data[k]:
                for pkey in d.keys():
                    tData.append(d[pkey])

        ec2Data = pluginManager.getEc2Plugs()
        keys = ec2Data.keys()
        for k in keys:
            tData.append(k)
            for d in ec2Data[k]:
                for pkey in d.keys():
                    tData.append(d[pkey])
        self.data = tData


    # overwrite the switch_to function to control the
    #   screenmanager from here
    def switch_to(self, text):
        self.manager.current = text.screen
        self.current = text


    def doConfiguredServices(self):
        ret = ''
        servs = pluginManager.getConfiguredServices()
        for s in servs:
            ret += s+"\n"
        s = PluginsScreen(name = "confServices", text=ret)
        l = Label(text = ret)
        self.add_widget(s)
        self.current=("confServices")

    def doConfiguredPlugins(self):
        ret = ''
        plugs = pluginManager.getConfiguredPlugins()
        for p in plugs:
            ret += p + "\n"
        s = PluginsScreen(name="confPlugins", text=ret)
        l = Label(text=ret)
        self.add_widget(s)
        self.current = ("confPlugins")

    def pluginsScreen(self):
        pass

class AWSApp(App):
    def build(self):
        return MainWindow()

