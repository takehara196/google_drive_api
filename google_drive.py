# !/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import pickle
import os.path
import io
import sys

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_NAME = 'file_test'
GET_FOLDER_NAME = 'get_data'


def main():
    # OAuth
    drive = None
    creds = None
    if os.path.exists('config/token.pickle'):
        with open('config/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(
                'config/client_secret_450956917642-oe4jngmvfpcnucog8j4oi5c56eged08j.apps.googleusercontent.com.json'):
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/client_secret_450956917642-oe4jngmvfpcnucog8j4oi5c56eged08j.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('config/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    if creds and creds.valid:
        drive = build('drive', 'v3', credentials=creds)
    if not drive: print('Drive auth failed.')

    # Folfer list
    folders = None
    if drive:
        results = drivecd.files().list(
            pageSize=100,
            fields='nextPageToken, files(id, name)',
            q='name="' + FOLDER_NAME + '" and mimeType="application/vnd.google-apps.folder"'
        ).execute()
        folders = results.get('files', [])
        if not folders: print('No folders found.')

    # File list
    files = None
    if folders:
        query = ''
        for folder in folders:
            if query != '': query += ' or '
            query += '"' + folder['id'] + '" in parents'
        query = '(' + query + ')'
        # query += ' and (name contains ".jpeg" or name contains ".png")'
        query += ' and (name contains ".csv")'

        results = drive.files().list(
            pageSize=100,
            fields='nextPageToken, files(id, name)',
            q=query
        ).execute()
        files = results.get('files', [])
        if not files: print('No files found.')

    # Download
    if files:
        for file in files:
            request = drive.files().get_media(fileId=file['id'])
            fh = io.FileIO(f"{GET_FOLDER_NAME}/{file['name']}", mode='wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()


if __name__ == '__main__':
    main()

# def main():
#     _get_google_drive()
#
#
# if __name__ == '__main__':
#     main()
