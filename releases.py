# access library for google functions, particularly 'build' which will specify the google application (youtube)
from googleapiclient.discovery import build
# this library enbles environment files (e.x. setting an invisible api key)
from dotenv import load_dotenv
# this module allows python to access external files (.env)
import os

from ytmusicapi import YTMusic
# the data interchange format to communicate with javascript
import json

videoDict = [{'album': 'x', 'id': 'c'}]
singleItems = ['a', 'a', 'b', 'a', 'c', 'd']


# the below logic will remove duplicates from appearing in the singles array that already.
for entry in videoDict:
    videoid = entry['id']
    x = singleItems.count(videoid)
    for i in range(x):
        singleItems.remove(videoid)

print(singleItems)







