import os.path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_dl import YoutubeDL
from ffmpy import FFmpeg

def writeError(fileNumber):
    errorFile = open('errors.txt', 'a') 
    errorFile.write(f"Error on file {fileNumber}\n")
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
            start = i['start']
            duration = i['duration']
            return [start, duration]

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
    ff = FFmpeg(
        inputs={
            f"{vidURL}" : ['-ss', f"{startPoint}"],
            f"{audURL}" : ['-ss', f"{startPoint}"]
        },
        outputs={
            f"{filename}": ['-map', '0:v', '-map', '1:a', '-ss', f"{startPoint}", '-t', f"{duration}", "-c:v", "libx264", "-c:a", "aac"]
        }
    )

    ff.run()

# ___________________________________________
# Open list of URLs
file1 = open('urls.txt', 'r') 
urlFile = file1.readlines() 
    # The command used to get the URLs: (We don't want to have to load this every time)
    # youtube-dl --get-id https://www.youtube.com/playlist?list=PLzyXKIJyRnnNtfLFSaAf7M52cJ64zzQ0A -i >> urls.txt

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
            
            downloadStreams(vidURL, audURL, timestamps[0], timestamps[1], getFileTitle(index))

        except:
            print(f"\nError occured on video {index}: \"{videoId.strip()}\". Continuing.\n")
            writeError(index)

file1.close()

# Plans:

# The command to download from youtube:
# ffmpeg -ss $start_point -i "$video_url" -ss $start_point -i "$audio_url" -map 0:v -map 1:a -ss $start_point -t $duration -c:v libx264 -c:a aac test.mkv

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