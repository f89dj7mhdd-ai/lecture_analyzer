import os

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
os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("temp/frames", exist_ok=True)
os.makedirs("temp/important_frames", exist_ok=True)


# 動画パス
video_path ="videos/探索的データ解析.mp4"



# =========================
# 音声処理
# =========================

print("===== 音声抽出開始 =====")

extract_audio(video_path)

print("===== 音声分割開始 =====")

split_audio("temp/lecture_audio.mp3")

print("===== Whisper文字起こし開始 =====")

transcribe_all()

print("===== GPT要約開始 =====")

summarize_lecture()


# =========================
# 画像処理
# =========================

print("===== フレーム抽出開始 =====")

extract_frames(video_path)

print("===== 差分検出開始 =====")

detect_changes()

print("===== Vision解析開始 =====")

analyze_frames()


# =========================
# 統合
# =========================

print("===== ノート統合開始 =====")

merge_notes()


# =========================
# PDF生成
# =========================

print("===== PDF生成開始 =====")

make_pdf()

print("===== 全処理完了 =====")