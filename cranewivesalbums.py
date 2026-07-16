from ytmusicapi import YTMusic
# the data interchange format to communicate with javascript
import json

ytmusic = YTMusic()

playlistItems = []
videoItems = []
videoDict = []

browseSingles = []
singleItems = []

# index 0 is LEE EMI, index 2 is The Crane Wives.
staticChannelsList = ['UClzs1UE_hLclY-Ln74FO7ZA', 'UCQ1ctrffvMbPct8cPOJL6xQ']

# this line should mean, after passing the 'channel' parameter for the 'channelId' field in 'artistQuery', all channels desired are scraped
# in sequence and then all mashed into the same json file.
for channel in staticChannelsList:

    # this line will get many details about the artist found (the crane wives is the given channel ID).
    artistQuery = ytmusic.get_artist(channelId = channel)
    print(artistQuery)
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
            # this variable will hold the name of the song alongside the video id, for stricter filtering.


            for song in videoItems:
                # for each videoId in a given playlist, assign a album name for javascript clarity later when seperating the entire array out. 
                videoDict.append({'album': albumTitle, 'id': song})

            # clear old videos for looping
            videoItems = []
    else:
        print("The key " + key + " is not present in the dictionary, therefore no albums are assumed for this channel.")

    key = "singles"    
    if key in artistQuery.keys():
        key2 = 'params'
        #  the 'params' key does not always appear, so this is a neccessity if a user has < 10 items for singles. If < 10 is the case, then there should be no params and the 'else' block runs.
        if key2 in artistQuery['singles'].keys():

            # unlike albums, singles do not recieve values for 'audioPlaylistId'. Therefore, the browseId needs to be gathered and then passed to
            # 'get_artist_albums' which, despite the name, also functions for singles.
            singlesId = artistQuery['singles']['browseId']
            singlesParam = artistQuery['singles']['params']

            singlesQuery = ytmusic.get_artist_albums(
                channelId= singlesId,
                params= singlesParam
            )

            for playlist in singlesQuery:
                singlesQuery2 = ytmusic.get_playlist(
                    playlistId= playlist['playlistId']
                )

                # the video id property after running the get_playlist request is underneath tracks -> videoId. Then, the singleItems playlist will
                # populate with all video IDs present in the current playlist
                for entry in singlesQuery2['tracks']:
                    singleItems.append(entry['videoId'])
        else:

            # this code should run for artists that do not have a 'param' key under 'singles'. This should occur when they have < 10 items, such as 
            # LEE EMI.
            for single in artistQuery['singles']['results']:
                album = ytmusic.get_album(
                    single['browseId']
                )

                for track in album['tracks']:
                    singleItems.append(track['videoId'])
            
            # clear old single browse ids for looping
            browseSingles = []
    else:
        print("The key " + key + " is not present in the dictionary, therefore no singles are assumed for this channel.")

# the premise of this code is that if a video id is present in the mainarray (albums), it should be fully removed from the secondarray (singles) if it 
# is also present there. mainarray should be an array with each index having a dictionary with keys 'album' and 'id', whilst secondarray
# is a regular array with single string video ids at each index.
for entry in videoDict:
    videoid = entry['id']
    # this finds the amount (as an int) of videoids that appear in the singles list that also appeared in the albums array.
    x = singleItems.count(videoid)
    # this for loop is necessary, because 'remove()' only gets rid of the first instance of an entry, and we want all entries gone.
    for i in range(x):
        singleItems.remove(videoid)


# write album-connected songs to the .json file in root
with open('./albums.json', 'w') as f:
    json.dump(videoDict, f)

# write singles to the .json file in root
with open('./singles.json', 'w') as f:
    json.dump(singleItems, f)

#print(videoDict)
#print('')
#print(len(videoDict))
