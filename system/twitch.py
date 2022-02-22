import json
import requests
from bs4 import BeautifulSoup
import os


offstream_check = 0

def add_channel(link):
    twitch_channels = {}
    try:
        with open("save/followed_twitch_channels.json") as f:
            twitch_channels = json.load(f)

        if link.split('/')[-1] not in twitch_channels:
            twitch_channels[link.split('/')[-1]] = {}
        twitch_channels[link.split('/')[-1]]["link"] = link
        twitch_channels[link.split('/')[-1]]["streaming_title"] = "No"
        twitch_channels[link.split('/')[-1]]["message_sent"] = 0

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
    global offstream_check
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

        data = '{"description":"No", "publication":{"isLiveBroadcast": false}}'

        for tag in tags:
            try:
                if tag.get("type") == "application/ld+json":
                    data = tag.get_text().strip("[]")
            except:
                pass


        with open("save/twitch_text.json", 'w') as f:
            f.write(data)

        data = {}

        with open("save/twitch_text.json") as f:
            data = json.load(f)

        title = data["description"]
        isLive = data["publication"]["isLiveBroadcast"]
        message_sent = streamers[key]["message_sent"]

        if isLive:
            if not message_sent:
                streamers[key]["streaming_title"] = title
                streamers[key]["message_sent"] = 1

                temp_list = []
                temp_list.append(f"直播: {key}")
                temp_list.append(title)
                temp_list.append(streamers[key]["link"])
                temp_list.append("----------")

                text.append('\n'.join(temp_list))

                with open("save/followed_twitch_channels.json", 'w') as f:
                    json.dump(streamers, f)
            else:
                offstream_check = 0
        else:
            if message_sent:
                offstream_check += 1
                if offstream_check == 5:
                    streamers[key]["streaming_title"] = "No"
                    streamers[key]["message_sent"] = 0
                    offstream_check = 0

                    with open("save/followed_twitch_channels.json", 'w') as f:
                        json.dump(streamers, f)

    os.remove("save/twitch_text.json")

    if len(text):
        return text
    else:
        return False