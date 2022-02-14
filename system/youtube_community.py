import json
import requests
from bs4 import BeautifulSoup


def add_channel(link):
    youtube_channels = {}
    try:
        with open("save/followed_youtube_channels.json") as f:
            youtube_channels = json.load(f)

        if link.split('/')[-1] not in youtube_channels:
            youtube_channels[link.split('/')[-1]] = {}
        youtube_channels[link.split('/')[-1]]["channel"] = link
        youtube_channels[link.split('/')[-1]]["community"] = f"{link}/community"

        with open("save/followed_youtube_channels.json", 'w') as f:
            json.dump(youtube_channels, f)

        return True
    except:
        return False


def remove_channel(link):
    youtube_channels = {}
    try:
        with open("save/followed_youtube_channels.json") as f:
            youtube_channels = json.load(f)

            del youtube_channels[link.split('/')[-1]]

        with open("save/followed_youtube_channels.json", 'w') as f:
            json.dump(youtube_channels, f)

        return True
    except:
        return False


def get_latest():
    youtube_community_update()
    youtube_channels = {}

    with open("save/followed_youtube_channels.json") as f:
        youtube_channels = json.load(f)
    text = []
    i = 1

    for key in youtube_channels.keys():
        text.append(f"{i}. {key}")
        text.append(youtube_channels[key]["latest_post"])
        text.append("----------")
        i += 1

    return '\n'.join(text)


def youtube_community_update():
    youtubers = {}
    with open("save/followed_youtube_channels.json") as f:
        youtubers = json.load(f)
        for key in youtubers:
            url = youtubers[key]["community"]
            r = requests.get(url)

            soup = BeautifulSoup(r.text, 'html.parser')
            tags = soup.find_all("script")

            text = []
            post_links = []

            for tag in tags:
                text.append(tag.get_text().strip())

            with open("save/community_text.json", 'w') as f:
                f.write(text[-7].strip(";var ytInitialData = "))

            with open("save/community_text.json") as f:
                data = json.load(f)
                posts = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][3]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

                for post in posts:
                    # postid = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]["postId"]
                    if "backstagePostThreadRenderer" in post:
                        postid = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]["postId"]
                        post_links.append(f"https://www.youtube.com/post/{postid}")

            youtubers[key]["latest_post"] = post_links[0]

    with open("save/followed_youtube_channels.json", 'w') as f:
        json.dump(youtubers, f)


# for i in department.keys():
#     writer.writerow([department[i]])
    
#     for j in trans.keys():

#         url = f"http://curri.aca.ntu.edu.tw/NTUVoxCourse/index.php/uquery/cou?DPRNDPT={i}+&QPYEAR=110&MSLGRD={j}"
#         writer.writerow([trans[j]])
#         r = requests.get(url)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         class_tags = soup.find_all("td", {"width":"15%"})
#         class_list = []
#         for tag in class_tags:
#             if tag.get_text().strip() != "課程中文名稱":
#                 class_list.append(tag.get_text().strip())
#         writer.writerow(class_list)