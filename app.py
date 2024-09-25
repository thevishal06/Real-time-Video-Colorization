import cv2
from flask import Flask, render_template, Response
import numpy as np

app = Flask(__name__)

def colorize_frame(frame):
    # Dummy colorization logic (Replace with your model)
    return cv2.applyColorMap(frame, cv2.COLORMAP_JET)

def generate_frames():
    camera = cv2.VideoCapture(0)  # Capture from webcam

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        colorized_frame = colorize_frame(gray_frame)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', colorized_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
