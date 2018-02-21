#!/usr/bin/env python
#
# This illustrates the call-flow required to complete an OAuth request
# against the discogs.com API, using the discogs_client libary.
# The script will download and save a single image and perform and
# an API search API as an example. See README.md for further documentation.

import discogs_client
from discogs_client.exceptions import HTTPError
import json
import time
# Your consumer key and consumer secret generated and provided by Discogs.
# See http://www.discogs.com/settings/developers . These credentials
# are assigned by application and remain static for the lifetime of your discogs
# application. the consumer details below were generated for the
# 'discogs-oauth-example' application.
# NOTE: these keys are typically kept SECRET. I have requested these for
# demonstration purposes.
consumer_key = 'vtdDEtmcNwrKeMLjxaLO'
consumer_secret = 'ntXYptNGBgvLJUsSoLMCwhgiAUrDZndt'

# A user-agent is required with Discogs API requests. Be sure to make your
# user-agent unique, or you may get a bad response.
user_agent = 'discogs_api_example/2.0'

# instantiate our discogs_client object.
discogsclient = discogs_client.Client(user_agent)

# prepare the client with our API consumer data.
discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()

#print ' == Request Token == '
#print '    * oauth_token        = {0}'.format(token)
#print '    * oauth_token_secret = {0}'.format(secret)
#print

# Prompt your user to "accept" the terms of your application. The application
# will act on behalf of their discogs.com account.
# If the user accepts, discogs displays a key to the user that is used for
# verification. The key is required in the 2nd phase of authentication.
print('Please browse to the following URL {0}'.format(url))

#accepted = 'n'
#while accepted.lower() == 'n':
#    print
#    accepted = input('Have you authorized me at {0} [y/n] :'.format(url))


# Waiting for user input. Here they must enter the verifier key that was
# provided at the unqiue URL generated above.
oauth_verifier = input('Verification code :')

try:
    access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
except HTTPError:
    print('Unable to authenticate.')
    exit()

# fetch the identity object for the current logged in user.
user = discogsclient.identity()

#print
#print ' == User =='
#print '    * username           = {0}'.format(user.username)
#print '    * name               = {0}'.format(user.name)
#print ' == Access Token =='
#print '    * oauth_token        = {0}'.format(access_token)
#print '    * oauth_token_secret = {0}'.format(access_secret)
print(' Authentication complete. Future requests will be signed with the above tokens.')

# With an active auth token, we're able to reuse the client object and request
# additional discogs authenticated endpoints, such as database search.
#search_results = discogsclient.search('House For All', type='release',
#        artist='Blunted Dummies')

#print '\n== Search results for release_title=House For All =='
#for release in search_results:
#    print '\n\t== discogs-id {id} =='.format(id=release.id)
#    print u'\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
#                                         in release.artists))
#    print u'\tTitle\t: {title}'.format(title=release.title)
#    print u'\tYear\t: {year}'.format(year=release.year)
#    print u'\tLabels\t: {label}'.format(label=','.join(label.name for label in
#                                        release.labels))
genres = ["jazz", "rock", "electronic", "pop", "reggae", "blues", 
          "folk, world, & country", "funk / soul", "hip-hop", "classical"]
countries = ["Indonesia", "Turkey", "Venezuela", "China"]
year_min = 1900
year_max = 2017
frame = {}
#maxwait = 0

for country in countries:
    frame.update({country:{}})
    for year in range(year_min,year_max):
        frame[country].update({year:{}})
        for genre in genres:
            start=time.clock()
            #a = frame[country][year]{year})
            #a = next(index for (index, d) in enumerate(lst) if d["name"] == "Tom")
            search_results = discogsclient.search(type='release', genre = genre, country = country, year = year)
            (frame[country][year]).update({genre:len(search_results)})
            print(country, year, genre, len(search_results))
            #frame[country].append(len(search_results))
            wait= time.clock()-start
            time.sleep(max(1.001-wait,1.001))            
    with open(country+'.json', 'w') as fp:
        json.dump(frame, fp, sort_keys=True, indent=4)
    frame.clear()



# You can reach into the Fetcher lib if you wish to used the wrapped requests
# library to download an image. The following example demonstrates this.
#image = search_results[0].images[0]['uri']
#content, resp = discogsclient._fetcher.fetch(None, 'GET', image,
#                headers={'User-agent': discogsclient.user_agent})

#print ' == API image request =='
#print '    * response status      = {0}'.format(resp)
#print '    * saving image to disk = {0}'.format(image.split('/')[-1])
#
#with open(image.split('/')[-1], 'w') as fh:
#fh.write(content)