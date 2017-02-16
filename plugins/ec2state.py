#!/usr/bin/python3
import collections

def lambda_handler(e):
    ret = []
    count = collections.Counter()
    for i in e:
        count[e[i]["State"]] += 1
        #ret.append(e[i]["State"])
    return count