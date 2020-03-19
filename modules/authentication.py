import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from config import TOKEN_PATH, SCOPES


class Credentials:
    def __init__(self):
        self._creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                self._creds = pickle.load(token)

    @property
    def access_token(self):
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            self._get_credentials()

        return self._creds.token

    def _get_credentials(self):
        if self._creds and self._creds.expired and self._creds.refresh_token:
            self._creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            self._creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(self._creds, token)
