from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route("/mark_video_watched", methods=["POST"])
def mark_video_watched():
    payload = request.form
    video_url = payload["video_url"]
    s = subprocess.run(f'python yt_dlp_tool.py -d "{video_url}"', shell=True)
    print(video_url, s.stdout, s.stderr)
    return "ok", 200


if __name__ == "__main__":
    app.run(debug=False, port=59521, host="0.0.0.0")
