import os

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv


def main():
    load_dotenv()
    google_credentials_file_path = os.path.join(
        os.path.dirname(__file__),
        os.getenv('GOOGLE_GREDENTIALS_FILENAME')
    )
    spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        google_credentials_file_path, scopes
    )
    authorization = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=authorization)
    request = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=['Лист1'])
    print(request.execute())


if __name__ == '__main__':
    main()
