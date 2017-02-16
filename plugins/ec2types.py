#!/usr/bin/python3
import collections

def lambda_handler(e):
    ret = []
    count = collections.Counter()
    for i in e:
        curr = e[i]["Type"]
        print(curr)
        count[curr] += 1
        #ret.append(i + ":" +e[i]["Type"])
    return count
