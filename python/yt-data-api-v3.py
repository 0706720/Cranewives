# access library for google functions, particularly 'build' which will specify the google application (youtube)
from googleapiclient.discovery import build
# this library enbles environment files (e.x. setting an invisible api key)
from dotenv import load_dotenv
# this module allows python to access external files (.env)
import os
# the data interchange format to communicate with javascript
import json

# Loads variables from .env
load_dotenv()  

api_key = os.getenv("API_KEY")
playlistArray = []

youtube = build('youtube', 'v3', developerKey=api_key)

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId='PLat0VcCHprJb1O8CpOBmdvhhNeLwXNqgZ',
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response =pl_request.execute()

    vid_ids = []

    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
        #print(vid_ids)
        #print()

    vid_request = youtube.videos().list(
        part='contentDetails',
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        print(duration)
        print()
    
    # the first time the while loop runs, it will have 50 entries in the vid_ids array. these vids can be assigned individually to the main 
    # array, where they will be stored until all pages are eventually completed (e.g. a playlist has 102 entries. The loop will run 3 times 
    # because there is a max of 50 video entries per page, and the playlistArray will need updating 3 times overall).
    for vid in vid_ids:
        playlistArray.append(vid)

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break


# write video IDs to the .json file in root
with open('./videos.json', 'w') as f:
    json.dump(playlistArray, f)

print(len(playlistArray))








