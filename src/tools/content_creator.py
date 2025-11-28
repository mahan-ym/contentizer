import os
import requests
from dotenv import load_dotenv

# get from environment variables
load_dotenv()
Youtube_API_KEY = os.getenv("Youtube_API_KEY")


def look_for_youtube_trends():
    """This function looks the YouTube trends."""
    ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
    REGION_CODE = "US"

    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": REGION_CODE,
        "maxResults": 10,
        "key": Youtube_API_KEY,
    }

    response = requests.get(ENDPOINT, params=params)

    if response.status_code == 200:
        data = response.json()
        trends = []
        for item in data.get("items", []):
            video_info = {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "tags": item["snippet"].get("tags", []),
                "publishedAt": item["snippet"]["publishedAt"],
                "channel": item["snippet"]["channelTitle"],
                "views": item["statistics"].get("viewCount", "N/A"),
                "likes": item["statistics"].get("likeCount", "N/A"),
                "comments": item["statistics"].get("commentCount", "N/A"),
            }
            trends.append(video_info)
        return trends
    else:
        print(f"Error fetching data from YouTube API: {response.status_code}")
        return None


if __name__ == "__main__":
    print(look_for_youtube_trends())
