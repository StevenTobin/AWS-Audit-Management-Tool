#!/usr/bin/python3

import boto3
import configparser
import json
import pluginManager
import sys
import AWSApp

AWSCFG      = "~/.aws/"
PROFILES    = []
RESOURCES   = ""
REGIONS = []

#
# Lists for collection of resources
#
EC2INSTANCES   = []
S3BUCKETS     = []
EBSVOLUMES     = []

# Read the credentials file
def doReadProfiles():
    config = configparser.ConfigParser()
    config.read(AWSCFG + "credentials")
    for key in config:
        tkey = key.lower()
        PROFILES.append(tkey)
    return PROFILES

# Read the plugin configuration file
def doReadResources():
    pluginData = open("plugins.json").read()
    RESOURCES = json.loads(pluginData)
    return RESOURCES

# Find AWS regions
def doReadRegions():
    if len(REGIONS) == 0:
        client = boto3.client('ec2')
        for region in client.describe_regions()['Regions']:
            # This should allow the tool to automatically keep itself
            # up to date with new regions
            REGIONS.append(region["RegionName"])
        return REGIONS
    else:
        return REGIONS

# Collect the instance ids of provisioned infrastructure so we can use them
# later to collect more detailed information
def doCollectResources(s, region, RESOURCES):
    for res in RESOURCES["Resources"]:
        if "ec2" in res:
            ec2l=[]
            reg ={}
            # Collect EC2 instances
            ec2 = s.resource("ec2")
            for i in ec2.instances.all():
                inst = str(i)
                # cut so we only end up with the instance id
                inst = inst[17:-2]
                ec2l.append(inst)
            reg[region] = ec2l
            EC2INSTANCES.append(reg)
        if "ebs" in res:
            # Collect EBS information
            ec2 = s.resource("ec2")
            ebsl=[]
            reg={}
            for v in ec2.volumes.all():
                vol = str(v)
                # cut so we only end up with the volume id
                vol = vol[15:-2]
                ebsl.append(vol)
            reg[region] = ebsl
            EBSVOLUMES.append(reg)
        if "s3" in res:
            # Collect S3 Buckets
            s3 = s.resource("s3")
            for b in s3.buckets.all():
                name = b.name
                S3BUCKETS.append(b.name)

# Collect the ec2 information we want
def doFindEC2Information(s, region):
    ec2 = s.resource("ec2")
    ec2Data = {}
    for instances in EC2INSTANCES:
        if region in instances:
            for id in instances[region]:
                currInstance = ec2.Instance(id=id)
                ec2Data[id] = {"Type"            : str(currInstance.instance_type),
                              "State"           : str(currInstance.state),
                              "SecurityGroup"   : str(currInstance.security_groups),
                              "PrivateIP"       : str(currInstance.private_ip_address),
                              "VPC"             : str(currInstance.vpc_id),
                              "SubnetID"        : str(currInstance.subnet_id),
                              "PublicDNS"       : str(currInstance.public_dns_name),
                              "PrivateDNS"      : str(currInstance.private_dns_name),
                              "IAM"             : str(currInstance.iam_instance_profile),
                              "KeyName"         : str(currInstance.key_name),
                              "Placement"       : str(currInstance.placement),
                              "Tags"            : str(currInstance.tags)
                              }
    return ec2Data

# Collect the EBS information we want
def doFindEBSInformation(s, region):
    ec2 = s.resource("ec2")
    volData = {}
    for instances in EBSVOLUMES:
        if region in instances:
            for id in instances[region]:
                currVolume = ec2.Volume(id)
                volData[id] = {"State"           : str(currVolume.state),
                              "Tags"            : str(currVolume.tags),
                              "Size"            : str(currVolume.size),
                              "VolumeType"      : str(currVolume.volume_type),
                              "Encrypted"       : str(currVolume.encrypted),
                              "SnapshotId"      : str(currVolume.snapshot_id)
                              }
    return volData

# Collect the S3 information we want
def doFindS3Information(s):
    s3 = s.resource("s3")
    s3Data = {}
    for b in S3BUCKETS:
        currBucket = s3.Bucket(name=b)
        s3Data[b] = {"Name" : str(currBucket.name)}
    return s3Data

# Get the regions we found and return them if anything else
#   needs them
def doGetRegions():
    reg = []
    for r in REGIONS:
        reg.append(r)
    return reg

if __name__ == '__main__':
    sys.path.append('/plugins/')
    doReadProfiles()
    doReadRegions()
    RESOURCES = doReadResources()
    AWSApp.AWSApp().run()
