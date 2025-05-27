import os
import re
import yt_dlp
import subprocess
from urllib.parse import urlparse, parse_qs

AUDIO_DIR = "audio"
WHISPER_CPP_PATH = os.path.expanduser("~/whisper.cpp/build/bin")  # Path to whisper.cpp folder
WHISPER_MODEL = "../models/ggml-medium.en.bin"               # Relative to WHISPER_CPP_PATH

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().lower())

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in {"www.youtube.com", "youtube.com"}:
        qs = parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    return None

def get_playlist_videos(playlist_url):
    """Return a list of (video_url, title) from a playlist."""
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": False  # ✅ proper extractor
    }
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if "entries" in info:
            for entry in info["entries"]:
                if entry and "url" in entry and "title" in entry:
                    url = entry["url"]
                    if not url.startswith("http"):
                        url = f"https://www.youtube.com/watch?v={url}"
                    videos.append((url, entry["title"]))
    return videos

def download_audio(video_url, output_path):
    """Download audio from a YouTube video using yt-dlp + ffmpeg."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_path, "%(id)s.%(ext)s"),
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return info["id"], os.path.join(output_path, f"{info['id']}.wav")

def transcribe_video(video_url, output_dir, audio_dir):
    """Transcribe a YouTube video using whisper.cpp."""
    video_id, audio_path = download_audio(video_url, audio_dir)

    output_base = os.path.join(output_dir, video_id)
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎙️ Transcribing {video_id} using whisper.cpp...")
    cmd = [
        os.path.join(WHISPER_CPP_PATH, "main"),
        "-m", os.path.join(WHISPER_CPP_PATH, WHISPER_MODEL),
        "-f", audio_path,
        "-of", output_base,
        "-otxt", "-osrt", "-ovtt"
    ]
    subprocess.run(cmd, check=True)
