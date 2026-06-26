from openai import OpenAI
import os
import base64
import glob

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_frames():

    frame_files = sorted(
        glob.glob("temp/important_frames/*.jpg")
    )

    results = []

    for frame in frame_files:

        print(f"{frame} 解析中")

        with open(frame, "rb") as f:
            base64_image = base64.b64encode(
                f.read()
            ).decode("utf-8")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
この講義板書画像を解析し、
重要内容を簡潔にまとめてください。
"""
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ]
        )

        results.append(response.output_text)

    full_text = "\n\n".join(results)

    with open(
        "outputs/vision_summary.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(full_text)

    print("vision_summary.txt 保存完了")