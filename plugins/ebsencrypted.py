#!/usr/bin/python3
import collections

def lambda_handler(e):
    count = collections.Counter()
    for r in e:
        for i in r:
            for inst in r[i]:
                if inst:
                    count[r[i][inst]["Encrypted"]] += 1
    return count