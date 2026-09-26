#!/usr/bin/env python3
"""Xuất danh sách CHÍNH XÁC các ảnh chụp màn hình cần chụp cho mọi video, đọc
trực tiếp từ "Bảng cảnh AI" trong từng file kịch bản (không hand-type, tự động
đồng bộ khi kịch bản đổi) -- để người dùng chỉ cần làm theo, không phải tự suy
luận cần chụp gì / lưu tên gì.

Dùng:
    python3 pipeline/export_screenshot_checklist.py channels/ai-de-dung/scripts \
        --out channels/ai-de-dung/screenshot-checklist.md
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_script  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scripts_dir", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    lines = [
        "# Danh sách ảnh chụp màn hình cần chụp (tự sinh từ scripts/*.md -- chạy lại "
        "`pipeline/export_screenshot_checklist.py` sau khi sửa kịch bản để cập nhật)",
        "",
        "> **Quy tắc lưu tên file:** cảnh chỉ cần 1 ảnh -> lưu `NN.png` (NN = số thứ tự "
        "cảnh, 2 chữ số). Cảnh cần NHIỀU ảnh (xem cột \"Ghi chú\" -- có ghi số tấm) -> "
        "lưu `NNa.png`, `NNb.png`, `NNc.png`... `pipeline/assemble.py` tự nhận diện cả "
        "2 kiểu và tự chia đều thời lượng cảnh cho nhiều ảnh. Chụp bằng phím tắt chụp "
        "màn hình có sẵn trên máy (Windows: Win+Shift+S), không cần quay video, không "
        "cần chỉnh sửa gì thêm -- chụp xong lưu đúng thư mục là dùng được ngay.",
        "",
    ]

    total = 0
    for script_path in sorted(Path(args.scripts_dir).glob("*.md")):
        _, scenes = load_script(script_path)
        shots = [s for s in scenes if not s.is_ai_video]
        if not shots:
            continue
        slug = script_path.stem
        title = script_path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        lines.append(f"## {title}")
        lines.append(f"Lưu vào: `channels/ai-de-dung/assets/{slug}/screenshots/`")
        lines.append("")
        lines.append("| Cảnh # | Thời điểm | Cần chụp gì | Tên file lưu |")
        lines.append("|---|---|---|---|")
        for s in shots:
            total += 1
            lines.append(f"| {s.index:02d} | {s.time_range} | {s.description} — *{s.note}* | `{s.index:02d}.png` (hoặc `{s.index:02d}a.png`, `{s.index:02d}b.png`... nếu ghi chú yêu cầu nhiều tấm) |")
        lines.append("")

    lines.insert(3, f"> **Tổng cộng: {total} cảnh cần ảnh trên toàn kênh** (một số cảnh cần nhiều hơn 1 tấm -- xem ghi chú từng dòng).\n")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Đã lưu {args.out} ({total} cảnh cần ảnh trên {len(list(Path(args.scripts_dir).glob('*.md')))} video)")


if __name__ == "__main__":
    main()
