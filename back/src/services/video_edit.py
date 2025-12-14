import os
import ffmpeg
import subprocess
import json
from src.global_constants import ASSETS_DIR, THUMBNAILS_DIR


def probe(video_path):
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        probe_result = ffmpeg.probe(full_path)
    except ffmpeg.Error as e:
        print(f"An error occurred while probing the video: {e}")
        return None
    return probe_result


def get_video_duration(video_path):
    """Get video duration in seconds"""
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        probe_result = ffmpeg.probe(full_path)
        duration = float(probe_result["format"]["duration"])
        return duration
    except ffmpeg.Error as e:
        print(f"An error occurred while getting video duration: {e}")
        return 0.0


def get_video_metadata(video_path):
    """Get comprehensive video metadata including duration, resolution, fps"""
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        probe_result = ffmpeg.probe(full_path)
        video_stream = next(
            (
                stream
                for stream in probe_result["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )

        if not video_stream:
            return None

        return {
            "duration": float(probe_result["format"]["duration"]),
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "fps": eval(video_stream.get("r_frame_rate", "30/1")),
            "codec": video_stream.get("codec_name", "unknown"),
        }
    except ffmpeg.Error as e:
        print(f"An error occurred while getting video metadata: {e}")
        return None


def gen_thumbnail(video_path):
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        # Generate thumbnail directly in the thumbnails directory
        thumbnail_path = os.path.join(
            THUMBNAILS_DIR, f"{os.path.basename(video_path)}.jpg"
        )

        # Ensure thumbnails directory exists
        os.makedirs(THUMBNAILS_DIR, exist_ok=True)

        ffmpeg.input(full_path, ss="00:00:01").filter("scale", 1280, -1).output(
            thumbnail_path, vframes=1
        ).run(overwrite_output=True)

        return thumbnail_path
    except ffmpeg.Error as e:
        print(f"An error occurred while generating thumbnail: {e}")
        return "https://placehold.co/400"


def trim(video_path, output_path, start, end):
    try:
        full_path = os.path.join(ASSETS_DIR, video_path)
        ffmpeg.input(full_path).trim(start=start, end=end).setpts(
            "PTS-STARTPTS"
        ).output(output_path).run()
    except ffmpeg.Error as e:
        print(f"An error occurred while trimming the video: {e}")


def concatenate_videos(video_paths, output_path):
    """Concatenate multiple videos in sequence"""
    try:
        # Create a temporary file list for ffmpeg concat
        concat_file_path = os.path.join(ASSETS_DIR, "concat_list.txt")

        with open(concat_file_path, "w") as f:
            for video_path in video_paths:
                full_path = os.path.join(ASSETS_DIR, video_path)
                # Escape single quotes in the path
                escaped_path = full_path.replace("'", "'\\\\''")
                f.write(f"file '{escaped_path}'\n")

        # Use ffmpeg concat demuxer
        output_full_path = os.path.join(ASSETS_DIR, output_path)

        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_file_path,
                "-c",
                "copy",
                output_full_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Clean up temp file
        os.remove(concat_file_path)

        return output_full_path
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while concatenating videos: {e.stderr}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def add_video_to_sequence(existing_videos, new_video_path):
    """Calculate the start time for adding a new video after existing ones"""
    total_duration = 0.0
    for video in existing_videos:
        duration = get_video_duration(video["track_location"])
        total_duration += duration

    return total_duration


def seek():
    pass
