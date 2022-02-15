# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

# import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



def store_json(response:dict,name:str ):
    with open(name+'.json','w') as response_json:
        json.dump(response,response_json,indent=4)

def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly","https://www.googleapis.com/auth/youtube.force-ssl"]


    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # print('type:',type(youtube))
    return(youtube)

   

def retrieve_disliked_video_list(youtube):
    token = None
    vid_list = []
    total_videos = 0

    try:
        while(True):
            request = youtube.videos().list(part="snippet",
            maxResults=50,myRating="dislike",pageToken=token)
            response = request.execute()
            vid_list.extend(response["items"])
            token = response["nextPageToken"]
            total_videos = response["pageInfo"]["totalResults"]
    
    except KeyError:
        print('Key Error reported')

    except googleapiclient.errors.HttpError as e:
        print(e.__dict__)

    finally:
        if total_videos != len(vid_list):
            print('List Incomplete.',end =' ')
        print(f'{len(vid_list)}/{response["pageInfo"]["totalResults"]} videos listed')
        store_json(response,'last_response')
        store_json({'disliked videos':vid_list}, 'disliked_vid')
        return(vid_list)
    
def create_playlist(youtube,pl_name):
    try:
        request = youtube.playlists().insert(
            part="id,snippet",
            body={
            "snippet": {
                "title": pl_name
            }
            }
        )
        response = request.execute()
        # print('Playlist response:',response)
        return(response)
    except  googleapiclient.errors.HttpError as e:
        print(e.__dict__)

def upload_vid(youtube,pl,vid_list):
    counter = 0
    try:

        for video in vid_list:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                "snippet": {
                "playlistId": pl['id'],
                "resourceId": {
                "kind": "youtube#video",
                "videoId": video['id']
                            }
                            }
                    }
                )
            response = request.execute()
            counter+=1
    except  googleapiclient.errors.HttpError as e:
        print(e.__dict__)
    
    finally:
        print(f'{counter}/{len(vid_list)} videos uploaded')

    # print(response)

def main():
    youtube = authenticate()
    vid_list = retrieve_disliked_video_list(youtube)
    pl_response = create_playlist(youtube,'Disliked Videos')
    upload_vid(youtube,pl_response,vid_list)

if __name__ == "__main__":
    main()