#!/usr/bin/python3
import collections

def lambda_handler(e):
    count = collections.Counter()
    for i in e:
        count[e[i]["SubnetID"]] += 1
    return count