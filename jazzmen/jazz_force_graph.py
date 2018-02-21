# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 20:34:27 2018

@author: Maks
"""

import discogs_client
from discogs_client.exceptions import HTTPError 
import json
import time

consumer_key = 'vtdDEtmcNwrKeMLjxaLO'
consumer_secret = 'ntXYptNGBgvLJUsSoLMCwhgiAUrDZndt'
user_agent = 'discogs_api_example/2.0'

discogsclient = discogs_client.Client(user_agent)
discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()

print('Please browse to the following URL {0}'.format(url))

oauth_verifier = input('Verification code :')

try:
    access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
except HTTPError:
    print('Unable to authenticate.')
    exit()

user = discogsclient.identity()
print(' Authentication complete. Future requests will be signed with the above tokens.')

fname = 'jazzmen.txt'
nodes = []
links = []

with open(fname) as f:
    jazzmen = f.readlines()
jazzmen = [x.strip('\n') for x in jazzmen]
#print(jazzmen)
for i in jazzmen:
    node = {"name": i}
    nodes.append(node)
print(nodes)
for i in range(len(jazzmen)):
    for j in range(i+1,len(jazzmen)):
        link = {"source": i, "target": j, "value": 0}
        links.append(link)
for i in links:
    start=time.clock()
    search_results = discogsclient.search(type='master', credit = (i["source"],i["target"]))
    i["value"]=len(search_results)
    wait= time.clock()-start
    time.sleep(max(1.001-wait,1.001))    
    print(i)
    
json_prep = {"nodes":nodes, "links":links}
json_dump = json.dumps(json_prep, indent=1, sort_keys=True)
print(json_dump)
filename_out = 'jazzmen.json'
json_out = open(filename_out,'w')
json_out.write(json_dump)
json_out.close()