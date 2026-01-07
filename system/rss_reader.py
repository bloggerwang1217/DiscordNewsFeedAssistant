import feedparser
import json
from bs4 import BeautifulSoup
import time
from datetime import datetime


def add_rss(name, link):
    followed_dict = {}
    try:
        with open("save/followed_rss.json") as f:
            followed_dict = json.load(f)

            followed_dict[name] = {}
            followed_dict[name]["link"] = link
            followed_dict[name]["last_check_time"] = time.time()

        with open("save/followed_rss.json", 'w') as f:
            json.dump(followed_dict, f)

        return True
    except:
        return False


def remove_rss(name):
    followed_dict = {}
    try:
        with open("save/followed_rss.json") as f:
            followed_dict = json.load(f)

            del followed_dict[name]

        with open("save/followed_rss.json", 'w') as f:
            json.dump(followed_dict, f)

        return True
    except:
        return False


def get_rss(name, index):
    followed_dict = {}

    with open("save/followed_rss.json") as f:
        followed_dict = json.load(f)

    text = []
    NewsFeed = feedparser.parse(followed_dict[name]["link"])
    entry = NewsFeed["entries"][index-1]

    text = []
    text.append(entry.title + '\n' + entry.published + "\n" + "\n-----正文-----")


    try:
        soup = BeautifulSoup(entry.summary, 'html.parser')
        content = soup.get_text()

        for paragraph in content.split("\n\n\n"):
            if paragraph != "":
                text.append(paragraph + "----------")
    except:
        text.append("無正文")

    text.append("-----連結-----" + "\n" + entry.link)

    return text


def check_latest():
    followed_dict = {}

    with open("save/followed_rss.json") as f:
        followed_dict = json.load(f)

    text = []
    current_time = time.time()

    for key in followed_dict.keys():
        NewsFeed = feedparser.parse(followed_dict[key]["link"])
        last_check_time = followed_dict[key].get("last_check_time", 0)

        # Check up to 10 recent entries
        for entry in NewsFeed["entries"][:10]:
            # Get entry published time
            entry_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                entry_time = time.mktime(entry.published_parsed)
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                entry_time = time.mktime(entry.updated_parsed)

            # Skip if we can't determine time or if it's older than last check
            if not entry_time or entry_time <= last_check_time:
                continue

            # This is a new entry, add it to output
            temp_list = []
            temp_list.append(entry.title + '\n' + entry.published + "\n" + "-----正文-----")

            try:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                content = soup.get_text()
                for paragraph in content.split("\n\n\n"):
                    if paragraph != "":
                        temp_list.append(paragraph + "\n--------------")
            except:
                temp_list.append("無正文")

            temp_list.append("-----連結-----" + "\n" + entry.link)
            text.append(temp_list)

        # Update last check time
        followed_dict[key]["last_check_time"] = current_time

    with open("save/followed_rss.json", 'w') as f:
        json.dump(followed_dict, f)

    if len(text):
        return text
    else:
        return False