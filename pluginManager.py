#!/usr/bin/python3

import boto3
import json
import plugins
import importlib

def doRunPlugins(ec2, s3, ebs):
    pluginsConf = doFindPlugins()
    pluginNames = []
    for p in pluginsConf["Plugins"]:
        m = importlib.import_module("plugins."+p)
        m.lambda_handler(ec2)

def doFindPlugins():
    pluginData = open("plugins.json").read()
    plugins = json.loads(pluginData)
    return plugins
