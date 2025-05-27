from flask import Flask, request, render_template_string, jsonify
import subprocess
import os

app = Flask(__name__)
VERSION = "v1.2.0"

HTML_TEMPLATE = """
<!doctype html>
<title>Whisper Transcriber</title>
<h2>🎤 Whisper Playlist Transcriber</h2>
<form method="POST">
    <label>Playlist URL:</label><br>
    <input type="text" name="url" style="width: 400px" required><br><br>

    <label>Force Reprocess?</label>
    <input type="checkbox" name="force"><br><br>

    <label>Worker Count:</label>
    <input type="number" name="workers" value="4" min="1" max="16"><br><br>

    <input type="submit" value="Transcribe">
</form>

{% if status %}
<hr>
<h3>🚀 Status:</h3>
<pre>{{ status }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    if request.method == "POST":
        url = request.form["url"]
        force = "--force" if "force" in request.form else ""
        workers = request.form.get("workers", "4")

        os.environ["PLAYLIST_URL"] = url
        cmd = f"python3 transcribe.py --playlist \"{url}\" --workers {workers} {force}"
        try:
            status = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            status = f"Error: {e.output}"

    return render_template_string(HTML_TEMPLATE, status=status)

@app.route("/version")
def version():
    return jsonify({"version": VERSION})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
