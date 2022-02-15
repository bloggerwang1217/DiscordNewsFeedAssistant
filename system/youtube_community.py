import json
import requests
from bs4 import BeautifulSoup
import os


def add_channel(link):
    youtube_channels = {}
    try:
        with open("save/followed_youtube_channels.json") as f:
            youtube_channels = json.load(f)

        if link.split('/')[-1] not in youtube_channels:
            youtube_channels[link.split('/')[-1]] = {}
        youtube_channels[link.split('/')[-1]]["channel"] = link
        youtube_channels[link.split('/')[-1]]["community"] = f"{link}/community"
        youtube_channels[link.split('/')[-1]]["videos"] = f"{link}/videos"

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
    youtube_update("save/followed_youtube_channels.json")
    youtube_channels = {}

    with open("save/followed_youtube_channels.json") as f:
        youtube_channels = json.load(f)
    
    text = []
    i = 1

    for key in youtube_channels.keys():
        temp_list = []
        
        temp_list.append((f"{i}. {youtube_channels[key]['latest_post_poster']}({youtube_channels[key]['latest_post_time']})"))
        temp_list.append(youtube_channels[key]["latest_post_link"])
        temp_list.append(youtube_channels[key]["latest_post_text"])
        temp_list.append(youtube_channels[key]["latest_post_image"])
        temp_list.append("----------")

        text.append(temp_list)
        i += 1

    return text


def check_latest():
    with open("save/new_post.json", 'w') as f:
        f.write("{}")
    youtube_update("save/new_post.json")
    new_youtube_channels = {}
    old_youtube_channels = {}

    with open("save/new_post.json") as new_f:
        new_youtube_channels = json.load(new_f)

    with open("save/followed_youtube_channels.json") as old_f:
        old_youtube_channels = json.load(old_f)
    
    text = []
    i = 1

    for key in new_youtube_channels.keys():
        temp_list = []
        
        if new_youtube_channels[key]["latest_post_link"] != old_youtube_channels[key]["latest_post_link"]:
            temp_list.append((f"{i}. {youtube_channels[key]['latest_post_poster']}({youtube_channels[key]['latest_post_time']})"))
            temp_list.append(youtube_channels[key]["latest_post_link"])
            temp_list.append(youtube_channels[key]["latest_post_text"])
            temp_list.append(youtube_channels[key]["latest_post_image"])
            temp_list.append("----------")

            text.append(temp_list)
            i += 1

    if len(text):
        with open("save/followed_youtube_channels.json", 'w') as f:
            json.dump(new_youtube_channels, f)
        return text
    else:
        return False


def youtube_update(saving_to):
    youtubers = {}
    with open(saving_to) as f:
        youtubers = json.load(f)
        for key in youtubers:
            community_url = youtubers[key]["community"]
            # videos_url = youtubers[key]["videos"]
            community_r = requests.get(community_url)
            # videos_r = requests.get(videos_url)

            community_soup = BeautifulSoup(community_r.text, 'html.parser')
            # videos_soup = BeautifulSoup(community_r.text, 'html.parser')
            community_tags = community_soup.find_all("script")
            # videos_tags = videos_soup.find_all("script")

            community_text = []
            videos_text = []
            post_data = []

            for community_tag in community_tags:
                community_text.append(community_tag.get_text().strip())

            # for videos_tag in videos_tags:
                # videos_text.append(videos_tag.get_text().strip())

            with open("save/community_text.json", 'w') as f:
                f.write(community_text[-7].strip(";var ytInitialData = "))

            with open("save/community_text.json") as f:
                data = json.load(f)
                posts = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][3]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

                for post in posts:
                    # print(post, end="\n")
                    # postid = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]["postId"]
                    try:
                        prefix = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]
                        postid = prefix["postId"]
                        author_text = prefix["authorText"]["runs"][0]["text"]
                        content_text = prefix["contentText"]["runs"][0]["text"]
                        image_link = prefix["backstageAttachment"]["backstageImageRenderer"]["image"]["thumbnails"][0]["url"]
                        publish_time = prefix["publishedTimeText"]["runs"][0]["text"]

                        post_data_dict = {}
                        post_data_dict["link"] = f"https://www.youtube.com/post/{postid}"
                        post_data_dict["poster"] = author_text
                        post_data_dict["text"] = content_text
                        post_data_dict["image"] = image_link
                        post_data_dict["time"] = publish_time
                        post_data.append(post_data_dict)
                    except:
                        pass

            youtubers[key]["latest_post_link"] = post_data[0]["link"]
            youtubers[key]["latest_post_poster"] = post_data[0]["poster"]
            youtubers[key]["latest_post_text"] = post_data[0]["text"]
            youtubers[key]["latest_post_image"] = post_data[0]["image"]
            youtubers[key]["latest_post_time"] = post_data[0]["time"]

            os.remove("save/community_text.json")


    with open(saving_to, 'w') as f:
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