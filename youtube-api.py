# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def store_json(response:dict,name:str ):
    with open(name+'.json','w') as response_json:
        json.dump(response,response_json,indent=4)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # channel_request = youtube.channels().list(
    #     part="contentDetails",
    #     mine=True
    # )
    
    # playlist_request = youtube.playlists().list(
    #     part="snippet,contentDetails",
    #     maxResults=25,
    #     mine=True
    # )
    # channel_response = channel_request.execute()
    # playlist_response = playlist_request.execute()

    # store_json(channel_response,'ch_json')
    # store_json(playlist_response, 'pl_json')    

    token = None

    vid_list = []

    try:
        while(True):
            request = youtube.videos().list(part="snippet",
            maxResults=50,myRating="like",pageToken=token)
            response = request.execute()
            vid_list.extend(response["items"])
            token = response["nextPageToken"]
    except KeyError:
        print('Key Error reported')
        pass
    finally:
        store_json(response,'last_response')
        store_json({'liked videos':vid_list}, 'liked_vid')
        print(len(vid_list))

if __name__ == "__main__":
    main()