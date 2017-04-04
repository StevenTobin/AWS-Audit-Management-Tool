#!/usr/bin/python3

def lambda_handler(e):
    total = 0
    for r in e:
        for i in r:
            for inst in r[i]:
                if inst:
                    total += int(r[i][inst]["Size"])
    return str(total)
