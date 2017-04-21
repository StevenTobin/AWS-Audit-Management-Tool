#!/usr/bin/python3

import boto3

regions = []
client = boto3.client('ec2')
for region in client.describe_regions()['Regions']:
    regions.append(region["RegionName"])

for reg in regions:
    s = boto3.Session(profile_name='default', region_name=reg)
    ec2 = s.resource('ec2')
    print("Deleting instances in "+str(reg))
    try:
        for i in ec2.instances.all():
            i.terminate()
    except:
        pass

    try:
        for i in ec2.volumes.all():
            i.delete()
    except:
        pass




