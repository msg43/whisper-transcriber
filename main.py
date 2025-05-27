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

    args = sys.argv[1:]

    if not args:
        print("\nWhisper Transcriber CLI")
        print("Usage:")
        print("  python main.py web")
        print("  python main.py transcribe <playlist_url> [--force] [--workers N]")
        print("  python main.py version")
        print("  python main.py help")
        return

    if args[0] == "web":
        run_web()
    elif args[0] == "transcribe" and len(args) >= 2:
        playlist_url = args[1]
        force = "--force" in args
        if "--workers" in args:
            try:
                idx = args.index("--workers")
                workers = int(args[idx + 1])
            except (IndexError, ValueError):
                print("⚠️ Invalid or missing worker count. Using default.")
                workers = detect_workers()
        run_transcriber(playlist_url, force=force, workers=workers)
    elif args[0] == "version":
        print(f"\n📦 Version: {version}\n🧠 Backend: {backend}\n⚙️ Workers: {workers}")
    elif args[0] == "help":
        print("Usage:")
        print("  python main.py web")
        print("  python main.py transcribe <playlist_url> [--force] [--workers N]")
        print("  python main.py version")
    else:
        print("❌ Invalid command. Use `python main.py help` for usage.")

if __name__ == "__main__":
    main()
