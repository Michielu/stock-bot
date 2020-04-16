# Source: https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1PUXr633cTwpGMELumWuveqFQBOhB7zW-gkSUjKnkWm0'
SAMPLE_RANGE_NAME = 'A1:B2'


def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './src/config/credentials.json', SCOPES)  # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                      range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

    print("Value found: ", values_input)


main()

df = pd.DataFrame(values_input[1:], columns=values_input[0])
print("DF: ", df)
# df_gold = df[(df['Medal'] == 'Gold') & (df['Sport'] == 'Gymnastics')]
# df_gold = pd.DataFrame({'APD': [215.46, 5.118, '2020-04-16'], 'ALB': [60.23, 6.606, '2020-04-16'], 'AMCR': [9.21, 12.267, '2020-04-16'], 'AVY': [109.98, 6.216, '2020-04-16'], 'BLL': [67.84, 4.399, '2020-04-16'], 'CE': [
#    87.47, 19.697, '2020-04-16'], 'CF': [34.89, 29.832, '2020-04-16'], 'CTVA': [26.49, 8.303, '2020-04-16'], 'DOW': [39.42, 30.472, '2020-04-16'], 'DD': [47.17, 35.704, '2020-04-16'], 'EMN': [60.33, 23.698, '2020-04-16']})
df_gold = df

# change this by your sheet ID
EXPORT_SPREADSHEET_ID = '1z29YBnfRorhV28dExGRtC-zfBgFd5J5GD0H4Vn5J48g'

# change the range if needed
SAMPLE_RANGE_NAME = 'A1:B2'


def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    # print(SCOPES)

    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        # return service
    except Exception as e:
        print(e)
        # return None


# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('./src/config/credentials.json', 'sheets', 'v4', [
               'https://www.googleapis.com/auth/spreadsheets'])


def Export_Data_To_Sheets():
    print(df_gold.T.reset_index().T.values.tolist())
    response_date = service.spreadsheets().values().update(
        spreadsheetId=EXPORT_SPREADSHEET_ID,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict(
            majorDimension='ROWS',
            values=df_gold.T.reset_index().T.values.tolist()
            # values=df_gold
        )
    ).execute()
    print('Sheet successfully Updated')


Export_Data_To_Sheets()
