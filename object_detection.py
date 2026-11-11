
import cv2
import time
import argparse
from collections import Counter
from ultralytics import YOLO


# ==========================================================
# CONFIGURATION
# ==========================================================

MODEL_PATH = "yolov5su.pt"
CONFIDENCE_THRESHOLD = 0.40

COLORS = [
    (140, 100, 255),
    (80, 220, 180),
    (255, 170, 80),
    (100, 180, 255),
    (255, 100, 180),
    (180, 255, 100),
]


# ==========================================================
# HELPERS
# ==========================================================

def draw_label(frame, text, x, y, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.55
    thickness = 2

    (w, h), baseline = cv2.getTextSize(
        text, font, scale, thickness
    )

    y = max(y, h + 12)

    cv2.rectangle(
        frame,
        (x, y - h - 10),
        (x + w + 10, y + baseline),
        color,
        -1
    )

    cv2.putText(
        frame,
        text,
        (x + 5, y - 4),
        font,
        scale,
        (15, 20, 35),
        thickness,
        cv2.LINE_AA
    )


def draw_hud(frame, fps, object_count, class_counts):
    h, w = frame.shape[:2]

    # Header background
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (0, 0),
        (w, 75),
        (12, 18, 32),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.88,
        frame,
        0.12,
        0,
        frame
    )

    # Header title
    cv2.putText(
        frame,
        "AI OBJECT DETECTION & TRACKING",
        (22, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (220, 225, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        "LIVE ANALYTICS",
        (22, 56),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (180, 140, 255),
        1,
        cv2.LINE_AA
    )

    # FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (w - 220, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (100, 255, 190),
        2,
        cv2.LINE_AA
    )

    # Object count
    cv2.putText(
        frame,
        f"OBJECTS: {object_count}",
        (w - 220, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (220, 225, 255),
        2,
        cv2.LINE_AA
    )

    # Bottom analytics panel
    panel_height = 45

    cv2.rectangle(
        frame,
        (0, h - panel_height),
        (w, h),
        (12, 18, 32),
        -1
    )

    summary = " | ".join(
        f"{name}: {count}"
        for name, count in class_counts.items()
    )

    if not summary:
        summary = "No objects detected"

    cv2.putText(
        frame,
        summary[:100],
        (20, h - 16),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (180, 220, 255),
        1,
        cv2.LINE_AA
    )


# ==========================================================
# MAIN DETECTION
# ==========================================================

def run_detection(source=0):
    print("[INFO] Loading YOLO model...")

    model = YOLO(MODEL_PATH)

    print("[INFO] Starting video input...")

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("[ERROR] Unable to open video source.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    previous_time = time.time()

    cv2.namedWindow(
        "AI Object Detection & Tracking",
        cv2.WINDOW_NORMAL
    )

    while True:
        ret, frame = cap.read()

        if not ret:
            print("[INFO] Video ended or frame unavailable.")
            break

        # YOLO detection and tracking
        results = model.track(
            frame,
            persist=True,
            conf=CONFIDENCE_THRESHOLD,
            tracker="bytetrack.yaml",
            verbose=False
        )

        result = results[0]

        object_count = 0
        class_counts = Counter()

        if result.boxes is not None:
            boxes = result.boxes

            for box in boxes:
                coords = box.xyxy[0].cpu().numpy().astype(int)

                x1, y1, x2, y2 = coords

                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())

                class_name = model.names[class_id]

                object_count += 1
                class_counts[class_name] += 1

                # Stable color for class
                color = COLORS[class_id % len(COLORS)]

                # Tracking ID
                track_id = None

                if box.id is not None:
                    track_id = int(box.id[0].item())

                if track_id is not None:
                    label = (
                        f"{class_name.upper()} "
                        f"ID:{track_id} "
                        f"{confidence:.0%}"
                    )
                else:
                    label = (
                        f"{class_name.upper()} "
                        f"{confidence:.0%}"
                    )

                # Bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                # Label background
                draw_label(
                    frame,
                    label,
                    x1,
                    y1,
                    color
                )

                # Corner markers
                corner_length = 15
                thickness = 3

                cv2.line(
                    frame,
                    (x1, y1),
                    (x1 + corner_length, y1),
                    color,
                    thickness
                )

                cv2.line(
                    frame,
                    (x1, y1),
                    (x1, y1 + corner_length),
                    color,
                    thickness
                )

                cv2.line(
                    frame,
                    (x2, y2),
                    (x2 - corner_length, y2),
                    color,
                    thickness
                )

                cv2.line(
                    frame,
                    (x2, y2),
                    (x2, y2 - corner_length),
                    color,
                    thickness
                )

        # Calculate FPS
        current_time = time.time()

        elapsed = current_time - previous_time

        fps = 1 / elapsed if elapsed > 0 else 0

        previous_time = current_time

        # Draw analytics HUD
        draw_hud(
            frame,
            fps,
            object_count,
            class_counts
        )

        cv2.imshow(
            "AI Object Detection & Tracking",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Press Q to quit
        if key == ord("q"):
            break

        # Press F for fullscreen toggle
        if key == ord("f"):
            cv2.setWindowProperty(
                "AI Object Detection & Tracking",
                cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_FULLSCREEN
            )

    cap.release()
    cv2.destroyAllWindows()

    print("[INFO] Detection stopped.")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YOLO Object Detection and Tracking"
    )

    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index or path to video file"
    )

    args = parser.parse_args()

    source = args.source

    if source.isdigit():
        source = int(source)

    run_detection(source)
