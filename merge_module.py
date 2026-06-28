import os


def merge_notes(output_dir):

    with open(
        os.path.join(output_dir, "summary.txt"),
        "r",
        encoding="utf-8"
    ) as f:
        summary = f.read()

    with open(
        os.path.join(output_dir, "vision_summary.txt"),
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
        os.path.join(output_dir, "final_note.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(final_note)

    print("final_note.txt 保存完了")