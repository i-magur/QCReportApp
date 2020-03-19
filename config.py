import json

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
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)


SCOPES = [
    # 'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')
# CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
#
# ICON_PATH = os.path.join(BASE_DIR, "icon.ico")

TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = "credentials.json"

CONFIG_PATH = "config.json"
ICON_PATH = "icon.ico"

TITLE = "QC Report App"

BASE_SHEET = get_value("BASE_SHEET", "")
