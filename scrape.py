"""
 Idea: Take three passes
 1: Load the youtube URL
    Look through it, and find the transcript
    Find the intro text
    Load that timestamp
 2: Download the youtube video
 3: On completion, cut the youtube video to size.
  {repeat}

"""

import os.path
from youtube_transcript_api import YouTubeTranscriptApi

def getFileTitle(index):
    return(f"Videos/{index}.mp4")

def getYoutubeURL(videoId):
    return(f"https://www.youtube.com/watch?v={videoId}")

# Returns the timestamps of the first instance of a string
def getTimestamps(videoId, string): 
    transcript = YouTubeTranscriptApi.get_transcript(videoId, languages=['en', 'en-GB'])

    for i in transcript:
        if string.lower() in i['text'].lower():
            start = i['start']
            end = round(i['start']+i['duration'], 3)
            return [start,end]

# Open list of URLs
file1 = open('urls.txt', 'r') 
urlFile = file1.readlines() 
    # The command used to get the URLS
    # youtube-dl --get-id https://www.youtube.com/playlist?list=PLzyXKIJyRnnNtfLFSaAf7M52cJ64zzQ0A -i >> urls.txt

# Go through every url in urls.txt
for index, videoId in enumerate(urlFile):
    # Check if we already downloaded this video
    if os.path.isfile(getFileTitle(index)):
        print (getFileTitle(index) + " already exists")
    else:
        try:
            # print(f"\nTime ({videoId.strip()}):",end="\n\t")
            getTimestamps(videoId, 'vsauce')

        except:
            print(f"\nError occured on video {index}: \"{videoId.strip()}\". Continuing.\n")

# Plans:

# The command to download from youtube:
# time ffmpeg -ss $start_point -i "$video_url" -ss $start_point -i "$audio_url" -map 0:v -map 1:a -ss $start_point -t $duration -c:v libx264 -c:a aac gog-vs-triv.mkv

# Needs:
#   start_point
#   duration
#   video_url
#   audio_url

# Audio & Video url is from youtube-dl -g {URL GOES HERE}
# Gives Video, then Audio Stream

        
# https://unix.stackexchange.com/questions/230481/how-to-download-portion-of-video-with-youtube-dl-command

# After we get all of the videos downloaded,
# https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos
# do some tile mosaic with them all together.