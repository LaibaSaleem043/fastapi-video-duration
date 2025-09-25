from fastapi import FastAPI
from pydantic import BaseModel
from moviepy.video.io.VideoFileClip import VideoFileClip
from typing import List


app = FastAPI()

class VideoClip(BaseModel):
    url: str

videos: List[VideoClip] = []

@app.get("/")
def welcome_message():
    return{"message": "Welcome To calculate video duration api"}

@app.post("/videos")
def calculate_duration(video: VideoClip):
    clip = VideoFileClip(video.url)
    duration = clip.duration
    return {"url": video.url,
        "duration_seconds": duration}

