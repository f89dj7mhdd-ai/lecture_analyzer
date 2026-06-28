from faster_whisper import WhisperModel
import glob
import os

# 文字起こしに使うモデル
# large-v3 = 高精度/低速, medium = バランス, small = 高速/低精度
MODEL_SIZE = "large-v3"

# モデルは初回実行時に自動ダウンロードされる（large-v3 で約1.5GB）
# Mac(CPU)では compute_type="int8" が省メモリで安定
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe_all(output_dir):

    mp3_files = sorted(
        glob.glob("temp/output*.mp3")
    )

    all_text = []

    for mp3_file in mp3_files:

        print(f"{mp3_file} 文字起こし中")

        # language="ja" で日本語に固定（誤判定を防ぐ）
        segments, info = model.transcribe(mp3_file, language="ja")

        # segments はジェネレータなので連結してテキスト化
        text = "".join(segment.text for segment in segments)

        all_text.append(text)

    full_text = "\n".join(all_text)

    with open(
        os.path.join(output_dir, "transcript.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(full_text)

    print("transcript.txt 保存完了")
