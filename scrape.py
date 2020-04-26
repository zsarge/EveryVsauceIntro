import os.path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_dl import YoutubeDL
from ffmpy import FFmpeg

# To change the videos this program downloads,
# change the video keys in urls.txt

# Start downloading [offset] seconds before the string.
offset = 1
# The seconds of video to download.
length = 7

def loadErrorFile():
    errorFile = open('errors.txt', 'a') 
    errorFile.write("\n---------- new instance ----------\n")
    errorFile.close()  

def writeError(videoId, string="unknown error"):
    errorFile = open('errors.txt', 'a') 
    errorFile.write(f"Error with video \"{videoId.strip()}\".\n")
    errorFile.write(f"\t> {string}\n")
    errorFile.write(f"\tContinuing.\n\n")
    errorFile.close()

def getFileTitle(index):
    return(f"Videos/{index}.mkv")

def getYoutubeURL(videoId):
    return(f"https://www.youtube.com/watch?v={videoId}")

# Returns the timestamps of the first instance of a string
def getTimestamps(videoId, string): 
    transcript = YouTubeTranscriptApi.get_transcript(videoId, languages=['en', 'en-GB'])

    for i in transcript:
        if string.lower() in i['text'].lower():
            # Move start back one second to get the "Hey" in front of "Vsauce"
            start = (i['start'] - offset) if (i['start'] - offset) > 0 else i['start']
            duration = i['duration']
            return [start, duration] 
            # return a list to make selecting just the quoted part easy
    
    writeError(videoId, "String not found in transcript.")
    raise ValueError

def loadVideo(url):
    with YoutubeDL() as ydl:
        return ydl.extract_info(url, download=False)

def getVideoStream(info_dict):
    url = ''
    maxWidth = 0
    # Find the widest video only stream
    for value in info_dict['formats']:
        if value['acodec'] == 'none':
            if value['width'] > maxWidth:
                url = value['url']
    return url

def getAudioStream(info_dict):
    # Audio quality doesn't matter as much,
    # so return the first audio only stream.
    for value in info_dict['formats']:
        if value['vcodec'] == 'none':
            return value['url']

def downloadStreams(vidURL, audURL, startPoint, duration, filename):
    """
    This combines the video and audio streams directly, and clips
    the output to the duration, because youtube-dl doesn't have
    a built in function for that, so the full video would be downloaded 
    every time. This way, we only download part of the video.
    """
    ff = FFmpeg(
        inputs={
            f"{vidURL}" : ['-ss', f"{startPoint}", '-t', f"{duration}"],
            f"{audURL}" : ['-ss', f"{startPoint}", '-t', f"{duration}"]
        },
        outputs={
            f"{filename}": ['-map', '0:v:0', '-map', '1:a:0', '-y']
        }
    )

    ff.run()

# _________________Script that excecutes:__________________________
loadErrorFile()
# Open list of URLs
file1 = open('urls.txt', 'r') 
urlFile = file1.readlines() 
    # The command used to get the URLs: (We don't want to have to load this every time)
    # youtube-dl --get-id https://www.youtube.com/playlist?list=PLzyXKIJyRnnNtfLFSaAf7M52cJ64zzQ0A -i >> urls.txt
    # Urls like bA32J-dmtC4 and R3unPcJDbCc have been ignored, because he doesn't say the intro.

# Go through every url in urls.txt
for index, videoId in enumerate(urlFile):
    # Check if we already downloaded this video
    if os.path.isfile(getFileTitle(index)):
        print (getFileTitle(index) + " already exists")
    else:
        try:
            # print(f"\nTime ({videoId.strip()}):",end="\n\t")
            timestamps = getTimestamps(videoId, 'vsauce')

            info_dict = loadVideo(getYoutubeURL(videoId))
            vidURL = getVideoStream(info_dict)
            audURL = getAudioStream(info_dict)
            
            downloadStreams(vidURL, audURL, timestamps[0], length, getFileTitle(index))

        except:
            print(f"\nError occured on video {index}: \"{videoId.strip()}\". Continuing.\n")
            writeError(videoId)

file1.close()

# Plans:

# After we get all of the videos downloaded,
# https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos
# do some tile mosaic with them all together.