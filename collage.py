from ffmpy import FFmpeg
# Using: https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos

""" My modified command:
ffmpeg
	-i 1.mkv -i 2.mkv -i 3.mkv -i 4.mkv
	-filter_complex "
		nullsrc=size=640x480 [base];
		[0:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft];
		[1:v] setpts=PTS-STARTPTS, scale=320x240 [upperright];
		[2:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft];
		[3:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright];
		[base][upperleft] overlay=shortest=1 [tmp1];
		[tmp1][upperright] overlay=shortest=1:x=320 [tmp2];
		[tmp2][lowerleft] overlay=shortest=1:y=240 [tmp3];
		[tmp3][lowerright] overlay=shortest=1:x=320:y=240;
        amix=inputs=4:duration=first
	"
	-c:v libx264 output.mkv
"""

ff = FFmpeg(
    inputs={
        "Videos/Testing/4vids/1.mkv" : None,
        "Videos/Testing/4vids/2.mkv" : None,
        "Videos/Testing/4vids/3.mkv" : None,
        "Videos/Testing/4vids/4.mkv" : None
    },
    outputs={
        "Videos/Testing/4vids/output.mkv": [ '-filter_complex',
        "nullsrc=size=640x480 [base]; \
         [0:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
         [1:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
         [2:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
         [3:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
         [base][upperleft] overlay=shortest=1 [tmp1]; \
         [tmp1][upperright] overlay=shortest=1:x=320 [tmp2]; \
         [tmp2][lowerleft] overlay=shortest=1:y=240 [tmp3]; \
         [tmp3][lowerright] overlay=shortest=1:x=320:y=240; \
         amix=inputs=4:duration=first",
        '-c:v','libx264'
        ]
    }
)

print(ff.cmd)
ff.run()