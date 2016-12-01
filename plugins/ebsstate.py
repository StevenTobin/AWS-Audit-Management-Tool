#!/usr/bin/python3

def lambda_handler(e):
    for i in e:
        print(e[i]["State"])
