#!/usr/bin/python3

import boto3
ec2 = boto3.resource('ec2')
ec2.create_instances(ImageId='ami-9398d3e0', InstanceType="t2.micro", MinCount=1, MaxCount=2)
