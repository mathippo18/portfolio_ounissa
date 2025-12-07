import os
from pathlib import Path
from vercel_py import VercelRequest, VercelResponse

VALID_EXT = {".mp4", ".mov", ".webm", ".m4v"}

def handler(request: VercelRequest) -> VercelResponse:
    root = Path("public/videos")

    if not root.exists():
        return VercelResponse.json({"error": "videos folder not found"}, status=404)

    output = []

    # Parcourt tous les sous-dossiers
    for folder in root.rglob("*"):
        if folder.is_dir():
            videos = [
                str(f.relative_to(root)) 
                for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in VALID_EXT
            ]

            if videos:
                output.append({
                    "folder": str(folder.relative_to(root)),
                    "videos": videos
                })

    return VercelResponse.json(output)
