import ollama
import glob
import os

# 板書解析に使うビジョンモデル（`ollama list` で確認できる）
MODEL = "qwen2.5vl:3b"


def analyze_frames(output_dir):

    frame_files = sorted(
        glob.glob("temp/important_frames/*.jpg")
    )

    results = []

    for frame in frame_files:

        print(f"{frame} 解析中")

        # ollama は images に画像ファイルのパスを直接渡せる
        # （base64エンコードはライブラリが内部で行う）
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "この講義板書画像を解析し、重要内容を簡潔にまとめてください。",
                    "images": [frame]
                }
            ]
        )

        results.append(response["message"]["content"])

    full_text = "\n\n".join(results)

    with open(
        os.path.join(output_dir, "vision_summary.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(full_text)

    print("vision_summary.txt 保存完了")
