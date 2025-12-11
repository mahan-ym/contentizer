import ffmpeg

def probe(video_path):
    probe_result = ffmpeg.probe(video_path)
    return probe_result

def trim(video_path, output_path, start, end):
    pass

def seek():
    pass