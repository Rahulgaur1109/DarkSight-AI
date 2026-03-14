🌙 DarkSight AI

AI-Powered Low-Light Surveillance & Intrusion Detection System

DarkSight AI is an intelligent surveillance system designed to improve visibility and monitoring in low-light environments. It enhances dark video feeds, performs real-time object detection, detects suspicious motion, and streams the processed video to a live web dashboard for monitoring.

The system combines computer vision, deep learning, and web technologies to create a real-time AI security solution suitable for campuses, parking areas, smart cities, and other low-visibility environments.

⸻

🚀 Features
	•	🌙 Low-Light Enhancement – Improves visibility of dark video feeds
	•	🎯 Real-Time Object Detection – Detects objects using YOLOv8
	•	🚨 Motion Detection & Intrusion Alert – Detects suspicious movement
	•	📹 Live Video Streaming – Real-time AI processed feed in browser
	•	🌐 Web Dashboard – React-based monitoring interface
	•	⚡ Real-Time Processing – AI inference on live webcam stream

                  ┌───────────────┐
                │   Webcam Feed │
                └───────┬───────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Low-Light Enhance │
              │  (Gamma Correction) │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Motion Detection │
              │   (OpenCV)       │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Object Detection │
              │    YOLOv8 AI     │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Flask Streaming  │
              │    API Server    │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ React Dashboard  │
              │  Live Monitoring │
              └──────────────────┘

              🛠️ Tech Stack

AI & Computer Vision
	•	Python
	•	OpenCV
	•	YOLOv8 (Ultralytics)
	•	NumPy

Backend
	•	Flask
	•	MJPEG Video Streaming

Frontend
	•	React.js

DarkSightAI
│
├── server.py            # Flask AI streaming server
├── darksight_alert.py   # Motion detection & alert logic
├── webcam_detect.py     # YOLO webcam detection
│
├── darksight-ui
│   ├── src
│   │   └── App.js
│   └── package.json
│
├── requirements.txt
└── README.md


⚙️ Installation

1️⃣ Clone the Repository
git clone https://github.com/yourusername/darksight-ai.git
cd darksight-ai

2️⃣ Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install ultralytics opencv-python numpy flask flask-cors

▶️ Run the AI Server
python server.py

Open browser:
http://localhost:5000/video

🌐 Run the React Dashboard
cd darksight-ui
npm install
npm start

🎯 Use Cases
	•	Campus & hostel security
	•	Smart city surveillance
	•	Parking lot monitoring
	•	Low-light industrial environments
	•	AI-powered CCTV systems

⸻

🚀 Future Improvements
	•	Mobile notification alerts
	•	Cloud deployment
	•	Multi-camera monitoring
	•	AI anomaly detection
	•	Sound alarm system

⸻

👨‍💻 Author

Rahul Gaur
B.Tech Computer Science
Bennett University
