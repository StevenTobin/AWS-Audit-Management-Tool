#!/usr/bin/python3

def lambda_handler(e):
    total = 0
    for region in e:
        for instances in region:
            for inst in region[instances]:
                if inst:
                    total += int(region[instances][inst]["Size"])
    return total
