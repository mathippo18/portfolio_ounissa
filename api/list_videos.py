from flask import Flask, jsonify
from pathlib import Path

app = Flask(__name__)

VALID_EXT = {".mp4", ".mov", ".webm", ".m4v"}

@app.route('/api/videos')
def list_videos():
    root = Path("static/videos")
    if not root.exists():
        return jsonify({"error": "videos folder not found"}), 404

    output = []

    for folder in root.rglob("*"):
        if folder.is_dir():
            videos = [
                str(f.relative_to(root))  # chemin relatif à static/videos
                for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in VALID_EXT
            ]
            if videos:
                output.append({
    "folder": str(folder.relative_to(root)).replace("\\", "/"),  # remplace les backslash
    "videos": [f.name.replace("\\", "/") for f in folder.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXT]
})


    return jsonify(output)
