import os
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils import get_video_id, transcribe_video, get_playlist_videos

OUTPUT_DIR = "transcripts"
AUDIO_DIR = "audio"

def already_processed(video_id):
    required = [".txt", ".srt", ".vtt", ".json"]
    return all(os.path.exists(os.path.join(OUTPUT_DIR, f"{video_id}{ext}")) for ext in required)

def transcribe_single(video, force):
    url, title = video
    video_id = get_video_id(url)
    print(f"🔍 Checking {title} ({video_id})")

    if not force and already_processed(video_id):
        print(f"✅ Already done: {video_id}")
        return video_id, "skipped"

    try:
        transcribe_video(url, OUTPUT_DIR, AUDIO_DIR)
        return video_id, "transcribed"
    except Exception as e:
        print(f"❌ Failed {video_id}: {e}")
        return video_id, "failed"

def main():
    parser = argparse.ArgumentParser(description="Transcribe YouTube playlist with Whisper")
    parser.add_argument("--playlist", required=False, help="YouTube playlist URL (or set PLAYLIST_URL env)")
    parser.add_argument("--force", action="store_true", help="Force reprocessing even if already completed")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel processes")
    args = parser.parse_args()

    playlist_url = args.playlist or os.environ.get("PLAYLIST_URL")
    if not playlist_url:
        print("❌ No playlist URL provided.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    videos = get_playlist_videos(playlist_url)
    print(f"📋 Found {len(videos)} videos in playlist.")

    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(transcribe_single, v, args.force) for v in videos]
        for future in as_completed(futures):
            video_id, status = future.result()
            results.append((video_id, status))

    print("\n📊 Summary:")
    for vid, status in results:
        print(f"{vid}: {status}")

if __name__ == "__main__":
    main()
