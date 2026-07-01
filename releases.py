# access library for google functions, particularly 'build' which will specify the google application (youtube)
from googleapiclient.discovery import build
# this library enbles environment files (e.x. setting an invisible api key)
from dotenv import load_dotenv
# this module allows python to access external files (.env)
import os
# the data interchange format to communicate with javascript
import json
import requests
import re


# Loads variables from .env
load_dotenv()  

api_key = os.getenv("API_KEY")
playlistArray = []

url = "https://www.youtube.com/@thecranewives/releases"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
    )
}

html = requests.get(url, headers=headers).text

match = re.search(r'var ytInitialData = ', html)

decoder = json.JSONDecoder()
yt_data, _ = decoder.raw_decode(html[match.end():])
with open("./releases.json", "w", encoding="utf-8") as f:
    json.dump(yt_data, f, indent=2)

def find_releases(jsondata)
       if "playlistId" in obj:

find_releases(yt_data)


