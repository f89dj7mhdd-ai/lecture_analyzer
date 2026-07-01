import os
import glob
import sys
import shutil

from audio import extract_audio
from splitter import split_audio

from whisper_module import transcribe_all
from summarize_module import summarize_lecture

from frame_extract import extract_frames
from diff_detector import detect_changes
from vision_module import analyze_frames

from merge_module import merge_notes
from pdf_module import make_pdf


# フォルダ作成
# temp は実行のたびに作り直す（前回の動画のフレーム・音声が残らないように）
if os.path.exists("temp"):
    shutil.rmtree("temp")

os.makedirs("temp/frames", exist_ok=True)
os.makedirs("temp/important_frames", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# =========================
# 動画を選ぶ
# =========================

def select_video():

    # 引数で渡されたらそれを使う（例: python main.py videos/講義.mp4）
    if len(sys.argv) > 1:
        return sys.argv[1]

    # 引数がなければ videos/ の一覧から番号で選ぶ
    videos = sorted(glob.glob("videos/*.mp4"))

    if not videos:
        print("videos/ に .mp4 がありません")
        sys.exit(1)

    print("解析する動画を選んでください：")
    for i, v in enumerate(videos):
        print(f"  {i + 1}: {os.path.basename(v)}")

    while True:
        try:
            choice = int(input("番号を入力: "))
            if 1 <= choice <= len(videos):
                return videos[choice - 1]
        except ValueError:
            pass
        print("正しい番号を入力してください")


video_path = select_video()


# 出力先を動画名ごとに分ける（例: outputs/探索的データ解析/）
video_name = os.path.splitext(os.path.basename(video_path))[0]
output_dir = os.path.join("outputs", video_name)
os.makedirs(output_dir, exist_ok=True)
print(f"出力先: {output_dir}")



# =========================
# 音声処理
# =========================

print("===== 音声抽出開始 =====")

extract_audio(video_path)

print("===== 音声分割開始 =====")

split_audio("temp/lecture_audio.mp3")

print("===== Whisper文字起こし開始 =====")

transcribe_all(output_dir)

print("===== 要約開始 =====")

summarize_lecture(output_dir)


# =========================
# 画像処理
# =========================

print("===== フレーム抽出開始 =====")

extract_frames(video_path)

print("===== 差分検出開始 =====")

detect_changes()

print("===== Vision解析開始 =====")

analyze_frames(output_dir)


# =========================
# 統合
# =========================

print("===== ノート統合開始 =====")

merge_notes(output_dir)


# =========================
# PDF生成
# =========================

print("===== PDF生成開始 =====")

make_pdf(output_dir)

print("===== 全処理完了 =====")