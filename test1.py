#!/bin/python3

import json
from datetime import datetime

days = 0


dateformat = "%Y-%m-%d"
today = datetime.now()


def datecmp(date_input):
    d = datetime.strptime(date_input, dateformat)
    nd = today - d
    return nd.days >= days


with open('tt') as json_file:
    data = json.load(json_file)
    print(data)
    i = 0
    while i < len(data['following']):
        if datecmp(data['following'][i]['date']):
            del data['following'][i]
            i -= 1
        i += 1
    print(data)
with open('tt', 'w') as outfile:
    json.dump(data, outfile)
