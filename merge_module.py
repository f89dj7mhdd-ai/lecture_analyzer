def merge_notes():

    with open(
        "outputs/summary.txt",
        "r",
        encoding="utf-8"
    ) as f:
        summary = f.read()

    with open(
        "outputs/vision_summary.txt",
        "r",
        encoding="utf-8"
    ) as f:
        vision = f.read()

    final_note = f"""
# 講義ノート

{summary}

---

# 板書解析

{vision}
"""

    with open(
        "outputs/final_note.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(final_note)

    print("final_note.txt 保存完了")