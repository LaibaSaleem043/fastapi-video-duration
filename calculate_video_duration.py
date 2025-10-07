# from fastapi import FastAPI
# from pydantic import BaseModel
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from typing import List


# app = FastAPI()

# class VideoClip(BaseModel):
#     url: str

# videos: List[VideoClip] = []

# @app.get("/")
# def welcome_message():
#     return {"message": "Welcome To calculate video duration api."}

# @app.post("/videos")
# def calculate_duration(video: VideoClip):
#     clip = VideoFileClip(video.url)
#     duration = clip.duration
#     return {"url": video.url,
#         "duration_seconds": duration}

from fastapi import FastAPI
from pydantic import BaseModel
from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
import tempfile
import os

app = FastAPI()


class VideoClip(BaseModel):
    url: str


@app.get("/")
def welcome_message():
    return {"message": "Welcome To calculate video duration API."}


@app.post("/videos")
def calculate_duration(video: VideoClip):
    try:
        # Download the video file from the URL
        response = requests.get(video.url, stream=True)
        if response.status_code != 200:
            return {"error": "Unable to download video. Status code: " + str(response.status_code)}

        # Save video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp_path = tmp.name

        # Open video with MoviePy
        clip = VideoFileClip(tmp_path)
        duration = clip.duration
        clip.close()

        # Clean up temp file
        os.remove(tmp_path)

        return {
            "url": video.url,
            "duration_seconds": duration
        }

    except Exception as e:
        return {"error": str(e)}
