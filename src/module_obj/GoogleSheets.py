# pylint: disable=no-member
# pylint: disable=import-error

import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle
from data_source.history import History
from util.conversion import Conversion

# here enter the id of your google sheet


class GoogleSheets:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = '1PUXr633cTwpGMELumWuveqFQBOhB7zW-gkSUjKnkWm0'
    SAMPLE_RANGE_NAME = 'A1:AA750'
    service = {}
    creds = None
    api_version = 'v4'
    api_service_name = 'sheets'
    secret_cred_file = './src/config/credentials.json'

    def __init__(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # here enter the name of your downloaded JSON file
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.secret_cred_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        try:
            self.service = build(self.api_service_name,
                                 self.api_version, credentials=self.creds)
            print(self.api_service_name, 'service created successfully')
        except Exception as e:
            print(e)

    def get_values(self, sheet_name):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result_input = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                          range=sheet_name+'!A1:AA750').execute()
        values_input = result_input.get('values', [])

        # print("Value found: ", values_input)
        values_input = Conversion["convert_to_number"](values_input)
        # print("New Values :", values_input)
        return values_input

    def write_values(self, new_value, sheet_name):
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
        sheet = self.service.spreadsheets()

        response_date = sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            valueInputOption='RAW',
            range=sheet_name+'!A1',
            body=dict(
                majorDimension='ROWS',
                values=new_value
                # values=df_gold
            )
        ).execute()
        print('Sheet successfully Updated')

    # Creates new spreadsheet .. not needed.
    # Took a while to get, might use this in the future
    def create_sheet(self, init_value):
        # https://developers.google.com/sheets/api/guides/create

        print("create new")
        spreadsheet = {
            'properties': {
                'title': "Test sheet"
            }
        }
        sheet = self.service.spreadsheets()

        spreadsheet = sheet.create(
            body=spreadsheet, fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        sheet_id = spreadsheet.get('spreadsheetId')

        sheet.values().update(
            spreadsheetId=sheet_id,
            valueInputOption='RAW',
            range=self.SAMPLE_RANGE_NAME,
            body=dict(
                majorDimension='ROWS',
                values=init_value
                # values=df_gold
            )
        ).execute()
        print('Sheet successfully Updated')

    # init_value = [["C1", "C2", "C3"], [1, 2, 3], [4, 5, 6]]
    # date = 2020-04-16
    def add_sheet(self, init_value, date):
        print('adding to current spreadsheet')
        body = {
            'requests': {
                "addSheet": {
                    "properties": {
                        "sheetId": date.replace('-', ''),
                        "title": date,
                        "gridProperties": {
                            "rowCount": 600,
                            "columnCount": 12
                        },
                        "tabColor": {
                            "red": 0.3,
                            "green": 1.0,
                            "blue": 0.4
                        },
                    }
                }
            }
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            print("Successfully created sheet")

            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                valueInputOption='RAW',
                range=date+'!A1',
                body=dict(
                    majorDimension='ROWS',
                    values=init_value
                )
            ).execute()
            print("Initial values")
        except Exception as e:
            print("Error creating sheet", e)

    def update_sheet(self, sheet_name):
        print("Updating", sheet_name)
        tickers = []
        dic = {}

        try:
            current_values = self.get_values(sheet_name)
        except:
            print("Invalid sheet name")
            return -1

        keys = current_values[0]

        for stock in current_values[1:]:
            dic[stock[0]] = stock[1:]
            tickers.append(stock[0])

        # print("DIC: ", dic)
        # print("Tickers: ", tickers)

        # History["get_closing_price"]("2020-04-17", tickers)
        closing_prices = History["get_closing_price"](sheet_name, tickers)

        for t in tickers:
            if np.isnan(closing_prices[t]):
                print("IN HERE")
                continue
            dic[t][4] = closing_prices[t]
            # print(type(float(dic[t][0])), type(closing_prices[t]))
            dic[t][5] = closing_prices[t]/float(dic[t][0]) * 100

        print("DIC AFTER:", dic)
        sheet_value = Conversion["dic_to_sheets"](dic, keys)
        print("sheet value: ", sheet_value)
        self.write_values(sheet_value, sheet_name)

    # Add

