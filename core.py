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


# Lists for collection of resources
EC2INSTANCES   = []
S3BUCKETS     = []
EBSVOLUMES     = []

def doReadProfiles():
    config = configparser.ConfigParser()
    config.read(AWSCFG + "credentials")
    for key in config:
        tkey = key.lower()
        PROFILES.append(tkey)

def doFindResources():
    pluginData = open("plugins.json").read()
    RESOURCES = json.loads(pluginData)
    return RESOURCES

def doCollectResources(s):
    for res in RESOURCES["Resources"]:
        if "ec2" in res:
            # Collect EC2 instances
            print("Collecting EC2 information...")
            ec2 = s.resource("ec2")
            for i in ec2.instances.all():
                inst = str(i)
                inst = inst[17:-2]
                EC2INSTANCES.append(inst)
        if "ebs" in res:
            # Collect EBS information
            print("Collecting EBS information...")
            ec2 = s.resource("ec2")
            for v in ec2.volumes.all():
                vol = str(v)
                vol = vol[15:-2]
                EBSVOLUMES.append(vol)
        if "s3" in res:
            # Collect S3 Buckets
            print("Collecting S3 information...")
            s3 = s.resource("s3")
            for b in s3.buckets.all():
                S3BUCKETS.append(b.name)

def doFindEC2Information(s):
    ec2 = s.resource("ec2")
    ec2Data = {}
    for i in EC2INSTANCES:
        currInstance = ec2.Instance(id=i)
        ec2Data[i] = {"Type"            : str(currInstance.instance_type),
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

def doFindEBSInformation(s):
    ec2 = s.resource("ec2")
    volData = {}
    for i in EBSVOLUMES:
        currVolume = ec2.Volume(i)
        volData[i] = {"State"           : str(currVolume.state),
                      "Tags"            : str(currVolume.tags),
                      "Size"            : str(currVolume.size),
                      "VolumeType"      : str(currVolume.volume_type),
                      "Encrypted"       : str(currVolume.encrypted),
                      "SnapshotId"      : str(currVolume.snapshot_id)
                      }

    return volData

def doFindS3Information(s):
    s3 = s.resource("s3")
    s3Data = {}
    for b in S3BUCKETS:
        currBucket = s3.Bucket(name=b)
        s3Data[b] = {}

    return s3Data


if __name__ == '__main__':
    sys.path.append('/plugins/')
    doReadProfiles()
    for p in PROFILES:
        session = boto3.Session(profile_name=p)
        # TO-DO:    Figure out how this will work for
        #           more than one profile.

    RESOURCES = doFindResources()
    doCollectResources(session)

    #
    # Information Gathering
    #

    # ec2Data
    ec2Data = doFindEC2Information(session)

    # s3Data
    s3Data = doFindS3Information(session)

    # volData
    volData = doFindEBSInformation(session)

    #
    # Plugins
    #
    print("Plugins----------------")
    pluginManager.doRunPlugins(ec2Data, s3Data, volData, RESOURCES)

    AWSApp.AWSApp().run()
