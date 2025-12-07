from flask import Flask, render_template
from api.list_videos import list_videos, stream_video  # importer les deux fonctions

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/realisations')
def realisations():
    return render_template('realisations.html')

@app.route('/api/videos')
def api_videos():
    return list_videos()

@app.route('/video/<path:folder>/<filename>')
def api_stream_video(folder, filename):
    return stream_video(folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
