import json
import requests
from bs4 import BeautifulSoup
import os


def add_channel(link):
    youtube_channels = {}
    try:
        with open("save/followed_youtube_channels.json") as f:
            youtube_channels = json.load(f)

        name = link.split('/')[-1]

        if name not in youtube_channels:
            youtube_channels[name] = {}

        youtube_channels[name]["channel"] = link
        youtube_channels[name]["community"] = f"{link}/community"
        youtube_channels[name]["videos"] = f"{link}/videos"
        youtube_channels[name]["latest_post_link"] = ""
        youtube_channels[name]["latest_post_poster"] = ""
        youtube_channels[name]["latest_post_text"] = ""
        youtube_channels[name]["latest_post_image"] = ""
        youtube_channels[name]["latest_post_time"] = ""
        youtube_channels[name]["latest_video_link"] = ""
        youtube_channels[name]["latest_video_title"] = ""
        youtube_channels[name]["latest_video_time"] = ""

        with open("save/followed_youtube_channels.json", 'w') as f:
            json.dump(youtube_channels, f)

        with open("save/youtube_update_loader.json", 'w') as f:
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


def get_latest_post():
    youtube_update("save/followed_youtube_channels.json")
    youtube_channels = {}

    with open("save/followed_youtube_channels.json") as f:
        youtube_channels = json.load(f)
    
    text = []

    for key in youtube_channels.keys():
        temp_list = []
        
        temp_list.append(f"貼文: {youtube_channels[key]['latest_post_poster']}({youtube_channels[key]['latest_post_time']})\n{youtube_channels[key]['latest_post_text']}")
        temp_list.append(youtube_channels[key]["latest_post_image"])
        temp_list.append(youtube_channels[key]["latest_post_link"] + "\n----------")

        text.append(temp_list)

    return text


def get_latest_video():
    youtube_update("save/followed_youtube_channels.json")
    youtube_channels = {}

    with open("save/followed_youtube_channels.json") as f:
        youtube_channels = json.load(f)
    
    text = []

    for key in youtube_channels.keys():
        temp_list = []
        
        temp_list.append((f"影片: {youtube_channels[key]['latest_post_poster']}({youtube_channels[key]['latest_video_time']})"))
        temp_list.append(youtube_channels[key]["latest_video_title"])
        temp_list.append(youtube_channels[key]["latest_video_link"])
        temp_list.append("----------")

        text.append('\n'.join(temp_list))

    return text


def check_latest():
    youtube_update("save/youtube_update_loader.json")
    new_youtube_channels = {}
    old_youtube_channels = {}

    with open("save/youtube_update_loader.json") as new_f:
        new_youtube_channels = json.load(new_f)

    with open("save/followed_youtube_channels.json") as old_f:
        old_youtube_channels = json.load(old_f)
    
    text = []

    for key in new_youtube_channels.keys():
        temp_list = []
        
        if new_youtube_channels[key]["latest_post_link"] != old_youtube_channels[key]["latest_post_link"]:
            temp_list.append(f"貼文: {new_youtube_channels[key]['latest_post_poster']}({new_youtube_channels[key]['latest_post_time']})\n{new_youtube_channels[key]['latest_post_text']}")
            temp_list.append(new_youtube_channels[key]["latest_post_image"])
            temp_list.append(new_youtube_channels[key]["latest_post_link"] + "\n----------")

            text.append(temp_list)

        elif new_youtube_channels[key]["latest_video_link"] != old_youtube_channels[key]["latest_video_link"]:
            temp_list.append((f"影片: {new_youtube_channels[key]['latest_post_poster']}({new_youtube_channels[key]['latest_video_time']})"))
            temp_list.append(new_youtube_channels[key]["latest_video_title"])
            temp_list.append(new_youtube_channels[key]["latest_video_link"])
            temp_list.append("----------")

            text.append('\n'.join(temp_list))

    if len(text):
        with open("save/followed_youtube_channels.json", 'w') as f:
            json.dump(new_youtube_channels, f)
        return text
    else:
        return False


def youtube_update(saving_to, update_file = "save/youtube_update_loader.json"):
    youtubers = {}
    with open(saving_to) as f:
        youtubers = json.load(f)
        for key in youtubers:
            community_url = youtubers[key]["community"]
            videos_url = youtubers[key]["videos"]
            community_r = requests.get(community_url)
            videos_r = requests.get(videos_url)

            community_soup = BeautifulSoup(community_r.text, 'html.parser')
            videos_soup = BeautifulSoup(videos_r.text, 'html.parser')
            community_tags = community_soup.find_all("script")
            videos_tags = videos_soup.find_all("script")

            community_text = []
            videos_text = []
            post_data = []
            video_data = []

            for community_tag in community_tags:
                community_text.append(community_tag.get_text().strip())

            for videos_tag in videos_tags:
                videos_text.append(videos_tag.get_text().strip())

            with open("save/community_text.json", 'w') as f:
                f.write(community_text[-7].strip(";var ytInitialData = "))

            with open("save/videos_text.json", 'w') as f:
                f.write(videos_text[-7].strip(";var ytInitialData = "))

            with open("save/community_text.json") as f:
                data = json.load(f)
                posts = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][3]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

                for post in posts:
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

            with open("save/videos_text.json") as f:
                data = json.load(f)
                videos = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]


                for video in videos:
                    try:
                        prefix = video["gridVideoRenderer"]
                        videoid = prefix["videoId"]
                        title = prefix["title"]["runs"][0]["text"]
                        image_link = prefix["thumbnail"]["thumbnails"][-1]["url"]
                        publish_time = prefix["publishedTimeText"]["simpleText"]

                        video_data_dict = {}
                        video_data_dict["link"] = f"https://www.youtube.com/watch?v={videoid}"
                        video_data_dict["title"] = title
                        video_data_dict["time"] = publish_time
                        video_data.append(video_data_dict)
                    except:
                        pass

            youtubers[key]["latest_post_link"] = post_data[0]["link"]
            youtubers[key]["latest_post_poster"] = post_data[0]["poster"]
            youtubers[key]["latest_post_text"] = post_data[0]["text"]
            youtubers[key]["latest_post_image"] = post_data[0]["image"]
            youtubers[key]["latest_post_time"] = post_data[0]["time"]

            youtubers[key]["latest_video_link"] = video_data[0]["link"]
            youtubers[key]["latest_video_title"] = video_data[0]["title"]
            youtubers[key]["latest_video_time"] = video_data[0]["time"]

            os.remove("save/community_text.json")
            os.remove("save/videos_text.json")


    with open(saving_to, 'w') as f:
        json.dump(youtubers, f)

    with open(update_file, 'w') as f:
        json.dump(youtubers, f)