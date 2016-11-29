#!/usr/bin/python3

import boto3
import json

def doRunPlugins(ec2, s3, ebs):
    plugins = doFindPlugins()
    for p in plugins["Plugins"]:
        with open("plugins/"+p+".py") as f:
            code = compile(f.read(), "plugins/ec2types/py", 'exec')
            exec(code)

def doFindPlugins():
    pluginData = open("plugins.json").read()
    plugins = json.loads(pluginData)
    print(plugins["Plugins"])
    return plugins
