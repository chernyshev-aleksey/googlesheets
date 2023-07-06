import os

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_json = os.path.dirname(os.path.abspath(__file__)) + "/creds/key.json"

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(
            self.creds_json, self.scopes).authorize(httplib2.Http())
        self.service = build('sheets', 'v4', http=creds_service)

    def get(self, _range: str) -> list[list[str]]:
        return self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id, range=_range).execute()['values']

    def add_rows(self, _range, values: list[list[str]]):
        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            valueInputOption='USER_ENTERED',
            range=_range,
            body={
                'majorDimension': 'ROWS',
                'values': values
            }).execute()

    def create_sheets(self, sheet_name):
        body = {
            'requests': {
                'addSheet': {
                    'properties': {
                        # "gridProperties": {
                        #     "rowCount": 10,
                        #     "columnCount": 5
                        # },
                        'title': sheet_name
                    }
                }
            }
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()

        except HttpError:
            pass
