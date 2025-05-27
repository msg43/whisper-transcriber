# 🎤 Whisper Transcriber

A fully automated system for transcribing entire **YouTube playlists** using [OpenAI Whisper](https://github.com/openai/whisper), powered by a modern CLI, native Mac compatibility, and an intuitive web UI.

---

## 🚀 Features

- ✅ Transcribe full YouTube playlists to `.txt`, `.srt`, `.vtt`, and `.json`
- ✅ Use either the web interface or the CLI
- ✅ Detects and skips already-processed videos
- ✅ Parallel processing with `--workers`
- ✅ Force reprocessing with `--force`
- ✅ Supports Torch backend with Apple Silicon acceleration
- ✅ Web UI includes charts, metadata, and export

---

## 🧠 Requirements

- macOS 13+ (Apple Silicon preferred)
- Python 3.10 (installed via Homebrew)
- `ffmpeg`
- `brew`, `git`

---

## ⚙️ One-Line Setup

Just run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/msg43/whisper-transcriber/main/install.sh)"
```

---

## 💻 Manual Setup (if needed)

```bash
git clone https://github.com/msg43/whisper-transcriber.git
cd whisper-transcriber
brew install python@3.10 ffmpeg
/opt/homebrew/bin/python3.10 -m venv whisper-env
source whisper-env/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio openai-whisper yt-dlp flask pandas tqdm chart-studio xlsxwriter
```

---

## 📦 Usage

### ▶️ Web UI

```bash
cd whisper-transcriber
source whisper-env/bin/activate
python main.py web
```

Visit: [http://localhost:5000](http://localhost:5000)

### 🔧 CLI Mode

```bash
python main.py transcribe "https://youtube.com/playlist?list=XYZ" --workers 6 --force
```

### 🛠 Run via helper script

```bash
./run_transcriber_native.sh --web
./run_transcriber_native.sh --playlist "https://..." --workers 4 --force
```

---

## 📁 Output

- Transcripts: `transcripts/*.txt`, `.srt`, `.vtt`, `.json`
- Audio: `audio/*.wav`
- Metadata: `transcripts/summary_log.csv`

---

## 🔁 Reprocessing & Retry Logic

- ✅ Automatically skips completed videos
- 🔄 Will re-run any that failed or were incomplete
- ✅ Use `--force` to re-run everything

---

## 🧪 Development Notes

- `transcribe.py` uses multiprocessing via `--workers`
- Web interface lives in `web_ui.py` (Flask)
- Utilities live in `utils.py` (yt-dlp, ffmpeg, whisper)

---

## 📚 Related

- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Whisper.cpp (optional)](https://github.com/ggerganov/whisper.cpp)

---

## 📦 Version

See [VERSION](./VERSION) and [CHANGELOG.md](./CHANGELOG.md)

---

## 📝 License

MIT © 2025 msg43
