# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 16:17:24 2017

@author: Maks
"""

import pylast
import json

API_KEY = "3bed9b9afbfaa4e4cf3e5b79ef3c462b"
API_SECRET = "849b4b87e7ecb3785ddac42dc20fb647"

lastfm_network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

genres = ["jazz", "rock", "electronic", "pop", "reggae", "blues", 
          "folk", "soul", "hip-hop", "classical"]

frame={}
for genre in genres:
    listeners_sum = 0
    tag = lastfm_network.get_tag(genre)
    for item in tag.get_top_artists(100):
        print(item[0])
        artist = lastfm_network.get_artist(item[0])
        listeners_sum+=artist.get_listener_count()
        #scrobbles_sum+=artist.get_playcount()
    print(genre, listeners_sum)
    frame.update({genre:listeners_sum})
with open('lastfm.json', 'w') as fp:
    json.dump(frame, fp, sort_keys=True, indent=4)
    
#print(scrobbles_sum)
#print("Listeners:", artist.get_listener_count())
#print("Scrobbles:", artist.get_playcount())