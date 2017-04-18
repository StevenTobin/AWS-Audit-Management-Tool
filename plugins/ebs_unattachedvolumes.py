#!/usr/bin/python3
import collections

def lambda_handler(e):
    res = []
    for region in e:
        for instances in region:
            for inst in region[instances]:
                if inst:
                    if region[instances][inst]["State"] == "available":
                        res.append(str(region) + ": " + str(inst))

    return res
