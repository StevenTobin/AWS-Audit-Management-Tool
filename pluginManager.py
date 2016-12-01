#!/usr/bin/python3

import boto3
import json
import plugins
import importlib

def doRunPlugins(ec2, s3, ebs, resources):
    for p in resources["Plugins"]:
        m = importlib.import_module("plugins."+p)
        if "ec2" in p:
            m.lambda_handler(ec2)
        elif "s3" in p:
            m.lambda_handler(s3)
        elif "ebs" in p:
            m.lambda_handler(ebs)
