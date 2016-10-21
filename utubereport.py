#!/usr/bin/env python

import logging
import sys
import requests

def getchannel ( channelId, api_key ):
    "Grab channel playlists ID for channelId"
    print channelId
    print api_key
    url = "https://www.googleapis.com/youtube/v3/playlists?part=contentDetails&channelId=%s&key=%s" % (channelId,api_key)
    r = requests.get(url)
    return r.json();






api_key = "AIzaSyCyZkQCo-lrj4fbRqY6o21fSgBPhATUjog"
channelId = "UCKON30YeSGIeqsueMYgEa9A"

print getchannel(channelId,api_key)
