import ffmpeg


def probe(video_path):
    try:
        probe_result = ffmpeg.probe(video_path)
    except ffmpeg.Error as e:
        print(f"An error occurred while probing the video: {e}")
        return None
    return probe_result


def gen_thumbnail(video_path):
    ffmpeg.input(video_path, ss="00:00:01").filter("scale", 1280, -1).output(
        "thumbnail.jpg", vframes=1
    ).run()


def trim(video_path, output_path, start, end):
    try:
        ffmpeg.input(video_path).trim(start=start, end=end).setpts(
            "PTS-STARTPTS"
        ).output(output_path).run()
    except ffmpeg.Error as e:
        print(f"An error occurred while trimming the video: {e}")


def seek():
    pass
