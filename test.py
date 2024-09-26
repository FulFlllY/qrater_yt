from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey='AIzaSyDl-zKEBOx6TAeEZAnX3But1XunhDPOYNA')


def get_video_title(video_url):
    try:
        # Extract the video ID from the URL
        video_id = video_url.split('v=')[-1]

        # Use the YouTube API to get video details
        response = youtube.videos().list(part="snippet", id=video_id).execute()

        # Extract the video title from the response
        video_title = response['items'][0]['snippet']['title']
        return video_title

    except HttpError as e:
        return f"An HTTP error occurred: {e}"


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
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            return video_url
        else:
            return "No video found"

    except HttpError as e:
        return f"An HTTP error occurred: {e}"


# Example URL of the original YouTube video
song_url = 'https://www.youtube.com/watch?v=qAqXDZoa624'

# Get the song title from the provided link
song_title = get_video_title(song_url)

# Generate the corresponding music video search query
search_query = f'{song_title} music video'

# Search for the music video URL
music_video_url = search_music_video(search_query)

print(f"Music Video URL: {music_video_url}")
