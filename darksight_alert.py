import cv2
from ultralytics import YOLO
import numpy as np
import time

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

def enhance_low_light(image):
    """
    Enhance low-light image using gamma correction
    """
    gamma = 1.8
    inv_gamma = 1.0 / gamma

    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(256)
    ]).astype("uint8")

    return cv2.LUT(image, table)

prev_gray = None
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not detected")
        break

    # Simulate low light
    dark = cv2.convertScaleAbs(frame, alpha=0.3, beta=0)

    # Enhance image
    enhanced = enhance_low_light(dark)

    # ---------------- Motion Detection ----------------
    gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:
        prev_gray = gray
        continue

    diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) > 150:   # sensitivity
            motion_detected = True
            break

    prev_gray = gray

    # ---------------- Object Detection ----------------
    results = model(enhanced, stream=True)
    for r in results:
        enhanced = r.plot()

    # ---------------- ALERT WINDOW ----------------
    if motion_detected:
        alert_img = np.zeros((300, 900, 3), dtype=np.uint8)
        alert_img[:] = (0, 0, 255)

        cv2.putText(alert_img, "INTRUSION ALERT !!!",
                    (120, 170),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.5, (255, 255, 255), 6)

        cv2.imshow("ALERT WINDOW", alert_img)
    else:
        cv2.destroyWindow("ALERT WINDOW")

    # ---------------- FPS ----------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    cv2.putText(enhanced, f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    # ---------------- Display ----------------
    cv2.imshow("DarkSight AI - Smart Surveillance", enhanced)
    cv2.imshow("Motion Mask", thresh)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()