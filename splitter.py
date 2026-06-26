from utils import run_command

def split_audio(audio_path):

    run_command([
        "ffmpeg",
        "-i",
        audio_path,
        "-f",
        "segment",
        "-segment_time",
        "600",
        "-c",
        "copy",
        "temp/output%03d.mp3"
    ])

    print("音声分割完了")