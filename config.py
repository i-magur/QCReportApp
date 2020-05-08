import json
import os
from datetime import date

VERSION = '1.2.3'
NAME = "QCReportApp"
TITLE = "QC Report App"
DESCRIPTION = "QC Report Helper Application"


FILE_CONFIG = dict()


def get_value(name, default=None, force=False):
    global FILE_CONFIG
    if FILE_CONFIG:
        config = FILE_CONFIG
    else:
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
        except FileNotFoundError:
            with open(CONFIG_PATH, "w") as f:
                json.dump({}, f)
                config = {}
        FILE_CONFIG = config
    try:
        return config[name]
    except KeyError:
        return default


def set_value(name, value):
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    data[name] = value
    FILE_CONFIG[name] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)


today = date.today()
MONTH_NAMES = [today.replace(month=i).strftime('%B') for i in range(1, 13)]


SCOPES = [
    # 'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

USER_DIR = os.path.expanduser('~')
BASE_PATH = os.path.join(USER_DIR, 'Documents', NAME)
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

CONFIG_PATH = os.path.join(BASE_PATH, "config.json")
TOKEN_PATH = os.path.join(BASE_PATH, 'token.pickle')

CREDENTIALS_PATH = "credentials.json"
ICON_PATH = "icon.ico"


BASE_SHEET = get_value("BASE_SHEET", "")
INTERNAL_SHEET = get_value("INTERNAL_SHEET", "")
FAILURES_SHEET = get_value("FAILURES_SHEET", "")
HAND_OFF_SHEET = get_value("HAND_OFF_SHEET", "")
