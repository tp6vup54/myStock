import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleSheetAdapter:
    def __init__(self):
        credentials = self._get_or_refresh_credentials()
        self.service = build('sheets', 'v4', credentials=credentials)

    def _get_or_refresh_credentials(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credential_path = 'credentials/google-sheet.json'
        token_path = 'credentials/token.pickle'
        credentials = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credential_path, scopes)
                credentials = flow.run_local_server(port=0)
            with open(token_path, 'wb') as token:
                pickle.dump(credentials, token)
        return credentials

    def get_transaction_history(self, spreadsheet_id: str, spreadsheet_range: str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=spreadsheet_range).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            return values

