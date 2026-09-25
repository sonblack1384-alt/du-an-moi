#!/usr/bin/env python3
"""Chạy trọn quy trình cho 1 video: tạo giọng đọc -> tạo cảnh AI-video -> nhắc chụp
màn hình -> ráp thành draft.mp4.

Dùng:
    python3 pipeline/run_all.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
    python3 pipeline/run_all.py <script.md> --dry-run   # xem trước, chưa tốn phí

Nếu có cảnh cần ảnh chụp màn hình mà chưa có sẵn trong assets/<slug>/screenshots/,
script sẽ dừng lại và liệt kê chính xác cần chụp gì trước khi ráp -- xong rồi
chạy lại lệnh này (hoặc `python3 pipeline/assemble.py <script.md>`) để tiếp tục.
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import assets_dir_for, load_script  # noqa: E402

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--voice", default="Kore")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    assets_dir = assets_dir_for(args.script)
    _, scenes = load_script(args.script)
    screenshot_scenes = [s for s in scenes if not s.is_ai_video]

    print("=== Bước 1/3: giọng đọc AI ===")
    subprocess.run(
        [sys.executable, str(HERE / "generate_voice.py"), str(args.script), "--voice", args.voice]
        + (["--dry-run"] if args.dry_run else []),
        check=True,
    )

    print("\n=== Bước 2/3: cảnh AI-video (Veo) ===")
    subprocess.run(
        [sys.executable, str(HERE / "generate_scenes.py"), str(args.script)] + (["--dry-run"] if args.dry_run else []),
        check=True,
    )

    print("\n=== Bước 3/3: ráp video ===")
    if args.dry_run:
        print("(--dry-run: dừng ở đây, không ráp video)")
        return

    missing = [s for s in screenshot_scenes if not any((assets_dir / "screenshots" / f"{s.index:02d}{ext}").exists() for ext in (".png", ".jpg", ".jpeg", ".webp"))]
    if missing:
        print(f"\nCần chụp {len(missing)} ảnh màn hình trước khi ráp video, lưu vào {assets_dir / 'screenshots'}/NN.png:")
        for s in missing:
            print(f"  #{s.index:02d} ({s.time_range}): {s.description}")
        print("\nChụp xong, chạy lại: python3 pipeline/run_all.py " + str(args.script))
        return

    subprocess.run([sys.executable, str(HERE / "assemble.py"), str(args.script)], check=True)


if __name__ == "__main__":
    main()
