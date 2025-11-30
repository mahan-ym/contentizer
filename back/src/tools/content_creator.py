import os
import requests
from dotenv import load_dotenv

# get from environment variables
load_dotenv()
Youtube_API_KEY = os.getenv("Youtube_API_KEY")


def get_youtube_video_categories():
    """This function fetches YouTube video categories."""
    ENDPOINT = "https://youtube.googleapis.com/youtube/v3/videoCategories"
    REGION_CODE = "US"
    params = {"part": "snippet", "regionCode": REGION_CODE, "key": Youtube_API_KEY}

    response = requests.get(ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        categories = {}
        for item in data.get("items", []):
            category_id = item["id"]
            category_title = item["snippet"]["title"]
            categories[category_id] = category_title
        return categories


def look_for_youtube_trends(keyword: str = "0", max_results: int = 10):
    """This function looks the YouTube trends.

    Args:
        keyword (str): The keyword to search for trends. Default is "0" which represents "All Categories" To fetch the other categories, get_youtube_video_categories() function should be called.
        max_results (int): The maximum number of results to return. Default is 10.

    Example:
        trends = look_for_youtube_trends(keyword="10", max_results=30)
    Returns:
        A list of dictionaries containing trending video information.
    """
    ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
    REGION_CODE = "NL"

    params = {
        "part": "snippet,contentDetails,statistics",
        "chart": "mostPopular",
        "regionCode": REGION_CODE,
        "maxResults": max_results,
        "videoCategoryId": keyword,
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


# if __name__ == "__main__":
#     print(look_for_youtube_trends())
