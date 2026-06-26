from utils import run_command

def extract_audio(video_path):

    run_command([
        "ffmpeg",
        "-i",
        video_path,
        "temp/lecture_audio.mp3"
    ])