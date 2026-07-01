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

print(api_key)

def get_releases_tab_videos():
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_ids = []
    next_page_token = None

    print("Searching for all music releases...")

    while True:
        # We use search.list to find all 'video' types for this channel
        # We filter by videoCategoryId='10' (Music) to target the songs
        search_request = youtube.search().list(
            part='snippet',
            channelId='UCQ1ctrffvMbPct8cPOJL6xQ',
            type='video',
            videoCategoryId='10', # 10 is the ID for Music
            maxResults=50,
            pageToken=next_page_token,
            order='date' # Gets newest releases first
        ).execute()

        for item in search_request.get('items', []):
            video_ids.append(item['id']['videoId'])

        next_page_token = search_request.get('nextPageToken')
        
        # Stop if there are no more pages
        if not next_page_token:
            break
    
    # write video IDs to the .json file in root
    with open('./videos.json', 'w') as f:
        json.dump(video_ids, f)

    return video_ids

# Run the script
all_songs = get_releases_tab_videos()
print(f"\nFound {len(all_songs)} songs from the music/releases category.")
print(all_songs)
    






