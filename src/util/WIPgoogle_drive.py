# https://stackoverflow.com/questions/58107431/how-to-create-a-sheet-under-a-specific-folder-with-google-api-for-python
# https://developers.google.com/drive/api/v3/quickstart/python
# pylint: disable=no-member
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle


class GoogleDrive:

    drive_cred_file = './src/config/credentials_drive.json'
    drive_creds = None

    def __init__(self):
        print("INIT")

    def create_sheet_to_dir(self, init_value):
        # https://developers.google.com/sheets/api/guides/create
        drive = build('drive', 'v3', credentials=self.drive_creds)
        file_metadata = {
            'name': 'sampleName',
            'parents': ['1qOX2gMaF23X09Mb-8W2gDvrBr2cCTJ3p'],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
        }

        res = drive.files().create(body=file_metadata).execute()
        print(res)

# Might now work with creds being on both sides
