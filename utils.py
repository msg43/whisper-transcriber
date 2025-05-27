import os
import re
import yt_dlp
import subprocess
from urllib.parse import urlparse, parse_qs
from whisper import load_model, transcribe

AUDIO_DIR = "audio"

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
        "force_generic_extractor": True,
    }
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if "entries" in info:
            for entry in info["entries"]:
                if entry and "url" in entry and "title" in entry:
                    full_url = f"https://www.youtube.com/watch?v={entry['url']}"
                    videos.append((full_url, entry["title"]))
    return videos

def download_audio(video_url, output_path):
    """Download the audio of a single YouTube video as WAV."""
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
    """Download and transcribe a video using Whisper."""
    video_id, audio_path = download_audio(video_url, audio_dir)
    model = load_model("base")

    print(f"🧠 Transcribing {video_id}...")
    result = model.transcribe(audio_path)

    # Save multiple formats
    base = os.path.join(output_dir, video_id)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(result["text"])

    with open(base + ".json", "w", encoding="utf-8") as f:
        import json
        json.dump(result, f, indent=2)

    with open(base + ".srt", "w", encoding="utf-8") as f:
        f.write(result["segments"][0].get("text", ""))  # Simplified

    with open(base + ".vtt", "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n" + result["segments"][0].get("text", ""))  # Simplified
