from datetime import datetime
import os

import requests
from xml.etree import ElementTree
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

from db_operations import request_to_db, create_table



def get_usd_exchange_rate():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    response.raise_for_status()
    tree = ElementTree.fromstring(response.content)
    for elem in tree.iter('Valute'):
        code = elem.find('CharCode').text
        if code == 'USD':
            usd_exchange = elem.find('Value').text
            return float(usd_exchange.replace(',', '.'))


def main():
    load_dotenv()
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_password = os.getenv('DB_PASSWORD')
    db_user = os.getenv('DB_USERNAME')
    db_port = os.getenv('DB_PORT')
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
        spreadsheetId=spreadsheet_id, ranges=['Лист1']
    )
    rows = request.execute()['valueRanges'][0]['values']
    print([tuple(row) for row in rows])
    '''
    create_table(
        db_user,
        db_password,
        db_host,
        db_port,
        db_name,
        'canalservice'
    )
    for row in rows[1:]:
        usd_price = int(row[2])
        usd_exchange_rate = get_usd_exchange_rate()
        rub_price = int(usd_price * usd_exchange_rate)
        row.append(rub_price)
        date = datetime.strptime(row[3].replace('.', '-'), '%d-%m-%Y').date()
        request_to_db(
            db_user,
            db_password,
            db_host,
            db_port,
            db_name,
            query=(
                f"""
                insert into canalservice 
                (id, order_id, usd_price, rub_price, delivery_time)
                values
                ({row[0]}, {row[1]}, {row[2]}, {row[4]}, date '{date}')
                on conflict do nothing
                """ 
            )
        )
    '''

if __name__ == '__main__':
    main()
