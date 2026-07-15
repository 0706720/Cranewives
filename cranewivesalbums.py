from ytmusicapi import YTMusic
# the data interchange format to communicate with javascript
import json

ytmusic = YTMusic()

playlistItems = []
videoItems = []
videoDict = []

browseSingles = []

# index 0 is LEE EMI, index 2 is The Crane Wives.
staticChannelsList = ['UClzs1UE_hLclY-Ln74FO7ZA', 'UCQ1ctrffvMbPct8cPOJL6xQ']

# this line should mean, after passing the 'channel' parameter for the 'channelId' field in 'artistQuery', all channels desired are scraped
# in sequence and then all mashed into the same json file.
for channel in staticChannelsList:

    # this line will get many details about the artist found (the crane wives is the given channel ID).
    artistQuery = ytmusic.get_artist(channelId = channel)
    #print(artistQuery)
    #print('')

    # the below two lines will check if the 'albums' key was found within the query. If not, it implies the channel doesn't have any albums and
    # therefore the playlist iterating is redundant, the code is skipped.
    key = "albums"
    if key in artistQuery.keys():
        # add a link for each playlist ID found within the album section of the given channel.
        for link in artistQuery['albums']['results']:
            playlistItems.append(link['audioPlaylistId'])

        for playlist_id in playlistItems:
            query2 = ytmusic.get_playlist(
                playlistId = playlist_id
            )

            # the video id property after running the get_playlist request is underneath tracks -> videoId. Then, the videItems playlist will
            # populate with all video IDs present in the current playlist
            for entry in query2['tracks']:
                videoItems.append(entry['videoId'])

            # this variable will get the common album name that all songs share within the same playlist
            albumTitle = query2['title']

            for song in videoItems:
                # for each videoId in a given playlist, assign a album name for javascript clarity later when seperating the entire array out. 
                videoDict.append({'album': albumTitle, 'id': song})

            # clear old videos for looping
            videoItems = []
    else:
        print("The key " + key + " is not present in the dictionary, therefore no albums are assumed for this channel.")

    key = "singles"    
    if key in artistQuery.keys():
        for browseID in artistQuery['singles']:
            browseSingles.append(browseID['browseId'])
            print(browseSingles)
        
        # clear old single browse ids for looping
        browseSingles = []
    else:
        print("The key " + key + " is not present in the dictionary, therefore no singles are assumed for this channel.")




# write video IDs to the .json file in root
with open('./albums.json', 'w') as f:
    json.dump(videoDict, f)

#print(videoDict)
#print('')
#print(len(videoDict))
