#!/usr/bin/python3
import collections

def lambda_handler(e):
    count = collections.Counter()
    for i in e:
        count[e[i]["Encrypted"]] += 1
    return count