from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import threading

app = Flask(__name__)
recognizer = sr.Recognizer()
mic = sr.Microphone()
recording = False
recognized_text = ""

def record_and_transcribe():
    global recognized_text, recording
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while recording:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                recognized_text += text + "\n"
                print("Recognized:", text)
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("Speech recognition service unavailable")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_recording():
    global recording
    if not recording:
        recording = True
        threading.Thread(target=record_and_transcribe).start()
        return jsonify({"status": "Recording started"})
    return jsonify({"status": "Already recording"})

@app.route("/stop", methods=["POST"])
def stop_recording():
    global recording
    recording = False
    return jsonify({"status": "Recording stopped", "text": recognized_text})

if __name__ == "__main__":
    app.run(debug=True)
