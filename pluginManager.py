#!/usr/bin/python3

import boto3
import json
import plugins
import importlib


#
# Dictionaries for plugin output
#
ec2PlugOutput = {}
s3PlugOutput = {}
ebsPlugOutput = {}

#
# Lists for informational functions
#
plugs = []
services = []

# Import the plugins that we are configured to run
#   gather the output and store the output in the
#   correct list
def doRunPlugins(ec2, s3, ebs, resources):
    for p in resources["Plugins"]:
        try:
            m = importlib.import_module("plugins."+p)
        except:
            print("Failed import : plugins."+str(p))
            continue
        if "ec2_" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(ec2)
            ec2PlugOutput[p] = currPlugin
            plugs.append(p)
        elif "s3_" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(s3)
            s3PlugOutput[p] = currPlugin
            plugs.append(p)
        elif "ebs_" in p and resources["Plugins"][p] == True:
            currPlugin = m.lambda_handler(ebs)
            ebsPlugOutput[p] = currPlugin
            plugs.append(p)
    for s in resources["Resources"]:
        if resources["Resources"][s] == True:
            services.append(s)

# Return the EC2 plugin outputs
def getEc2Plugs():
    return ec2PlugOutput

# Return the S3 plugins outputs
def getS3Plugs():
    return s3PlugOutput

# Return the EBS plugins outputs
def getEbsPlugs():
    return ebsPlugOutput

# Return the list of configured plugins
def getConfiguredPlugins():
    return plugs

# Returnt the list of configured services
def getConfiguredServices():
    return services

