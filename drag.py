from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



def search_music_video(query):
    try:
        # Search for music videos on YouTube
        response = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            videoCategoryId='10',  # Category ID for music
            maxResults=1
        ).execute()

        if response['items']:
            # Get the URL of the first video result
            video_id = response['items'][0]['id']['videoId']
            return video_id
        else:
            return "No video found"

    except HttpError as e:
        return "No video found"


def fetch_comments(video_id, count):
    response = youtube.videos().list(part="snippet", id=video_id).execute()
    video_title = response['items'][0]['snippet']['title']
    artist_name = video_title.split(' - ')[0] if ' - ' in video_title else 'Unknown Artist'

    try:
        comments = []
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            order="relevance",
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        return {"name": video_title, "comments": comments, "artist" : artist_name}

    except HttpError as e:
        if count == 0:
            search_query = f'{video_title} music video'
            music_video_id = search_music_video(search_query)
            if music_video_id != "No video found":
                return fetch_comments(music_video_id, 1)
            else:
                return {"name": "", "comments": "", "artist" : ""}
        else:
            return {"name": "", "comments": "", "artist" : ""}


def get_playlist_items(youtube, playlist_id, max_results=100):
    video_urls = []
    next_page_token = None

    while len(video_urls) < max_results:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=min(max_results - len(video_urls), 50),  # Fetch up to 50 results at a time
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video IDs from the response and generate URLs
        for item in response.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_urls.append(video_url)

            if len(video_urls) >= max_results:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_urls
