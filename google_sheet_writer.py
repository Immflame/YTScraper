import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)


class GoogleSheetWriter:
    def __init__(self, spreadsheet_id, worksheet_name='YouTube Data'):
        self.sheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.sheet = None
        self.agcm = None

    @staticmethod
    def get_creds():
        creds = service_account.Credentials.from_service_account_file(r'credentials.json') # Замените на ваш путь
        return creds

    async def init_spreadsheet(self):
        creds = self.get_creds()
        self.agcm = build('sheets', 'v4', credentials=creds)
        self.sheet = self.agcm.spreadsheets()
        logging.info(f"Initialized spreadsheet '{self.sheet_id}'")

    async def write_to_sheet(self, data):
        if self.sheet is None:
            await self.init_spreadsheet()

        if not data:
            return

        values = [[item.get('title', ''), item.get('description', ''), ','.join(item.get('tags', [])),
                   item.get('channel_name', ''), item.get('views_number', ''), item.get('upload_date', ''),
                   item.get('genre', '')] for item in data]

        try:
            body = {'values': values}
            result = self.sheet.values().append(spreadsheetId=self.sheet_id,
                                                range='A1',
                                                valueInputOption='USER_ENTERED',
                                                body=body).execute()
            logging.info("Data written to sheet.")
        except HttpError as error:
            logging.error(f"Error writing to sheet: {error}")




