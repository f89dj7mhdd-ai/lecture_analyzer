import os
import shutil
import numpy as np

from PIL import Image
from pathlib import Path


FRAME_DIR = "temp/frames"
OUTPUT_DIR = "temp/important_frames"

# 板書が「大きく変わった」と判定するしきい値（画素の平均差: 0〜255）
# 大きくするほど重要フレームは減る（重複が消える）。小さくすると増える。
# 目安: 15=ほぼ全部拾う / 25=重複を間引く / 35=本当に変わった時だけ
THRESHOLD = 25


def _load(path):
    # グレースケール＆縮小して比較用の配列にする（軽く・速く比較するため）
    image = Image.open(path).convert("L")
    image = image.resize((320, 180))
    return np.array(image, dtype=np.float32)


def detect_changes(threshold=THRESHOLD):
    """
    連続するフレームを比較して、板書が大きく変わる「区切り」を探す。
    各区切りごとに『変わる直前のコマ（＝板書が一番書き込まれた状態）』だけを保存する。
    これで重複を減らしつつ、完成した板書を残せる。
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 前回の結果が混ざらないよう、重要フレームを一旦クリア
    for old in Path(OUTPUT_DIR).glob("*.jpg"):
        old.unlink()

    files = sorted(os.listdir(FRAME_DIR))

    # 画像だけ残す
    files = [
        f for f in files
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    prev = None
    candidate = None   # 今の区切りで最後に見たコマ（＝一番完成した板書）
    saved = 0

    def save(path):
        shutil.copy(path, os.path.join(OUTPUT_DIR, os.path.basename(path)))

    for file in files:

        path = os.path.join(FRAME_DIR, file)
        arr = _load(path)

        if prev is None:
            prev = arr
            candidate = path
            continue

        diff = np.mean(np.abs(arr - prev))

        if diff > threshold:
            # 板書が大きく変わった → 直前の区切りの完成コマを確定保存
            save(candidate)
            saved += 1
            candidate = path        # 新しい区切りを開始
        else:
            candidate = path        # 同じ板書の続き → 最新コマに更新

        prev = arr

    # 最後の区切りの完成コマも保存
    if candidate is not None:
        save(candidate)
        saved += 1

    print(f"重要フレーム保存数: {saved}")
