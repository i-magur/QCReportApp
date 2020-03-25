import re
from datetime import datetime

DEFAULT_ORDER = ["Iryna", "Oleg", "Mariia", "Lilia", "Uliana", "Anna"]
DEFAULT_LABELS = [
    "N°Commande",
    "N°Devis",
    "Client",
    "DV",
    "Chef de Projet",
    "Langue Source",
    "Langue Cible",
    "Prestation",
    "UnitesFourn",
    "Début",
    "Date LF",
    "Actual THT",
    "Actual DT",
    "Proofreader",
    "devabit QC comments",
    "Time spent on package opening"
]

FAULT_INDEXES = list(range(11)) + [14]
FAULT_IDX = 13
FAULT_LABELS = [DEFAULT_LABELS[idx] for idx in FAULT_INDEXES]

HAND_OFF_INDEXES = list(range(10)) + [11, 10, 12]
HAND_OFF_SHORT = list(range(5)) + [8, 9, 11, 10, 12]
HAND_OFF_IDX = 12
HAND_OFF_LABELS = [DEFAULT_LABELS[idx] for idx in HAND_OFF_INDEXES]


USER = 13
WORDCOUNT = 8


def get_clean_data(raw_data):
    if not raw_data:
        return None
    return [row for row in raw_data[1:] if row[0]]


def collect_users_wh(clean_data):
    if not clean_data:
        return None
    data = dict()
    for r in clean_data:
        names = re.split(',(?![0-9])(?! [0-9])', r[USER])
        words = int(r[WORDCOUNT])
        for name in names:
            name = name.strip()
            if (idx := name.find('(')) != -1:
                r_name = name
                name = r_name[:idx].strip()
                split_words = r_name[idx + 1:-1].strip()
                split_words = split_words.replace(',', '').replace('.', '').replace(' ', '')
                split_words = int(split_words)
            else:
                split_words = words // len(names)

            try:
                data[name]["words"] += split_words
                data[name]["tasks"] += 1
            except KeyError:
                data[name] = {"words": split_words, "tasks": 1}
    return [
        (name, data.get(name, {"words": 0})["words"], data.get(name, {"tasks": 0})["tasks"])
        for name in DEFAULT_ORDER
    ]


def collect_faults(cd):
    pass


def bind_tree(widget, event, callback, add=''):
    """Binds an event to a widget and all its descendants."""

    widget.bind(event, callback, add)
    for child in widget.children.values():
        bind_tree(child, event, callback, add)


def find_a_place_to_fill(ws, current_date, date_format):
    values = ws.col_values(1)
    for ridx, date_cell in enumerate(values, 1):
        try:
            date = datetime.strptime(date_cell, date_format.replace('#', '')).date()
            if date > current_date:
                return ridx
            if date == current_date:
                return ''
        except ValueError:
            continue

    return len(values) + 1
