# Changelog

## v1.2.0 (Current Release)
- ✅ Rewrote `main.py` to avoid interactive input() and support CLI flags
- ✅ Added `--workers` and `--force` options to CLI and native launcher
- ✅ Auto-detects CPU/GPU and tunes worker count accordingly
- ✅ Implemented `install.sh` with Python 3.10 enforcement via Homebrew
- ✅ Full Flask-based web UI with progress feedback
- ✅ Added metadata CSV + charts + export via browser
- ✅ Created `run_transcriber_native.sh` to support CLI and Web UI entrypoints
- ✅ GitHub-ready structure with README, VERSION, install script

## v1.1.0
- Added duplicate transcript detection
- Implemented logic to retry or reprocess incomplete transcripts
- Generated `summary_log.csv` output and logic for safe overwriting
- Whisper backend now configurable (Torch vs whisper.cpp)
- Refined playlist parsing and download helpers in `utils.py`

## v1.0.0
- Initial release
- Basic `transcribe.py` for looping over playlist
- Added video/audio file handling
- Whisper transcription to `.txt`, `.srt`, `.vtt`, and `.json`
- CLI with Python virtual environment support
