#!/usr/bin/python3
import collections

def lambda_handler(e):
    ret = []
    count = collections.Counter()
    for r in e:
        for i in r:
            for inst in r[i]:
                if inst:
                    curr = r[i][inst]["Type"]
                    count[curr] += 1
    return count
