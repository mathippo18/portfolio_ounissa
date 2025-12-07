from flask import Flask, render_template
from api.list_videos import list_videos  # importe la fonction depuis le module api.list_videos

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/realisations')
def realisations():
    return render_template('realisations.html')

@app.route('/api/videos')
def api_videos():
    return list_videos()  # maintenant Flask connaît list_videos

if __name__ == "__main__":
    app.run(debug=True)
