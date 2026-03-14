from flask import Flask, Response
import cv2
from ultralytics import YOLO
import numpy as np

app = Flask(__name__)

# Load model
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

prev_gray = None

def enhance_low_light(image):
    gamma = 1.8
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)

def generate_frames():
    global prev_gray

    while True:
        success, frame = cap.read()
        if not success:
            break

        # ---------------- LOW LIGHT SIMULATION ----------------
        dark = cv2.convertScaleAbs(frame, alpha=0.3, beta=0)

        # ---------------- ENHANCEMENT ----------------
        enhanced = enhance_low_light(dark)

        # ---------------- MOTION DETECTION ----------------
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        motion_detected = False

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=3)

            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                if cv2.contourArea(c) > 200:
                    motion_detected = True
                    break

        prev_gray = gray

        # ---------------- OBJECT DETECTION ----------------
        results = model(enhanced, stream=True)
        for r in results:
            enhanced = r.plot()

        # ---------------- ALERT OVERLAY ----------------
        if motion_detected:
            cv2.rectangle(enhanced, (0, 0), (640, 90), (0, 0, 255), -1)
            cv2.putText(enhanced, "INTRUSION ALERT",
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.6, (255, 255, 255), 4)

        # ---------------- STREAM OUTPUT ----------------
        _, buffer = cv2.imencode('.jpg', enhanced)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5000)