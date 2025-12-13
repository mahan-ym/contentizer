import os
import ffmpeg
from src.global_constants import ASSETS_DIR


def probe(video_path):
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        probe_result = ffmpeg.probe(full_path)
    except ffmpeg.Error as e:
        print(f"An error occurred while probing the video: {e}")
        return None
    return probe_result


def gen_thumbnail(video_path):
    full_path = os.path.join(ASSETS_DIR, video_path)
    ffmpeg.input(full_path, ss="00:00:01").filter("scale", 1280, -1).output(
        "thumbnail.jpg", vframes=1
    ).run()


def trim(video_path, output_path, start, end):
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        ffmpeg.input(full_path).trim(start=start, end=end).setpts(
            "PTS-STARTPTS"
        ).output(output_path).run()
    except ffmpeg.Error as e:
        print(f"An error occurred while trimming the video: {e}")


def seek():
    pass
