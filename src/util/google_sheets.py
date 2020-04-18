# pylint: disable=no-member
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle
from services.history import History

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

        print("Value found: ", values_input)
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

    #init_value = [["C1", "C2", "C3"], [1, 2, 3], [4, 5, 6]]
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
        # Read in current sheets
        try:
            current_values = self.get_values(sheet_name)
        except:
            print("Invalid sheet name")
            return -1

        print("Values:", current_values)

        keys = current_values[0]

        print("keys: ", keys)

        tickers = []
        dic = {}
        for stock in current_values[1:]:
            dic[stock[0]] = stock[1:]
            tickers.append(stock)
            # print("S", stock)

        print("DIC: ", dic)
        print("Tickers: ", tickers)

        # History["get_closing_price"]("2020-04-17", tickers)
        History["get_closing_price"](sheet_name, tickers)
        # Get all tickers
        # ticker_list = ["SPY", "AAPL", "VOO"]

        # ticker_current = Current["get_current_price_list"](ticker_list)

    # Add


# gs = GoogleSheets()
# # gs.get_values()

# test_data = [['TICKER', 'CURRENT', 'PREDICTED', 'ERROR CHANCE', 'PREDICTED RATIO', 'ACTUAL', 'ACTUAL RATIO'], ['MO', 40.90999984741211, 42.85, 8.599, 1.0474211723251965, 'NA', 'NA'], ['ADM', 35.4900016784668, 37.16, 6.343, 1.0470554590744483, 'NA', 'NA'], ['CPB', 50.5, 50.49, 3.547, 0.9998019801980198, 'NA', 'NA'], ['CHD', 72.0, 72.5, 4.523, 1.0069444444444444, 'NA', 'NA'], ['CLX', 195.63999938964844, 198.01, 2.886, 1.0121140902563146, 'NA', 'NA'], ['KO', 47.61000061035156, 49.66, 7.847, 1.0430581676825839, 'NA', 'NA'], ['CL', 72.6500015258789, 72.12, 3.803, 0.9927047279456682, 'NA', 'NA'], ['CAG', 32.869998931884766, 32.4, 3.524, 0.9857012793684987, 'NA', 'NA'], ['STZ', 162.36000061035156, 175.07, 18.05, 1.0782828242292952, 'NA', 'NA'], ['COST', 310.2699890136719, 310.29, 2.8, 1.0000644953976754, 'NA', 'NA'], ['COTY', 5.78000020980835, 7.87, 44.754, 1.3615916460772843, 'NA', 'NA'], ['EL', 157.7899932861328, 166.42, 5.984, 1.054692991197596, 'NA', 'NA'], ['GIS', 59.04999923706055, 56.76, 3.568, 0.9612193180923309, 'NA', 'NA'], ['HSY', 142.60000610351562, 142.29, 4.234, 0.9978260442479182, 'NA', 'NA'], ['HRL', 48.65999984741211, 48.76, 3.056, 1.0020550791800549, 'NA', 'NA'], [
#     'SJM', 115.4000015258789, 114.8, 3.288, 0.9948006800871284, 'NA', 'NA'], ['K', 62.95000076293945, 62.67, 3.382, 0.9955520133511373, 'NA', 'NA'], ['KMB', 137.6699981689453, 137.23, 3.803, 0.9968039647359814, 'NA', 'NA'], ['KHC', 28.049999237060547, 28.28, 5.477, 1.0081996709160537, 'NA', 'NA'], ['KR', 32.029998779296875, 32.36, 2.763, 1.0103028795903803, 'NA', 'NA'], ['LW', 55.90999984741211, 57.7, 6.204, 1.0320157423980165, 'NA', 'NA'], ['MKC', 152.55999755859375, 156.07, 7.731, 1.0230073577449958, 'NA', 'NA'], ['TAP', 44.599998474121094, 49.26, 16.041, 1.1044843427199407, 'NA', 'NA'], ['MDLZ', 53.709999084472656, 53.83, 4.827, 1.002234237899327, 'NA', 'NA'], ['MNST', 62.290000915527344, 62.06, 4.077, 0.9963075788706561, 'NA', 'NA'], ['PEP', 135.02999877929688, 135.1, 5.502, 1.0005184123627042, 'NA', 'NA'], ['PM', 75.44000244140625, 77.39, 5.885, 1.025848323110916, 'NA', 'NA'], ['PG', 121.22000122070312, 120.54, 3.859, 0.994390354612643, 'NA', 'NA'], ['SYY', 46.099998474121094, 58.74, 34.735, 1.2741865931508556, 'NA', 'NA'], ['TSN', 60.150001525878906, 68.9, 19.253, 1.1454696301272163, 'NA', 'NA'], ['WMT', 128.75999450683594, 129.87, 3.321, 1.0086207326849888, 'NA', 'NA'], ['WBA', 43.439998626708984, 46.71, 7.759, 1.0752762770871835, 'NA', 'NA']]

# # gs.write_values(test_data, "2020-04-16")
# gs.add_sheet([["C1", "C2", "C3"], [1, 2, 3], [4, 5, 6]], "2020-04-16")
