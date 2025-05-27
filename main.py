import os
import subprocess
import sys

VERSION_FILE = "VERSION"

def get_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE) as f:
            return f.read().strip()
    return "unknown"

def detect_backend():
    return os.environ.get("WHISPER_BACKEND", "torch")

def detect_workers():
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except:
        return 4

def run_web():
    print("🚀 Launching web interface...")
    subprocess.run(["python3", "web_ui.py"])

def run_transcriber(playlist_url, force=False, workers=None):
    cmd = ["python3", "transcribe.py"]
    if force:
        cmd.append("--force")
    if workers:
        cmd += ["--workers", str(workers)]
    os.environ["PLAYLIST_URL"] = playlist_url
    subprocess.run(cmd)

def main():
    version = get_version()
    backend = detect_backend()
    workers = detect_workers()

    while True:
        print("\n🎛️ Whisper Transcriber Menu")
        print("----------------------------")
        print("1. Launch Web Interface")
        print("2. Run Transcription from Playlist URL")
        print("3. Force Reprocess Playlist")
        print("4. View Current Version")
        print("5. Exit")

        choice = input("Choose an option (1–5): ").strip()

        if choice == "1":
            run_web()
        elif choice == "2":
            url = input("Enter YouTube Playlist URL: ").strip()
            run_transcriber(url, force=False, workers=workers)
        elif choice == "3":
            url = input("Enter YouTube Playlist URL: ").strip()
            run_transcriber(url, force=True, workers=workers)
        elif choice == "4":
            print(f"\n📦 Version: {version}\n🧠 Backend: {backend}\n⚙️ Workers: {workers}")
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
