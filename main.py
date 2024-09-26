from drag import youtube as y, get_playlist_items, fetch_comments
from chatgpt import get_gpt_result
import json

from collections import OrderedDict

f = open("playlist.txt", 'r')
lines = f.readlines()

for line in lines:
    line = line.strip()
    URL = line.split(', ')[0]
    number = int(line.split(', ')[1])
    playlist_id = URL.split('=')[-1]
    video_urls = get_playlist_items(y, playlist_id)
    count = 0

    for url in video_urls:
        video_id = url.split('=')[-1]
        result = fetch_comments(video_id, 0)
        file_data = OrderedDict()
        if result["name"] == "":
            continue
        file_data["songName"] = result["name"]
        file_data["artist"] = result["artist"]
        print(result["name"])
        print(result["artist"])
        file_data["keywords"] = get_gpt_result(result["name"], result["comments"])
        with open('library.json', 'a', encoding = "utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
        count += 1

        if count == number:
            break

f.close()
