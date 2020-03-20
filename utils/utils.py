def get_users_wh(raw_data):
    if not raw_data:
        return None
    # 8 wordcount, 13 user
    return [[row[13], row[8]] for row in raw_data[1:] if row[0]]


def collect_users_wh(raw_data):
    clean_data = get_users_wh(raw_data)
    if not clean_data:
        return None
    data = dict()
    for r in clean_data:
        try:
            data[r[0]]["words"] += int(r[1])
            data[r[0]]["tasks"] += 1
        except KeyError:
            data[r[0]] = {"words": int(r[1]), "tasks": 1}
    return sorted([(k, v["words"], v["tasks"]) for k, v in data.items()], key=lambda i: i[0])
