# 🎯 Object Detection & Tracking

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Model-YOLOv5s-FF6F00?style=flat-square" alt="YOLOv5">
  <img src="https://img.shields.io/badge/Tracking-ByteTrack-EE4C2C?style=flat-square" alt="ByteTrack">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
</p>

<p align="center">
  <b>Real-time multi-object detection and tracking with YOLOv5 + ByteTrack and a live Flask dashboard.</b><br>
  <sub>Webcam, video file, and image support with persistent object IDs and bounding boxes.</sub>
</p>

---

## ✨ Features

- Real-time object detection using YOLOv5s
- Multi-object tracking with ByteTrack algorithm
- Persistent object IDs across frames
- Live Flask dashboard with real-time video streaming
- Webcam, video file, and image input support
- Bounding boxes with tracking labels
- Confidence score display

## 🛠️ Tech Stack

| Component | Technology |
|:----------|:-----------|
| **Detection** | YOLOv5s (Ultralytics) |
| **Tracking** | ByteTrack |
| **Backend** | Python, Flask |
| **Streaming** | OpenCV (MJPEG streaming) |
| **Frontend** | HTML5, CSS3, JavaScript |

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/OmkarSolat-17/CodeAlpha_Object-Detection-and-Tracking.git
cd CodeAlpha_Object-Detection-and-Tracking
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download pretrained weights

The model weights (`yolov5su.pt`, ~14 MB) are **not stored in this repo** to keep it lightweight. Download them with one command:

```bash
python download_weights.py
```

This script automatically downloads `yolov5su.pt` from the official Ultralytics release and saves it to the project root.

> **Manual download (alternative):**  
> Download `yolov5su.pt` from [Ultralytics YOLOv5 Releases](https://github.com/ultralytics/yolov5/releases) and place it in the project root directory.

### 5. Run the application

```bash
python app.py
```

### 6. Open in browser

Visit: `http://127.0.0.1:5000`

## 🧠 How It Works

```
Video Frame → YOLOv5 Detection → ByteTrack Association → Annotated Frame → MJPEG Stream → Dashboard
```

1. Video frame is captured from webcam, file, or image
2. YOLOv5 detects objects and returns bounding boxes with confidence scores
3. ByteTrack associates detections across frames, assigning persistent IDs
4. Annotated frame with boxes and tracking IDs is streamed to the dashboard
5. Dashboard displays live feed with detection statistics

## 📂 Project Structure

```
CodeAlpha_Object-Detection-and-Tracking/
├── app.py                  # Flask app, streaming, and tracking pipeline
├── download_weights.py     # Downloads yolov5su.pt weights automatically
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignores *.pt, venv, cache files
├── templates/
│   └── index.html          # Dashboard template
├── static/
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
└── README.md
```

> **Note:** `yolov5su.pt` is intentionally excluded from Git via `.gitignore`. Run `python download_weights.py` after cloning to get it.

## 🔧 Troubleshooting

| Problem | Solution |
|:--------|:---------|
| `FileNotFoundError: yolov5su.pt` | Run `python download_weights.py` first |
| Webcam not detected | Check camera permissions; try a video file instead |
| Slow on CPU | Use `yolov5ns.pt` (nano) for faster inference — update the model path in `app.py` |
| Port already in use | Change the port in `app.py` (`app.run(port=5001)`) |

## 🎯 Project Objective

Build a real-time object detection and tracking system combining YOLOv5 detection with ByteTrack multi-object tracking, served through a live Flask dashboard.

## 👨‍💻 Internship

This project was developed as part of the **Artificial Intelligence Internship at CodeAlpha**.

---

<p align="center">
  <sub>Built by <a href="https://github.com/OmkarSolat-17">Omkar Solat</a> · B.Tech CSE (AI/ML)</sub>
</p>

<!--
Topics to add in repo settings:
object-detection, yolov5, bytetrack, multi-object-tracking, computer-vision, opencv, flask, deep-learning, real-time, tracking
-->
