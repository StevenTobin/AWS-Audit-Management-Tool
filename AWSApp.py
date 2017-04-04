#!/usr/bin/python3
import collections

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import threading
import boto3
import json
import pluginManager
import core

s3Data = []
ec2Data = []
ebsData = []

PopulatedFlag = 0
FetchedFlag = 0

class HomeScreen(Screen):
    text = StringProperty('')
    tableLayout = ObjectProperty(None)

    def buildTable(self):
        self.tableLayout.clear_widgets()
        self.tableLayout.add_widget(Label(text="Region", size_hint=(1, None), height=40))
        self.tableLayout.add_widget(Label(text="Ec2Instances", size_hint=(1, None), height=40))
        self.tableLayout.add_widget(Label(text="EbsVolumes", size_hint=(1, None), height=40))
        self.tableLayout.add_widget(Label(text="UnattachedVolumes", size_hint=(1, None), height=40))
        self.showpopup()
        self.pop_up.value = 0
        regions = core.doReadRegions()
        self.pop_up.update_pop_up_info('Building overview')
        tableLayout = self.tableLayout
        for reg in regions:
            self.pop_up.update_pop_up_text('Current Region: ' + str(reg))
            self.tableLayout.add_widget(Label(text=reg, size_hint=(1, None), height=40))
            tableLayout.height=self.tableLayout.minimum_height
            for e in ec2Data:
                if reg in e:
                    k = len(e[reg].keys())
                    self.tableLayout.add_widget(Label(text=str(k), size_hint=(1, None), height=40))
                    tableLayout.height = self.tableLayout.minimum_height
            for v in ebsData:
                if reg in v:
                    kv = len(v[reg].keys())
                    self.tableLayout.add_widget(Label(text=str(kv), size_hint=(1, None), height=40))
                    tableLayout.height = self.tableLayout.minimum_height
            self.tableLayout.add_widget(Label(text="None unattached", size_hint=(1, None), height=40))
            tableLayout.height = self.tableLayout.minimum_height

        self.pop_up.dismiss()


    def showpopup(self):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text('Connecting...')
        self.pop_up.open()

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

class TableRow(Widget):
    pass

class MyScreenManager(ScreenManager):
    pass

class PluginsListButton(ListItemButton):
    pass

class PluginsOutputListButton(ListItemButton):
    pass

class OverviewListButton(ListItemButton):
    pass

class Listview(ListView):
    pass

class MainWindow(GridLayout):
    student_list = ObjectProperty()
    manager = ObjectProperty()
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
                if type(res) == collections.Counter:
                    for k in res:
                        tData.append(k+": "+str(res[k]))
                else:
                    for k in res:
                        tData.append(k)
                self.outData = tData

    def fetchData(self):
        profiles = core.doReadProfiles()
        print(profiles)
        regions = core.doReadRegions()
        resources = core.doReadResources()

        tReg = len(regions)

        for p in profiles:
            for region in regions:
                count = 1
                self.pop_up.value = 0
                self.pop_up.update_pop_up_text('Current Region: '+str(region)+" ("+str(count)+"/"+str(tReg)+")")
                session = boto3.Session(profile_name=p, region_name=region)
                resEc2 = {}
                resEbs = {}
                core.doCollectResources(session, region, resources)
                self.pop_up.update_pop_up_info('Collecting Resources')
                self.pop_up.setValue(20)

                #
                # Information Gathering
                #

                # ec2Data
                currInst = core.doFindEC2Information(session, region)
                self.pop_up.update_pop_up_info('Collecting EC2 instances')
                self.pop_up.setValue(40)
                resEc2[region] = currInst
                ec2Data.append(resEc2)

                # s3Data
                s3Data = core.doFindS3Information(session, region)
                self.pop_up.update_pop_up_info('Collecting S3 buckets')
                self.pop_up.setValue(60)

                # volData
                currVol = core.doFindEBSInformation(session, region)
                self.pop_up.update_pop_up_info('Collecting EBS volumes')
                self.pop_up.setValue(80)
                resEbs[region] = currVol
                ebsData.append(resEbs)
                count += 1
        pluginManager.doRunPlugins(ec2Data, s3Data, ebsData, resources)
        self.pop_up.update_pop_up_text("Complete!")
        self.pop_up.setValue(100)
        self.pop_up.update_pop_up_info("")
        self.pop_up.dismiss()
        FetchedFlag == True
        print(ec2Data)
        print("ebsdata")
        print(ebsData)

    def doSnapshot(self):
        with open('ec2data.json', 'w') as outfile:
            json.dump(ec2Data, outfile)

        with open('ebsdata.json', 'w') as outfile:
            json.dump(ebsData, outfile)

        with open('s3data.json', 'w') as outfile:
            json.dump(s3Data, outfile)

    def fetchButton(self):
        self.show_popup()
        mythread = threading.Thread(target=self.fetchData)
        mythread.start()

    def show_popup(self):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text('Connecting...')
        self.pop_up.open()

class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    pop_up_info = ObjectProperty()
    pb_value = NumericProperty(0)
    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message

    def update_pop_up_info(self, i_message):
        self.pop_up_info.text = i_message

    def setValue(self, val):
        self.pb_value = val

class PBar(ProgressBar):
    pb_value = NumericProperty(0)

    def setValue(self, val):
        self.pb_value.value = val


class AWSApp(App):
    def build(self):
        return MainWindow()

    def build_config(self, config):
        pass

