#!/usr/bin/env python3
"""Tạo các cảnh video bằng Veo (Gemini API) từ mục "Bảng cảnh AI" trong kịch bản.

Chỉ tạo cho các dòng có nguồn = "AI text-to-video" -- các dòng "Ảnh chụp màn
hình" cần bạn tự chụp và bỏ vào assets/<slug>/screenshots/NN.png (NN = số
thứ tự cảnh, 2 chữ số, theo đúng thứ tự trong bảng).

Dùng:
    python3 pipeline/generate_scenes.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
    python3 pipeline/generate_scenes.py <script.md> --dry-run
    python3 pipeline/generate_scenes.py <script.md> --only 3      # chỉ tạo lại cảnh số 3

Lưu ý chi phí: mỗi cảnh Veo tốn phí thật theo tài khoản Google AI của bạn.
Kịch bản dài ~6-9 phút thường có 4-7 cảnh AI-video (phần còn lại là ảnh chụp
màn hình, không tốn phí Veo). Nên chạy --dry-run trước để xem số cảnh + prompt
trước khi tạo thật.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import assets_dir_for, get_client, load_script  # noqa: E402

VEO_MODEL = "veo-3.0-generate-001"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--aspect-ratio", default="16:9")
    ap.add_argument("--only", type=int, default=None, help="Chỉ tạo cảnh có số thứ tự này")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    _, scenes = load_script(args.script)
    ai_scenes = [s for s in scenes if s.is_ai_video]
    if args.only is not None:
        ai_scenes = [s for s in ai_scenes if s.index == args.only]

    if not ai_scenes:
        sys.exit("Không tìm thấy cảnh 'AI text-to-video' nào trong 'Bảng cảnh AI' (hoặc --only không khớp).")

    out_dir = args.out_dir or (assets_dir_for(args.script) / "scenes")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[generate_scenes] {len(ai_scenes)} cảnh AI-video cần tạo -> {out_dir}")
    for s in ai_scenes:
        out_path = out_dir / f"{s.index:02d}.mp4"
        print(f"\n--- Cảnh #{s.index} ({s.time_range}) -> {out_path.name} ---")
        print(f"Prompt: {s.prompt}")
        if args.dry_run:
            continue

        client = get_client()
        from google.genai import types

        operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=s.prompt,
            config=types.GenerateVideosConfig(aspect_ratio=args.aspect_ratio, number_of_videos=1),
        )
        print("Đang chờ Veo render (có thể mất vài phút)...")
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        if operation.error:
            print(f"LỖI cảnh #{s.index}: {operation.error}", file=sys.stderr)
            continue

        video = operation.response.generated_videos[0].video
        client.files.download(file=video)
        video.save(str(out_path))
        print(f"Đã lưu {out_path}")

    if args.dry_run:
        print("\n(--dry-run: chưa gọi API, chưa tốn phí)")


if __name__ == "__main__":
    main()
