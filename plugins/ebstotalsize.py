#!/usr/bin/python3

def lambda_handler(e):
    total = 0
    for i in e:
        total += int(e[i]["Size"])
    print("Total EBS Size: " +str(total))
