#!/usr/bin/python3

def lambda_handler(e):
    ret = []
    for i in e:
        ret.append(i + ":" +e[i]["Type"])
    return ret
