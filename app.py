# app.py
from flask import Flask, request, jsonify
import subprocess
import os
import requests

app = Flask(__name__)

HUGGINGFACE_API_KEY = os.getenv("hftoken")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    youtube_url = request.json.get('url')
    if not youtube_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        # Step 1: Download audio using yt-dlp
        filename = "audio.wav"
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "wav",
            "-o", "audio.%(ext)s", youtube_url
        ], check=True)

        # Step 2: Read audio
        with open(filename, "rb") as f:
            audio_data = f.read()

        # Step 3: Send to Hugging Face
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h",
            headers=headers,
            data=audio_data
        )

        os.remove(filename)  # Clean up
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
