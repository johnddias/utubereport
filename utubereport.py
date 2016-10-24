#!/usr/bin/env python

import logging
import sys
import requests
import argparse

def getchannel ( channelId, api_key ):
    "Grab channel playlists ID for channelId"
    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&key=%s" % (channelId,api_key)
    r = requests.get(url)
    page = r.json()
    playlists = page["items"]
    nResults = page["pageInfo"]["totalResults"]
    resultsPerPage = page["pageInfo"]["resultsPerPage"]
    nPages = ((int(nResults) / int(resultsPerPage))) + ((int(nResults)) % (int(resultsPerPage)) > 0)
    n = 1
    if nPages > 1:
        while (n < nPages):
            pageToken = page["nextPageToken"]
            url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&key=%s&pageToken=%s" % (channelId,api_key,pageToken)
            r = requests.get(url)
            page = r.json()
            m = 0
            while (m < len(page["items"])):
                playlists.append(page["items"][m])
                m = m + 1
            n = n + 1
    return playlists;

def getvideos ( playlistId, api_key ):
    "Get all videos from a playlist"
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&key=%s" % (playlistId,api_key)
    r = requests.get(url)
    page = r.json()
    videos = page["items"]
    nResults = page["pageInfo"]["totalResults"]
    resultsPerPage = page["pageInfo"]["resultsPerPage"]
    nPages = ((int(nResults) / int(resultsPerPage))) + ((int(nResults)) % (int(resultsPerPage)) > 0)
    n = 1
    if nPages > 1:
        while (n < nPages):
            pageToken = page["nextPageToken"]
            url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&key=%s&pageToken=%s" % (playlistId,api_key,pageToken)
            r = requests.get(url)
            page = r.json()
            m = 0
            while (m < len(page["items"])):
                videos.append(page["items"][m])
                m = m + 1
            n = n + 1
    return videos;

parser = argparse.ArgumentParser(description="Retrieve a list of videos from a YouTube channel and playlist(s).  Requires an API key stored in file apikey")
parser.add_argument('-c','--channelId', help="YouTube Channel ID",required=True)
args = parser.parse_args()


fo = open("apikey", "r")
api_key = fo.read()


response = getchannel(args.channelId,api_key)

videolist = getvideos(response[5]["id"],api_key)
print len(videolist)
