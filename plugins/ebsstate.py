#!/usr/bin/python3

def lambda_handler(e):
    ret = []
    for r in e:
        for i in r:
            for inst in r[i]:
                if inst:
                    ret.append(r[i][inst]["State"])
    return ret
