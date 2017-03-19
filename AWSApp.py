#!/usr/bin/python3
import collections
from kivy.adapters import listadapter
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

    def doConfiguredPlugins(self):
        ret = ''
        plugs = pluginManager.getConfiguredPlugins()
        for p in plugs:
            ret += p + "\n"
        self.text = ret

class MyScreenManager(ScreenManager):
    pass

class PluginsListButton(ListItemButton):
    pass

class PluginsOutputListButton(ListItemButton):
    pass

class Listview(ListView):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        ### Bind to `on_selection_change` here in `__init__`
        self.ids['listview'].adapter.bind(on_selection_change=self.callback)
        print(self.ids)

class MainWindow(GridLayout):
    student_list = ObjectProperty()
    manager = ObjectProperty(None)
    text = StringProperty('')
    data = ListProperty([])
    outData = ListProperty([])

    # Parse the plugin data and populate the listview
    def update(self):
        s3Data = pluginManager.getS3Plugs()
        tData = []
        keys = s3Data.keys()
        for k in keys:
            tData.append(k)

        ec2Data = pluginManager.getEc2Plugs()
        keys = ec2Data.keys()
        for k in keys:
            tData.append(k)

        ebsData = pluginManager.getEbsPlugs()
        keys = ebsData.keys()
        print(ebsData)
        for k in keys:
            tData.append(k)
        self.data = tData

    def clear(self):
        self.data = []
        self.outData = []

    # overwrite the switch_to function to control the
    #   screenmanager from here
    def switch_to(self, text):
        self.manager.current = text.screen
        self.current = text

    def display(self):
        if self.list_view.adapter.selection:
            sel = self.list_view.adapter.selection[0].text
            self.outData = []

            if "s3" in sel:
                s3Data = pluginManager.getS3Plugs()
                tData = []
                res = s3Data[sel]
                print("RES: "+str(res))
                for k in res:
                    if type(k) == str:
                        tData.append(k)
                    else:
                        for p in k.keys():
                            tData.append(k[p])
                self.outData = tData

            elif "ec2" in sel:
                ec2Data = pluginManager.getEc2Plugs()
                tData = []
                res = ec2Data[sel]
                print("RES: "+ str(res))
                if type(res) == collections.Counter:
                    for k in res:
                        tData.append(k+": "+str(res[k]))
                else:
                    for k in res:
                        tData.append(k)
                self.outData = tData

            elif "ebs" in sel:
                ebsData = pluginManager.getEbsPlugs()
                tData = []
                res = ebsData[sel]
                print("RES: "+ str(res))
                if type(res) == collections.Counter:
                    for k in res:
                        tData.append(k+": "+str(res[k]))
                else:
                    for k in res:
                        tData.append(k)
                self.outData = tData






class AWSApp(App):
    def build(self):
        return MainWindow()

