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
    Brightness enhancement using Gamma correction
    """
    gamma = 1.8
    inv_gamma = 1.0 / gamma

    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(256)
    ]).astype("uint8")

    return cv2.LUT(image, table)

prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Simulate darkness (for demo)
    dark_frame = cv2.convertScaleAbs(frame, alpha=0.3, beta=0)

    # Enhance dark image
    enhanced_frame = enhance_low_light(dark_frame)

    # YOLO detection on enhanced image
    results = model(enhanced_frame, stream=True)

    for r in results:
        enhanced_frame = r.plot()

    # FPS calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    cv2.putText(enhanced_frame, f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    # Display windows
    cv2.imshow("Dark Input (Simulated)", dark_frame)
    cv2.imshow("DarkSight AI (Enhanced + Detection)", enhanced_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()