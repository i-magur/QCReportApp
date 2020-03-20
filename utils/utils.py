import re

DEFAULT_ORDER = ["Iryna", "Oleg", "Mariia",	"Lilia", "Uliana", "Anna"]
WORD_EXP_HEADERS = ["Слова", "Таски", "Очікування"]
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
                split_words = r_name[idx+1:-1].strip()
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
