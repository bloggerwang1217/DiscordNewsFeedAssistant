import json


def add_watch_later(name, link):
    watch_later_dict = {}
    try:
        with open("save/watch_later_list.json") as f:
            watch_later_dict = json.load(f)

            watch_later_dict[name] = link

        with open("save/watch_later_list.json", 'w') as f:
            json.dump(watch_later_dict, f)

        return True
    except:
        return False


def remove_watch_later(name):
    watch_later_dict = {}
    try:
        with open("save/watch_later_list.json") as f:
            watch_later_dict = json.load(f)

            del watch_later_dict[name]

        with open("save/watch_later_list.json", 'w') as f:
            json.dump(watch_later_dict, f)

        return True
    except:
        return False


def get_watch_later():
    watch_later_dict = {}

    with open("save/watch_later_list.json") as f:
        watch_later_dict = json.load(f)
    text = []
    i = 1
    for key in watch_later_dict.keys():
        text.append(f"{i}. {key}")
        text.append(watch_later_dict[key])
        text.append("----------")
        i += 1

    return '\n'.join(text)