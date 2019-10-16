#!/bin/python3

import json
from operator import itemgetter

json_file1 = open('res/followed.json')
followed = json.load(json_file1)
json_file = open('magic_book.json')
data = json.load(json_file)


def json_parser_fake():
    parsed = list()
    for x in data['following']:
        parsed.append(x['url'])
    return parsed


following_list = json_parser_fake()
print(data['following'])

for x in data['following']:
    print(x)
    followed['followed'].append({
        'url': x['url']
    })

with open('res/followed.json', 'w') as outfile:
    json.dump(followed, outfile)
