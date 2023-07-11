import httplib2
from bson import json_util
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from src.database.google import DataBaseGoogleSheet
from src.settings import config


class GoogleSheet:
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.db = DataBaseGoogleSheet(config)
        creds_service = ServiceAccountCredentials.from_json_keyfile_dict(
            self.db.get_credential(config.NAME_PROJECT), self.scopes)
        self.service = build('sheets', 'v4', credentials=creds_service)
        self.sheets = self.service.spreadsheets()

    def get_values_by_range(self, _range: str) -> list[list[str]]:
        return self.sheets.values().get(spreadsheetId=self.sheet_id, range=_range).execute()['values']

    def add_rows(self, _range, values: list[list[str]]):
        self.sheets.values().update(
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
            self.sheets.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()

        except HttpError:
            pass
