# access library for google functions, particularly 'build' which will specify the google application (youtube)
from googleapiclient.discovery import build
# this library enbles environment files (e.x. setting an invisible api key)
from dotenv import load_dotenv
# this module allows python to access external files (.env)
import os

from ytmusicapi import YTMusic
# the data interchange format to communicate with javascript
import json

ytmusic = YTMusic()

# Loads variables from .env
load_dotenv()  

playlistArray = []
videoItems = []

#browseArray = ['MPREb_ARlR8h0EIdL', 'MPREb_tLns0Q1MnPh', 'MPREb_19AKYQEfSHP', 'MPREb_1BHpLSz743D', 'MPREb_HGwAhma5gSs', 'MPREb_Yp0371DVot9', 'MPREb_qryiUfEzBni', 'MPREb_JgEtzmGEMki', 'MPREb_NHLMzSOh8Gt', 'MPREb_hKF5U5t6Rsn']
singlesparam = 'ggMCCAI%3D'
singlesid = 'MPADUCoPTtb6E_Z6J7gVa6E8Z_Jw'

query = ytmusic.get_artist_albums(
    channelId=singlesid,
    params=singlesparam
)

for playlist in query:
    playlistArray.append(playlist['playlistId'])

for playlist_id in playlistArray:
    query2 = ytmusic.get_playlist(
            playlistId = playlist_id
        )

    # the video id property after running the get_playlist request is underneath tracks -> videoId. Then, the videItems playlist will
    # populate with all video IDs present in the current playlist
    for entry in query2['tracks']:
        videoItems.append(entry['videoId'])

print(videoItems)

# write video IDs to the .json file in root
with open('./singles.json', 'w') as f:
    json.dump(videoItems, f)





