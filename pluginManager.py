#!/usr/bin/python3

import boto3
import json
import plugins
import importlib


ec2PlugOutput = {}
s3PlugOutput = {}
ebsPlugOutput = {}

def doRunPlugins(ec2, s3, ebs, resources):
    for p in resources["Plugins"]:
        m = importlib.import_module("plugins."+p)
        if "ec2" in p:
            currPlugin = m.lambda_handler(ec2)
            ec2PlugOutput[p] = currPlugin
        elif "s3" in p:
            currPlugin = m.lambda_handler(s3)
            s3PlugOutput[p] = currPlugin
        elif "ebs" in p:
            currPlugin = m.lambda_handler(ebs)
            ebsPlugOutput[p] = currPlugin

def getEc2Plugs():
    ec2 = []
    for k in ec2PlugOutput.keys():
        ec2.append(ec2PlugOutput[k])
    print(ec2)
    return ec2

def getS3Plugs():
    s3 = []
    for k in s3PlugOutput.keys():
        s3.append(s3PlugOutput[k])
    print(s3)
    return s3

def getEbsPlugs():
    ebs = []
    for k in ebsPlugOutput.keys():
        ebs.append(ebsPlugOutput[k])
    print(ebs)
    return ebs

