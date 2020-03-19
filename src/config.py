import os

SCOPES = [
    # 'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

ICON_PATH = os.path.join(BASE_DIR, "icon.ico")

TITLE = "QC Report App"

