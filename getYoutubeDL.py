import youtube_dl
import os
import sys
import requests
import json
path = "./video/video.mp4"

def getVideo(url):
    if (os.path.exists(path)):
        os.remove(path)
        print("Removed old video!")
    ydl_opts = {'outtmpl': path}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    getVideo()