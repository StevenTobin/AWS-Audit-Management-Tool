#!/usr/bin/python3
import collections

def lambda_handler(e):
    count = collections.Counter()
    for region in e:
        for instances in region:
            for inst in region[instances]:
                if inst:
                    count[region[instances][inst]["State"]] += 1

    return count