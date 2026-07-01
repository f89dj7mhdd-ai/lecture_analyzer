# lecture_analyzer

講義動画を入れると、**文字起こし → 要約 → 板書解析 → 統合ノート → PDF** まで自動生成するツール。
解析はすべて**ローカル（Whisper + Ollama）**で動くので、API利用料はかかりません。

## 処理の流れ

```
動画(.mp4)
  ├─ 音声 → 文字起こし(faster-whisper) → 要約(Ollama: llama3.1)
  └─ 映像 → フレーム抽出 → 重要コマ選別 → 板書解析(Ollama: qwen2.5vl)
                                   ↓
                          統合ノート → PDF(xelatex)
```

## 必要なもの

- Python 3.14（`.venv`）
- [Ollama](https://ollama.com/)（解析用LLMをローカル実行）
- `ffmpeg`（音声抽出・フレーム抽出）
- `xelatex`（PDF生成 / MacTeX等）

## セットアップ

```bash
# 1) 仮想環境
python3.14 -m venv .venv
source .venv/bin/activate

# 2) Pythonパッケージ
pip install ollama faster-whisper numpy pillow

# 3) Ollamaのモデル（初回だけ）
ollama pull llama3.1:8b     # 要約用
ollama pull qwen2.5vl:3b    # 板書解析用
```

> 初回実行時、faster-whisper のモデル（`large-v3`, 約1.5GB）が自動ダウンロードされます。

## 使い方

```bash
# videos/ に解析したい動画(.mp4)を置く
python main.py
```

実行すると `videos/` 内の動画が一覧表示されるので、**番号を選ぶだけ**。
結果は動画名ごとに `outputs/<動画名>/` に保存されます。

```
outputs/<動画名>/
├── transcript.txt      文字起こし
├── summary.txt         要約
├── vision_summary.txt  板書解析
├── final_note.txt      統合ノート
└── note.pdf            PDF
```

引数で直接渡すこともできます：

```bash
python main.py videos/講義.mp4
```

## 設定（モデル・精度の調整）

| 項目 | 場所 | 既定値 |
|---|---|---|
| 文字起こしモデル | `whisper_module.py` の `MODEL_SIZE` | `large-v3` |
| 要約モデル | `summarize_module.py` の `MODEL` | `llama3.1:8b` |
| 板書解析モデル | `vision_module.py` の `MODEL` | `qwen2.5vl:3b` |
| 板書の重複間引き | `diff_detector.py` の `THRESHOLD` | `25` |

- 板書の質を上げたい → `vision_module.py` の `MODEL` を `qwen2.5vl:7b` に。
- 解析するコマが多すぎ/少なすぎ → `diff_detector.py` の `THRESHOLD` を上げる/下げる。

## 注意

- `videos/`, `temp/`, `outputs/` は `.gitignore` 済み（動画・生成物はGit管理しない）。
