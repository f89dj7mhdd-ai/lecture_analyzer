import os
import shutil
import numpy as np

from PIL import Image
from pathlib import Path


FRAME_DIR = "temp/frames"
OUTPUT_DIR = "temp/important_frames"


def detect_changes(threshold=15):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = sorted(os.listdir(FRAME_DIR))

    # 画像だけ残す
    files = [
        f for f in files
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    prev = None
    saved = 0

    for file in files:

        path = os.path.join(FRAME_DIR, file)

        image = Image.open(path).convert("L")
        image = image.resize((320, 180))

        arr = np.array(image, dtype=np.float32)

        if prev is None:
            shutil.copy(path, os.path.join(OUTPUT_DIR, file))
            prev = arr
            saved += 1
            continue

        diff = np.mean(np.abs(arr - prev))

        if diff > threshold:
            shutil.copy(path, os.path.join(OUTPUT_DIR, file))
            prev = arr
            saved += 1

    print(f"重要フレーム保存数: {saved}")