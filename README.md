# Object Detection and Tracking (Task 4)

This project implements real‑time object detection and tracking using a webcam (or video file) in Python.

## Features
- **Detection**: Uses the pre‑trained YOLOv5‑s model (via the `ultralytics` package) to detect objects in each frame.
- **Tracking**: Applies the SORT algorithm (`sort` package) to assign persistent IDs to detected objects across frames.
- **Visualization**: Draws bounding boxes with class labels and tracking IDs on the video stream.
- **Cross‑platform**: Works on Windows, macOS, and Linux with a standard Python environment.

## Setup
1. **Clone / open this folder** in your IDE or terminal.
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python object_detection.py
   ```
   - By default it uses your webcam (`camera index 0`).
   - To use a video file, pass the path as the first argument:
     ```
     python object_detection.py path/to/video.mp4
     ```

## Files
- `object_detection.py` – Main script that captures video, runs YOLO detection, tracks objects, and displays the output.
- `requirements.txt` – List of Python dependencies.
- `README.md` – This documentation.

## License
This demo code is provided for educational purposes under the MIT license.

