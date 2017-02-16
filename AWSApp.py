#!/usr/bin/python3

from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix import actionbar
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import pluginManager


class HomeScreen(Screen):
    text = StringProperty('')
    mode = ObjectProperty('spinner')

class PluginsScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    def doStuff(self):
        ec2Data = pluginManager.getEc2Plugs()
        ec2 = ''
        for d in ec2Data:
            print(d)
            for i in d:
                ec2 += i + ": "+ str(d[i]) +"\n"
            print("ec2: " +str(ec2))
        l = Label(text=ec2)
        s = HomeScreen(name = ec2, text = ec2)
        self.add_widget(s)
        self.current = ec2

class AWSApp(App):
    def build(self):
        return MyScreenManager()

