#!/usr/bin/python3

import boto3
import json
import plugins
import importlib

ec2PlugOutput = {}
s3PlugOutput = {}
ebsPlugOutput = {}

plugs = []
services = []

def doRunPlugins(ec2, s3, ebs, resources):
    for p in resources["Plugins"]:
        try:
            m = importlib.import_module("plugins."+p)
        except:
            print("Failed import : plugins."+str(p))
            continue
        if "ec2" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(ec2)
            #ec2PlugOutput["PluginName"] = p
            ec2PlugOutput[p] = currPlugin
            plugs.append(p)
        elif "s3" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(s3)
            #s3PlugOutput["PluginName"] = p
            s3PlugOutput[p] = currPlugin
            plugs.append(p)
        elif "ebs" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(ebs)
            #ebsPlugOutput["PluginName"] = p
            ebsPlugOutput[p] = currPlugin
            plugs.append(p)
    for s in resources["Resources"]:
        if resources["Resources"][s] == True:
            services.append(s)

def getEc2Plugs():
    return ec2PlugOutput

def getS3Plugs():
    return s3PlugOutput

def getEbsPlugs():
    ebs = []
    for k in ebsPlugOutput.keys():
        ebs.append(ebsPlugOutput[k])
    return ebs

def getConfiguredPlugins():
    return plugs

def getConfiguredServices():
    return services

