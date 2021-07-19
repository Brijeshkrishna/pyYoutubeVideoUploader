# -*- coding: utf-8 -*-

import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'


    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=None, month=None, day=None, hour=None, minute=None):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt




FILENAME=" "#  videofile in mp4
THUM="" # tumbnail in jpg or png

CLIENT_SECRET_FILE = 'client_secret_mybot.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)






request_body = {
    'snippet': {
        'categoryId': 19, # list of categoryId => https://pastebin.com/raw/tZ7c4EXU
        'title': 'Upload Testing ',
        'description': 'Hello World . ',
        'tags': ['Travel', 'video test', 'Travel Tips']
    },
    'status': {
        'privacyStatus': 'private',
        
        'selfDeclaredMadeForKids': False, 
       # 'publishAt': convert_to_RFC_datetime(year=, month=, day=, hour=, minute=), # if want to schedule the video set the date and time 

    },
    'notifySubscribers': True
}

#video upload
mediaFile = MediaFileUpload(FILENAME)

response_upload_video = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()

#thumbnail upload

response_upload_thumb= service.thumbnails().set(
    videoId=response_upload_video.get('id'),
    media_body=MediaFileUpload(THUM)
).execute()


print(response_upload_video,response_upload_thumb)


