from utils import run_command

def extract_frames(video_path):

    run_command([
        "ffmpeg",
        "-i",
        video_path,
        "-vf",
        "fps=1/60",
        "temp/frames/frame_%04d.jpg"
    ])

    print("フレーム抽出完了")