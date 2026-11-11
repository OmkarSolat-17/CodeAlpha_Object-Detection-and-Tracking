
import cv2
import time
import argparse
import threading
from collections import Counter

from flask import Flask, render_template, Response, jsonify, request
from ultralytics import YOLO


# ==========================================================
# CONFIGURATION
# ==========================================================

MODEL_PATH = "yolov5su.pt"

app = Flask(__name__)

settings = {
    "confidence": 0.40,
    "tracker": "bytetrack.yaml",
    "source": 0,
    "trails": False
}

stats = {
    "objects": 0,
    "unique_tracks": 0,
    "fps": 0.0,
    "classes": {},
    "model": MODEL_PATH,
    "status": "Initializing"
}

unique_track_ids = set()
settings_lock = threading.Lock()
stats_lock = threading.Lock()

COLORS = [
    (255, 180, 70),
    (180, 100, 255),
    (80, 220, 180),
    (100, 180, 255),
    (255, 100, 180),
    (180, 255, 100)
]


# ==========================================================
# MODEL
# ==========================================================

print("[INFO] Loading YOLO model...")
model = YOLO(MODEL_PATH)
print("[INFO] YOLO model loaded!")


# ==========================================================
# DASHBOARD ROUTES
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stats")
def get_stats():
    with stats_lock:
        return jsonify(stats.copy())


@app.route("/settings", methods=["POST"])
def update_settings():
    data = request.get_json(silent=True) or {}

    with settings_lock:
        if "confidence" in data:
            settings["confidence"] = max(
                0.05, min(float(data["confidence"]), 0.95)
            )

        if data.get("tracker") in ["bytetrack.yaml", "botsort.yaml"]:
            settings["tracker"] = data["tracker"]

        if "trails" in data:
            settings["trails"] = bool(data["trails"])

    return jsonify({"success": True})


@app.route("/reset", methods=["POST"])
def reset_stats():
    unique_track_ids.clear()

    with stats_lock:
        stats["unique_tracks"] = 0

    model.predictor = None

    return jsonify({"success": True})


# ==========================================================
# VIDEO STREAM
# ==========================================================

def generate_frames(source):

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        with stats_lock:
            stats["status"] = "Video source unavailable"
        return

    previous_time = time.time()

    with stats_lock:
        stats["status"] = "LIVE"

    while True:

        success, frame = cap.read()

        if not success:
            if isinstance(source, int):
                time.sleep(0.02)
                continue
            break

        with settings_lock:
            confidence = settings["confidence"]
            tracker = settings["tracker"]

        results = model.track(
            frame,
            persist=True,
            conf=confidence,
            tracker=tracker,
            verbose=False
        )

        result = results[0]

        object_count = 0
        class_counts = Counter()

        if result.boxes is not None:

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0].cpu().numpy().astype(int)
                )

                class_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())

                class_name = model.names[class_id]

                object_count += 1
                class_counts[class_name] += 1

                color = COLORS[class_id % len(COLORS)]

                track_id = None

                if box.id is not None:
                    track_id = int(box.id[0].item())
                    unique_track_ids.add(track_id)

                label = f"{class_name} {conf:.0%}"

                if track_id is not None:
                    label = f"ID:{track_id} {label}"

                # Bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                # Label background
                label_y = max(y1 - 8, 20)

                cv2.rectangle(
                    frame,
                    (x1, label_y - 25),
                    (x1 + 220, label_y),
                    color,
                    -1
                )

                cv2.putText(
                    frame,
                    label,
                    (x1 + 5, label_y - 7),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (15, 15, 25),
                    2,
                    cv2.LINE_AA
                )

        current_time = time.time()
        elapsed = current_time - previous_time

        fps = 1 / elapsed if elapsed > 0 else 0
        previous_time = current_time

        # Update live dashboard analytics
        with stats_lock:
            stats["objects"] = object_count
            stats["unique_tracks"] = len(unique_track_ids)
            stats["fps"] = round(fps, 1)
            stats["classes"] = dict(class_counts)
            stats["status"] = "LIVE"

        # Encode frame for browser
        ret, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 85]
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )

    cap.release()


@app.route("/video_feed")
def video_feed():

    source = settings["source"]

    return Response(
        generate_frames(source),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index or video file path"
    )

    args = parser.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source

    settings["source"] = source

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=False,
        threaded=True
    )
