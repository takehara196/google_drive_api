# !/usr/bin/env python
# -*- coding:utf-8 -*-

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('config/token.pickle')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('config/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive = build('drive', 'v3', http=creds.authorize(Http()))

dt_now = datetime.datetime.now()

file_metadata = {
    'name': f'test_folder_{dt_now.strftime("%Y/%m/%d_%H:%M:%S")}',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': ['1wNMmUygYdcsjcmCpveK6YhoX--uY7npq']
}
drive_service = drive.files().create(body=file_metadata,
                                     fields='id').execute()

# fieldに指定したidをfileから取得できる
# print('Folder ID: %s' % file.get('id'))
