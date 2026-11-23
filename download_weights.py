#!/usr/bin/env python3
"""
Download YOLOv5s pretrained weights (yolov5su.pt) from Ultralytics.

Usage:
    python download_weights.py

The weights file (~14 MB) is intentionally NOT stored in Git.
This script downloads it from the official Ultralytics release
and saves it to the project root as yolov5su.pt.
"""

import os
import sys
import urllib.request

# Official Ultralytics release URLs (tried in order)
URLS = [
    "https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5su.pt",
    "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov5su.pt",
]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov5su.pt")


def download(url, dest):
    """Download file with progress bar."""
    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(int(downloaded * 100 / total_size), 100) if total_size > 0 else 0
        bar = "#" * (percent // 2)
        sys.stdout.write(f"\r  [{bar:<50}] {percent}%  ({downloaded / 1e6:.1f} MB)")
        sys.stdout.flush()

    print(f"  Downloading from:\n    {url}\n")
    urllib.request.urlretrieve(url, dest, reporthook)
    print("\n  ✅ Download complete!")


def main():
    if os.path.exists(OUTPUT_FILE):
        size_mb = os.path.getsize(OUTPUT_FILE) / 1e6
        print(f"✅ yolov5su.pt already exists ({size_mb:.1f} MB) — skipping download.")
        return

    print("📥 Downloading YOLOv5s pretrained weights (yolov5su.pt)...\n")

    last_error = None
    for url in URLS:
        try:
            download(url, OUTPUT_FILE)
            break
        except Exception as e:
            last_error = e
            print(f"\n  ⚠️  Failed: {e}")
            if os.path.exists(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)
    else:
        print(f"\n❌ All download attempts failed. Last error: {last_error}")
        print("\nManual download:")
        print("  1. Go to https://github.com/ultralytics/yolov5/releases")
        print("  2. Download yolov5su.pt")
        print(f"  3. Place it in: {os.path.dirname(OUTPUT_FILE)}")
        sys.exit(1)

    size_mb = os.path.getsize(OUTPUT_FILE) / 1e6
    print(f"\n🎉 Saved to: {OUTPUT_FILE} ({size_mb:.1f} MB)")
    print("   You can now run: python app.py")


if __name__ == "__main__":
    main()
