import json
import requests
from bs4 import BeautifulSoup
import os


def add_channel(link):
    twitch_channels = {}
    try:
        with open("save/followed_twitch_channels.json") as f:
            twitch_channels = json.load(f)

        if link.split('/')[-1] not in twitch_channels:
            twitch_channels[link.split('/')[-1]] = {}
        twitch_channels[link.split('/')[-1]]["link"] = link
        twitch_channels[link.split('/')[-1]]["streaming_title"] = "No"
        twitch_channels[link.split('/')[-1]]["last_status"] = ""

        with open("save/followed_twitch_channels.json", 'w') as f:
            json.dump(twitch_channels, f)

        return True
    except:
        return False


def remove_channel(link):
    twitch_channels = {}
    try:
        with open("save/followed_twitch_channels.json") as f:
            twitch_channels = json.load(f)

            del twitch_channels[link.split('/')[-1]]

        with open("save/followed_twitch_channels.json", 'w') as f:
            json.dump(twitch_channels, f)

        return True
    except:
        return False



def check_latest():
    streamers = {}
    text = []

    with open("save/followed_twitch_channels.json") as f:
        streamers = json.load(f)

    for key in streamers:
        url = streamers[key]["link"]

        r = requests.get(url)
        r_text = r.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r.text)[0])
        soup = BeautifulSoup(r_text, 'html.parser')
        tags = soup.find_all("script")
        name_tags = soup.find_all("meta")

        data = '{"description":"No"}'

        for tag in tags:
            try:
                if tag.get("type") == "application/ld+json":
                    data = tag.get_text().strip("[]")
            except:
                pass

        current_status = str()

        for tag in name_tags:
            try:
                if tag.get("name") == "description":
                    current_status = tag.get("content")
            except:
                pass


        with open("save/twitch_text.json", 'w') as f:
            f.write(data)

        data = {}

        with open("save/twitch_text.json") as f:
            data = json.load(f)

        title = data["description"]

        if streamers[key]["streaming_title"] != title and streamers[key]["last_status"] != current_status:
            streamers[key]["streaming_title"] = title
            streamers[key]["last_status"] = current_status
            if data["description"] != "No":
                temp_list = []
                temp_list.append(f"直播: {key}")
                temp_list.append(title)
                temp_list.append(streamers[key]["link"])
                temp_list.append("----------")

                text.append('\n'.join(temp_list))

            with open("save/followed_twitch_channels.json", 'w') as f:
                json.dump(streamers, f)

    os.remove("save/twitch_text.json")

    if len(text):
        return text
    else:
        return False