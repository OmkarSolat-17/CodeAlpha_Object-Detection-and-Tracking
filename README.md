# 👁️ Object Detection & Tracking (Task 4)

A real-time object detection and multi-object tracking application built using YOLOv5su, OpenCV, and ByteTrack. The system detects objects in video streams and tracks their movement using unique tracking IDs.

## ✨ Features

- Real-time object detection
- Multi-object tracking
- Bounding boxes around detected objects
- Object class labels and confidence scores
- Unique tracking IDs
- Webcam and video input support
- FPS monitoring
- Object detection analytics
- Interactive web dashboard

## 🛠️ Tech Stack

- **Python** – Core programming
- **YOLOv5su** – Object detection model
- **Ultralytics** – Model integration
- **OpenCV** – Video processing
- **ByteTrack** – Multi-object tracking
- **Flask** – Web dashboard and backend
- **HTML5, CSS3, JavaScript** – Frontend

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/OmkarSolat-17/CodeAlpha_ObjectDetectionTracking.git
cd CodeAlpha_ObjectDetectionTracking
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

### 4. Open in browser

Visit:

```text
http://127.0.0.1:5000
```

## 🧠 How It Works

1. The application receives video input from a webcam or video file.
2. YOLOv5su detects objects in each frame.
3. ByteTrack associates detected objects across consecutive frames.
4. Each tracked object receives a tracking ID.
5. OpenCV renders bounding boxes, labels, and confidence scores.
6. Detection statistics are displayed through the dashboard.

## 📂 Project Structure

```text
CodeAlpha_ObjectDetectionTracking/
├── app.py
├── object_detection.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

## 📌 Model

The project uses the pretrained `yolov5su.pt` model.

The model weights are downloaded automatically by Ultralytics when required. The `.pt` file does not need to be committed to the repository.

## 🎯 Project Objective

To implement a computer vision system demonstrating object detection, multi-object tracking, and real-time video analytics.

## 👨‍💻 Internship

This project was developed as part of the **Artificial Intelligence Internship at CodeAlpha**.

---

⭐ If you find this project interesting, consider giving it a star!
