#!/bin/bash

set -e

# === BUNDLED INSTALLER FOR WHISPER TRANSCRIBER ===
# Clones repo, sets up Python venv with Python 3.10, installs dependencies, and launches web UI

REPO_URL="https://github.com/msg43/whisper-transcriber.git"
PROJECT_DIR="$HOME/whisper-transcriber"
PYTHON_PATH="/opt/homebrew/bin/python3.10"

# 1. Clone or update the repository
if [ ! -d "$PROJECT_DIR" ]; then
  echo "📥 Cloning project into $PROJECT_DIR..."
  git clone "$REPO_URL" "$PROJECT_DIR"
else
  echo "📁 Updating existing project in $PROJECT_DIR..."
  cd "$PROJECT_DIR"
  git pull
fi

cd "$PROJECT_DIR"

# 2. Ensure Python 3.10 is installed
if [ ! -f "$PYTHON_PATH" ]; then
  echo "🔧 Installing Python 3.10 via Homebrew..."
  brew install python@3.10
fi

# 3. Clean up any existing virtual environment
if [ -d "whisper-env" ]; then
  echo "🧹 Removing existing virtual environment..."
  rm -rf whisper-env
fi

# 4. Set up virtual environment with Python 3.10
echo "🐍 Creating virtual environment with Python 3.10..."
"$PYTHON_PATH" -m venv whisper-env

source whisper-env/bin/activate

# 5. Install or upgrade dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install torch torchvision torchaudio openai-whisper yt-dlp flask pandas tqdm chart-studio xlsxwriter

# 6. Create folders if missing
mkdir -p transcripts audio

# 7. Launch web UI
echo "🚀 Starting the transcription web interface..."
python3 web_ui.py
