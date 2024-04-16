from pytube import YouTube, exceptions
from moviepy.editor import *
import pandas as pd
import regex as re

def timestamp_to_seconds(timestamp):
    [hours, minutes, seconds] = timestamp.split(":")
    hours_to_seconds = int(hours)*60*60
    minutes_to_seconds = int(minutes)*60
    total = hours_to_seconds + minutes_to_seconds + int(seconds)
    return total

def seconds_to_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def on_complete(path):
    print(path)

def download_video_by_id(youtube_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={youtube_id}', use_oauth=True, allow_oauth_cache=True)
    filename=str(youtube_id).replace(" ", "_") + ".mp4"
    filename = re.sub(r'[^\w\-_\. ]', '_', filename)
    stream = yt.streams.get_audio_only()
    output_path = stream.download('downloaded', filename=filename)
    return output_path

def cut_video(path_to_video, start, duration):
    output = path_to_video.replace("downloaded", "edited")
    start = seconds_to_timestamp(start)
    duration = seconds_to_timestamp(duration)
    command = f"ffmpeg -i {path_to_video} -ss {start} -t {duration} -c:a copy {output}"
    os.system(command=command)
    converted_path = output.replace("mp4", "mp3")
    os.system(f"ffmpeg -i {output} {converted_path}")
    os.remove(output)
    os.remove(path_to_video)

def download_and_cut_video(youtube_id, start):
    print('Downloading...')
    input = download_video_by_id(youtube_id=youtube_id)
    print('Cutting...')
    cut_video(input, start=start, duration=10)
    print('Done!')

dataset = pd.read_csv("musiccaps-public.csv")
dataset = dataset.loc[:, ['ytid', 'start_s']]

number_of_videos_to_download = 100
number_of_failed_downloads = 0
for i in range(0,number_of_videos_to_download+1):
    print(f"Downloading video {i}/{number_of_videos_to_download}")
    try:
        for path, directories, files in os.walk('C:/Users/marti/Documents/Exjobb/AudioLM/Musiccaps/edited'):
            if dataset.loc[i, 'ytid']+'.mp3' not in files:
                download_and_cut_video(dataset.loc[i, 'ytid'], dataset.loc[i, 'start_s'])
            else:
                print("Already downloaded!")
    except (exceptions.AgeRestrictedError, exceptions.VideoUnavailable):
        number_of_failed_downloads += 1
        continue

print(f"Downloads complete! Successfully downloaded {number_of_videos_to_download-number_of_failed_downloads}/{number_of_videos_to_download}")
