#!/usr/bin/python3

import boto3
import configparser
import collections
import json

AWSCFG      = "~/.aws/"
PLUGINCFG   = "~/Project/"
PROFILES    = []
RESOURCES   = []


# Lists for collection of resources
INSTANCES   = []
BUCKETS     = []
VOLUMES     = []

def doReadProfiles():
    config = configparser.SafeConfigParser()
    config.read(AWSCFG + "credentials")
    for key in config:
        tkey = key.lower()
        PROFILES.append(tkey)

def doFindResources():
    pluginConfig = configparser.SafeConfigParser()
    pluginConfig.read(PLUGINCFG + "plugins.cfg")
    for pkey in pluginConfig:
        print("plug key:" +str(pkey))
        options = collections.defaultdict(dict)
        for option in pluginConfig[pkey]:
            options[pkey][option] = True

            # End up with a dictionary of dictionaries
            # {ec2: {instances: True}, {SecurityGroup: True}, {Volume: True}}
            # so we want information of ec2 instances, Security Groups and Volumes

    RESOURCES.append(options)


def doCollectResources(s):
    # TO-DO:    Read in RESOURCES to find out
    #           which are required. Each resource
    #           collection function under here will
    #           then be in a big if-else statement


    # Collect EC2 instances
    print("Collecting EC2 information...")
    ec2 = s.resource("ec2")
    for i in ec2.instances.all():
        inst = str(i)
        inst = inst[17:-2]
        INSTANCES.append(inst)

    # Collect EBS information
    print("Collecting EBS information...")
    for v in ec2.volumes.all():
        vol = str(v)
        vol = vol[15:-2]
        VOLUMES.append(vol)

    # Collect S3 Buckets
    print("Collecting S3 information...")
    s3 = s.resource("s3")
    for b in s3.buckets.all():
        BUCKETS.append(b.name)

def doFindEC2Information(s):
    ec2 = s.resource("ec2")
    ec2Data = {}
    for i in INSTANCES:
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

    print(ec2Data)
    return ec2Data

def doFindEBSInformation(s):
    ec2 = s.resource("ec2")
    volData = {}
    for i in VOLUMES:
        currVolume = ec2.Volume(i)
        volData[i] = {"State"           : str(currVolume.state),
                      "Tags"            : str(currVolume.tags),
                      "Size"            : str(currVolume.size),
                      "VolumeType"      : str(currVolume.volume_type),
                      "Encrypted"       : str(currVolume.encrypted),
                      "SnapshotId"      : str(currVolume.snapshot_id)
                      }

    print(volData)
    return volData

def doFindS3Information(s):
    s3 = s.resource("s3")
    s3Data = {}
    for b in BUCKETS:
        currBucket = s3.Bucket(name=b)
        s3Data[b] = {}

    print(s3Data)
    return s3Data


if __name__ == '__main__':
    doReadProfiles()
    for p in PROFILES:
        s = boto3.Session(profile_name=p)
        # TO-DO:    Figure out how this will work for
        #           more than one profile.

    #doFindResources()
    doCollectResources(s)

    #
    # Information Gathering
    #

    # ec2Data
    ec2Data = doFindEC2Information(s)

    # s3Data
    s3Data = doFindS3Information(s)

    # volData
    volData = doFindEBSInformation(s)
