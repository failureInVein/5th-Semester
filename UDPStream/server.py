from flask import Flask, render_template, Response
import os
import random

app = Flask(__name__)
VIDEO_FOLDER = "videos"

def get_mime_type(filename):
    if filename.endswith('.mp4'):   return 'video/mp4'
    if filename.endswith('.webm'):  return 'video/webm'
    if filename.endswith('.ogg'):   return 'video/ogg'
    if filename.endswith('.mp3'):   return 'audio/mpeg'
    if filename.endswith('.wav'):   return 'audio/wav'
    return 'application/octet-stream'

def stream_file(filename):
    filepath = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    def generate():
        with open(filepath, "rb") as f:
            while True:
                chunk_size = random.randint(1000, 2000)   
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    mime = get_mime_type(filename)
    return Response(generate(), mimetype=mime)

@app.route('/')
def index():
    files = [f for f in os.listdir(VIDEO_FOLDER) 
             if f.lower().endswith(('.mp4', '.webm', '.ogg', '.mp3', '.wav'))]
    return render_template('index.html', files=files)

@app.route('/stream/<filename>')
def stream(filename):
    return stream_file(filename)

if __name__ == '__main__':
    print("Server running → http://127.0.0.1:5000")
    app.run(port=5000, threaded=True)