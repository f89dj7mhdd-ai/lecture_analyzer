from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def summarize_lecture():

    print("transcript.txt 読み込み")

    with open("outputs/transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    print("GPT要約開始")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
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
    )

    summary = response.output_text

    with open("outputs/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("summary.txt 保存完了")