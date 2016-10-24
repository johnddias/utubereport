#!/usr/bin/env python

import logging
import sys
import requests
import argparse
import json
import csv


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

#get API key from apikey file
#todo: allow user to specify api key path and filename
fo = open("apikey", "r")
api_key = fo.read()
fo.close()

#get all the playlists for the speicified channel
allplaylists = getchannel(args.channelId,api_key)

#layout headers for csv file output
#todo: allow user to specify csv filename and path for output
csvf = open("utubereport.csv", "wb")
writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
headers = ['Playlist','Title','Description','Date Added','Video URL']
writer.writerow(headers)

for playlist in allplaylists:
    videolist = getvideos(playlist["id"],api_key)
    for video in videolist:
        videoUrl = "https://youtube.com/watch?v=%s" % video["snippet"]["resourceId"]["videoId"]
        newRow = [playlist["snippet"]["title"].encode("utf-8"),video["snippet"]["title"].encode("utf-8"),video["snippet"]["description"].encode("utf-8"),video["snippet"]["publishedAt"].encode("utf-8"),videoUrl.encode("utf-8")]
        writer.writerow(newRow)

csvf.close()
