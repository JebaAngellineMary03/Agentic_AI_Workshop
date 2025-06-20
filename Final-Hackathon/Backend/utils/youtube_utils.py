from pytube import YouTube
import os
import subprocess
import yt_dlp

def download_audio_from_youtube(url: str, output_path: str = "audio.mp3") -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "audio.mp3"

def get_youtube_metadata(url: str) -> dict:
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "length_seconds": info.get("duration"),
            "channel": info.get("uploader"),
            "publish_date": info.get("upload_date"),
        }