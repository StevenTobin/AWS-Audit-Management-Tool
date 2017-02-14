#!/usr/bin/python3

def lambda_handler(e):
    total = 0
    ret = []
    for i in e:
        total += int(e[i]["Size"])
    ret.append(str(total))
