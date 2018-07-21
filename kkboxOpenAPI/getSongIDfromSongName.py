# -*- coding: UTF-8 -*-
from kkbox_developer_sdk.auth_flow import KKBOXOAuth
from kkbox_developer_sdk.api import KKBOXAPI
import json

def getSongID(songname,token):
	kkboxapi = KKBOXAPI(token)
	search_results = kkboxapi.search_fetcher.search(songname, types=['track'], terr='TW')
	songID = search_results['tracks']['data']
	return songID[0]['id']


CLIENT_ID = "your_kkbox_CLIENT_ID"
CLIENT_SECRET = "your_kkbox_CLIENT_SECRET"
auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)  
token = auth.fetch_access_token_by_client_credentials()

songname = "愛我別走	張震嶽"
print(getSongID(songname, token))