import re

USER = 13
WORDCOUNT = 8


def get_clean_data(raw_data):
    if not raw_data:
        return None
    return [row for row in raw_data[1:] if row[0]]


def collect_users_wh(raw_data):
    clean_data = get_clean_data(raw_data)
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
    return sorted([(k, v["words"], v["tasks"]) for k, v in data.items()], key=lambda i: i[0])
