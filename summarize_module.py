import ollama
import os

# 要約に使うローカルLLM（`ollama list` で確認できる）
MODEL = "llama3.1:8b"


def summarize_lecture(output_dir):

    print("transcript.txt 読み込み")

    with open(os.path.join(output_dir, "transcript.txt"), "r", encoding="utf-8") as f:
        transcript = f.read()

    print("要約開始")

    prompt = f"""
以下は大学講義の文字起こしです。

重要ポイントを整理し、
試験勉強用に分かりやすくまとめてください。

以下を含めてください：

- 講義概要
- 重要概念
- 重要数式
- 試験に出そうなポイント
- 理解しておくべき内容

{transcript}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = response["message"]["content"]

    with open(os.path.join(output_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(summary)

    print("summary.txt 保存完了")
