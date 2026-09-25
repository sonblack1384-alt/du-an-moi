#!/usr/bin/env python3
"""Ráp video nháp từ voice.wav + ảnh chụp màn hình + cảnh AI-video đã tạo.

Yêu cầu trước khi chạy (xem pipeline/README.md):
  assets/<slug>/voice.wav              <- từ generate_voice.py
  assets/<slug>/scenes/NN.mp4          <- từ generate_scenes.py (các cảnh AI-video)
  assets/<slug>/screenshots/NN.png|jpg <- bạn tự chụp, đặt theo đúng số thứ tự
                                           cảnh trong "Bảng cảnh AI" của kịch bản

Độ dài mỗi cảnh được co giãn theo tỉ lệ thời lượng đã ghi trong kịch bản, rồi
scale lại cho khớp đúng độ dài thật của file giọng đọc (voice.wav) -- vì giọng
đọc AI đọc nhanh/chậm khác với ước lượng ban đầu.

Dùng:
    python3 pipeline/assemble.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import assets_dir_for, load_script  # noqa: E402

W, H, FPS = 1920, 1080, 30
IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".webp"]


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def find_screenshot(screenshots_dir: Path, index: int) -> Path | None:
    for ext in IMAGE_EXTS:
        p = screenshots_dir / f"{index:02d}{ext}"
        if p.exists():
            return p
    return None


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def build_ai_video_clip(src: Path, duration: float, out_path: Path):
    run([
        "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{duration:.3f}",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
    ])


def build_screenshot_clip(src: Path, duration: float, out_path: Path):
    frames = max(1, int(duration * FPS))
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(src), "-t", f"{duration:.3f}",
        "-vf",
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='min(zoom+0.0008,1.15)':d={frames}:s={W}x{H}:fps={FPS}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
    ])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--assets-dir", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    assets_dir = args.assets_dir or assets_dir_for(args.script)
    voice_path = assets_dir / "voice.wav"
    scenes_dir = assets_dir / "scenes"
    screenshots_dir = assets_dir / "screenshots"
    out_path = args.out or (assets_dir / "draft.mp4")

    if not voice_path.exists():
        sys.exit(f"Chưa có {voice_path} -- chạy generate_voice.py trước.")

    _, scenes = load_script(args.script)
    if not scenes:
        sys.exit("Không đọc được 'Bảng cảnh AI' từ kịch bản.")

    audio_duration = ffprobe_duration(voice_path)
    authored_total = sum(s.duration_seconds for s in scenes)
    print(f"[assemble] Độ dài giọng đọc thật: {audio_duration:.1f}s | tổng thời lượng ước tính trong kịch bản: {authored_total:.1f}s")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        clip_paths = []
        for s in scenes:
            duration = s.duration_seconds / authored_total * audio_duration
            clip_path = tmp / f"clip_{s.index:02d}.mp4"
            if s.is_ai_video:
                src = scenes_dir / f"{s.index:02d}.mp4"
                if not src.exists():
                    sys.exit(f"Thiếu {src} -- chạy generate_scenes.py trước (hoặc kiểm tra lại số thứ tự cảnh).")
                print(f"  Cảnh #{s.index}: AI-video, {duration:.1f}s <- {src.name}")
                build_ai_video_clip(src, duration, clip_path)
            else:
                src = find_screenshot(screenshots_dir, s.index)
                if src is None:
                    sys.exit(
                        f"Thiếu ảnh chụp màn hình cho cảnh #{s.index} trong {screenshots_dir} "
                        f"(đặt tên {s.index:02d}.png hoặc .jpg). Mô tả cảnh cần chụp: {s.description}"
                    )
                print(f"  Cảnh #{s.index}: ảnh chụp màn hình, {duration:.1f}s <- {src.name}")
                build_screenshot_clip(src, duration, clip_path)
            clip_paths.append(clip_path)

        filelist = tmp / "filelist.txt"
        filelist.write_text("\n".join(f"file '{p}'" for p in clip_paths), encoding="utf-8")
        concatenated = tmp / "concatenated.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(filelist), "-c", "copy", str(concatenated)])

        out_path.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y", "-i", str(concatenated), "-i", str(voice_path),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", str(out_path),
        ])

    print(f"\n[assemble] Xong: {out_path}")
    print("Bước tiếp theo: mở file này trong CapCut để bật auto-caption tiếng Việt,")
    print("kiểm tra QC theo checklist ở strategy/05-quy-trinh-lam-video-nhanh.md, rồi xuất bản.")


if __name__ == "__main__":
    main()
