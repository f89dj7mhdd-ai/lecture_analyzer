from openai import OpenAI
import os
import glob

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def transcribe_all():

    mp3_files = sorted(
        glob.glob("temp/output*.mp3")
    )

    all_text = []

    for mp3_file in mp3_files:

        print(f"{mp3_file} 文字起こし中")

        audio_file = open(mp3_file, "rb")

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        text = transcript.text

        all_text.append(text)

    full_text = "\n".join(all_text)

    with open(
        "outputs/transcript.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(full_text)

    print("transcript.txt 保存完了")