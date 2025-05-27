import os
import re
import yt_dlp
import subprocess
from urllib.parse import urlparse, parse_qs

AUDIO_DIR = "audio"
WHISPER_CPP_PATH = os.path.expanduser("~/whisper.cpp/build/bin")
WHISPER_BINARY = "whisper-cli"
WHISPER_MODEL = "/Users/matthewgreer/whisper.cpp/models/ggml-medium.en.bin"

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().lower())

def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in {"www.youtube.com", "youtube.com"}:
        qs = parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    return None

def get_playlist_videos(playlist_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": False
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
    """Download audio and convert to mono WAV using ffmpeg manually."""
    os.makedirs(output_path, exist_ok=True)

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
        video_id = info["id"]
        raw_path = os.path.join(output_path, f"{video_id}.wav")
        mono_path = os.path.join(output_path, f"{video_id}_mono.wav")

        # Convert to mono and 16kHz
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_path,
            "-ac", "1", "-ar", "16000",
            mono_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return video_id, mono_path

def transcribe_video(video_url, output_dir, audio_dir):
    video_id, audio_path = download_audio(video_url, audio_dir)
    output_base = os.path.join(output_dir, video_id)
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎙️ Transcribing {video_id} using whisper-cli...")
    cmd = [
        os.path.join(WHISPER_CPP_PATH, WHISPER_BINARY),
        "-m", WHISPER_MODEL,
        "-f", audio_path,
        "-of", output_base,
        "-otxt", "-osrt", "-ovtt"
    ]
    subprocess.run(cmd, check=True)
