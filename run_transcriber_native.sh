#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_DIR="$PROJECT_DIR/whisper-env"
PYTHON_BIN="/opt/homebrew/bin/python3.10"

# Activate virtual environment
if [ ! -d "$ENV_DIR" ]; then
  echo "❌ Virtual environment not found. Run install.sh first."
  exit 1
fi

source "$ENV_DIR/bin/activate"

# Defaults
FORCE_FLAG=""
WORKERS=""
PLAYLIST_URL=""
USE_WEB=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE_FLAG="--force"
      shift
      ;;
    --workers)
      WORKERS="--workers $2"
      shift 2
      ;;
    --playlist)
      PLAYLIST_URL="$2"
      shift 2
      ;;
    --web)
      USE_WEB=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage:"
      echo "  ./run_transcriber_native.sh --playlist <url> [--force] [--workers N]"
      echo "  ./run_transcriber_native.sh --web"
      exit 1
      ;;
  esac
done

# Launch web or CLI
if $USE_WEB; then
  echo "🚀 Launching Web UI..."
  python main.py web
elif [ -n "$PLAYLIST_URL" ]; then
  echo "🎬 Running CLI transcriber..."
  python main.py transcribe "$PLAYLIST_URL" $FORCE_FLAG $WORKERS
else
  echo "❌ No playlist URL provided and --web not used."
  echo "Usage:"
  echo "  ./run_transcriber_native.sh --playlist <url> [--force] [--workers N]"
  echo "  ./run_transcriber_native.sh --web"
  exit 1
fi
