# !/usr/bin/env python
# -*- coding:utf-8 -*-

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('config/token.pickle')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('config/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))
print(drive_service)

dt_now = datetime.datetime.now()

# フォルダ作成
file_metadata = {
    'name': f'test_folder_{dt_now.strftime("%Y/%m/%d_%H:%M:%S")}',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': ['1wNMmUygYdcsjcmCpveK6YhoX--uY7npq']
}
file = drive_service.files().create(body=file_metadata,
                                             fields='id').execute()

# fieldに指定したidをfileから取得できる
print('Folder ID: %s' % file.get("id"))

############################
# ファイルアップロード
folder_id = file.get("id")
print(folder_id)
file_metadata = {
    'name': 'sample.txt',
    'parents': [folder_id]
}
media = MediaFileUpload(
    'sample.txt',
    mimetype='text/plain',
    resumable=True
)
file = drive_service.files().create(
    body=file_metadata, media_body=media, fields='id'
).execute()

# fieldに指定したidをfileから取得できる
print('File ID: %s' % file.get('id'))

# 参考
# https://zenn.dev/wtkn25/articles/python-googledriveapi-operation
