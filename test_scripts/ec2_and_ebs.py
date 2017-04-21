#!/usr/bin/python3
import boto3
from random import randint

regions = []
client = boto3.client('ec2')
for region in client.describe_regions()['Regions']:
    regions.append(region["RegionName"])

amis= {}


amis['us-east-1']      = "ami-c58c1dd3"
amis['us-east-2']      = "ami-4191b524"
amis['us-west-2']      = "ami-4836a428"
amis['us-west-1']      = "ami-7a85a01a"
amis['ca-central-1']   = "ami-0bd66a6f"
amis['eu-west-1']      = "ami-01ccc867"
amis['eu-west-2']      = "ami-b6daced2"
amis['eu-central-1']   = "ami-b968bad6"
amis['ap-southeast-1'] = "ami-fc5ae39f"
amis['ap-northeast-2'] = "ami-9d15c7f3"
amis['ap-northeast-1'] = "ami-923d12f5"
amis['ap-southeast-2'] = "ami-162c2575"
amis['ap-south-1']     = "ami-52c7b43d"
amis['sa-east-1']      = "ami-37cfad5b"




for reg in regions:
    s = boto3.Session(profile_name='default', region_name=reg)
    ec2 = s.resource('ec2')
    count = randint(0,10)
    print("Creating instances in "+ str(reg))
    ec2.create_instances(ImageId=amis[reg], InstanceType="t2.micro", MinCount=count, MaxCount=count)
