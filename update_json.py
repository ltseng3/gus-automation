import json
import sys
import os
import subprocess
from textwrap import indent

# run via:
# python update_config <config_num> <protocol>

# updates a json file
def update(file_path, key, new_value):
    file = open(file_path, "r+")
    json_object = json.load(file)
    file.close()

    json_object[key] = new_value

    file = open(file_path, "w")
    json.dump(json_object, file, indent=4)
    # file.write(simplej)

    file.close()

# ensures number of replicas is 3 and sets the latencies of those replicas to correspond with the given leader
def updateLatencies3(file_path, leader):
    latencies = {
        'california': {
            'california': 0,
            'virginia': 72,
            'ireland': 151,
        },
        'virginia': {
            'california': 72,
            'virginia': 0,
            'ireland': 88
        },
        'ireland': {
            'california': 151,
            'virginia': 88,
            'ireland': 0
        }
    }

    file = open(file_path, "r+")
    json_object = json.load(file)
    file.close()

    newServerList = ["california", "virginia", "ireland"]

    json_object["server_names"] = newServerList

    if (leader == "virginia"):
        temp = latencies['virginia']['ireland']
        latencies['virginia']['ireland'] = latencies['california']['ireland']
        latencies['california']['ireland'] = temp
    elif (leader == "ireland"):
        temp = latencies['ireland']['virginia']
        latencies['ireland']['virginia'] = latencies['california']['virginia']
        latencies['california']['virginia'] = temp

    json_object["server_ping_latencies"] = latencies

    json_object["number_of_replicas"] = 3

    file = open(file_path, "w")
    json.dump(json_object, file, indent=4)

    file.close()

# ensures number of replicas is 5 and sets the latencies of those replicas to correspond with the given leader
def updateLatencies5(file_path, leader):
    latencies = {
        'california': {
            'california': 0,
            'virginia': 72,
            'ireland': 151,
            'oregon': 59,
            'japan': 113
        },
        'virginia': {
            'california': 72,
            'virginia': 0,
            'ireland': 88,
            'oregon': 93,
            'japan': 162
        },
        'ireland': {
            'california': 151,
            'virginia': 88,
            'ireland': 0,
            'oregon': 145,
            'japan': 220
        },
        'oregon': {
            'california': 59,
            'virginia': 93,
            'ireland': 145,
            'oregon': 0,
            'japan': 121
        },
        'japan': {
            'california': 113,
            'virginia': 162,
            'ireland': 220,
            'oregon': 121,
            'japan': 0
        }
    }

    file = open(file_path, "r+")
    json_object = json.load(file)
    file.close()

    newServerList = ["california", "virginia", "ireland", "oregon", "japan"]

    json_object["server_names"] = newServerList

    if (leader == "virginia"):
        temp = latencies['virginia']['ireland']
        latencies['virginia']['ireland'] = latencies['california']['ireland']
        latencies['california']['ireland'] = temp

        temp = latencies['virginia']['oregon']
        latencies['virginia']['oregon'] = latencies['california']['oregon']
        latencies['california']['oregon'] = temp

        temp = latencies['virginia']['japan']
        latencies['virginia']['japan'] = latencies['california']['japan']
        latencies['california']['japan'] = temp
    elif (leader == "ireland"):
        temp = latencies['ireland']['virginia']
        latencies['ireland']['virginia'] = latencies['california']['virginia']
        latencies['california']['virginia'] = temp

        temp = latencies['ireland']['oregon']
        latencies['ireland']['oregon'] = latencies['california']['oregon']
        latencies['california']['oregon'] = temp

        temp = latencies['ireland']['japan']
        latencies['ireland']['japan'] = latencies['california']['japan']
        latencies['california']['japan'] = temp
    elif (leader == "oregon"):
        temp = latencies['oregon']['virginia']
        latencies['oregon']['virginia'] = latencies['california']['virginia']
        latencies['california']['virginia'] = temp

        temp = latencies['oregon']['ireland']
        latencies['oregon']['ireland'] = latencies['california']['ireland']
        latencies['california']['ireland'] = temp

        temp = latencies['oregon']['japan']
        latencies['oregon']['japan'] = latencies['california']['japan']
        latencies['california']['japan'] = temp
    elif (leader == "japan"):
        temp = latencies['japan']['virginia']
        latencies['japan']['virginia'] = latencies['california']['virginia']
        latencies['california']['virginia'] = temp

        temp = latencies['japan']['ireland']
        latencies['japan']['ireland'] = latencies['california']['ireland']
        latencies['california']['ireland'] = temp

        temp = latencies['japan']['oregon']
        latencies['japan']['oregon'] = latencies['california']['oregon']
        latencies['california']['oregon'] = temp

    json_object["server_ping_latencies"] = latencies

    json_object["number_of_replicas"] = 5

    file = open(file_path, "w")
    json.dump(json_object, file, indent=4)

    file.close()
