#!/usr/bin/python3

import boto3
ec2 = boto3.resource('ec2')
for i in ec2.instances.all():
    i.terminate()
for i in ec2.volumes.all():
    i.delete()
