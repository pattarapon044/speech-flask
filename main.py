from flask import Flask, render_template, request, Response, redirect
from gtts import gTTS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/text_to_speech")
def text_to_speech():
    return render_template("text_to_speech.html")


@app.route("/speech_to_text")
def speech_to_text():
    return render_template("speech_to_text.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/speech", methods=["POST"])
def speech():
    # Function to generate speech audio to response
    def generate():
        with open(f"./static/speech.mp3", "rb") as file:
            data = file.read(1024)
            while data:
                yield data
                data = file.read(1024)
    
    text = request.form.get("text") # Get text from formData
    filename = "speech.mp3" # Set filename
    tts = gTTS(text, lang="th") # Setup gTTS
    tts.save(f"./static/{filename}") # Save gTTS to file
    return Response(generate(), mimetype="audio/x-wav") # Return Response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)