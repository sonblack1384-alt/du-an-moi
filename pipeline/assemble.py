#!/usr/bin/env python3
"""Ráp video nháp từ voice.wav + ảnh chụp màn hình + cảnh AI-video đã tạo.

Yêu cầu trước khi chạy (xem pipeline/README.md):
  assets/<slug>/voice.wav              <- từ generate_voice.py
  assets/<slug>/scenes/NN.mp4          <- từ generate_scenes.py (các cảnh AI-video)
  assets/<slug>/screenshots/NN.png|jpg <- bạn tự chụp, đặt theo đúng số thứ tự
                                           cảnh trong "Bảng cảnh AI" của kịch bản.
                                           Cảnh cần NHIỀU ảnh (ghi chú "X tấm"):
                                           đặt tên NNa.png, NNb.png, NNc.png...
                                           -- sẽ tự chia đều thời lượng cho từng ảnh.

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


def find_screenshots(screenshots_dir: Path, index: int) -> list[Path]:
    """Tìm ảnh cho cảnh #index -- hỗ trợ NHIỀU ảnh cho 1 cảnh (đặt tên 04a.png,
    04b.png, 04c.png...) khi "Bảng cảnh AI" yêu cầu nhiều tấm cho cùng 1 khoảng
    thời gian (ví dụ "chụp từng prompt + kết quả, 3 tấm"). Vẫn nhận tên đơn giản
    04.png nếu chỉ có 1 ảnh. Trả về danh sách đã sắp xếp, rỗng nếu chưa có ảnh nào.
    """
    matches: list[Path] = []
    for ext in IMAGE_EXTS:
        matches.extend(screenshots_dir.glob(f"{index:02d}*{ext}"))
    return sorted(matches)


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def build_ai_video_clip(src: Path, duration: float, out_path: Path):
    run([
        "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{duration:.3f}",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
    ])


def build_single_screenshot_clip(src: Path, duration: float, out_path: Path):
    frames = max(1, int(duration * FPS))
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(src), "-t", f"{duration:.3f}",
        "-vf",
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='min(zoom+0.0008,1.15)':d={frames}:s={W}x{H}:fps={FPS}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
    ])


def build_screenshot_clip(srcs: list[Path], duration: float, out_path: Path, tmp: Path, tag: str):
    """Ráp 1 hoặc nhiều ảnh chụp màn hình thành 1 clip dài `duration` giây --
    nếu nhiều ảnh, chia đều thời lượng cho từng ảnh (mỗi ảnh 1 đoạn Ken Burns
    riêng) thay vì chỉ hiện đứng yên 1 ảnh cho cả khoảng thời gian dài.
    """
    if len(srcs) == 1:
        build_single_screenshot_clip(srcs[0], duration, out_path)
        return
    per_duration = duration / len(srcs)
    sub_clips = []
    for i, src in enumerate(srcs):
        sub_path = tmp / f"{tag}_sub{i:02d}.mp4"
        build_single_screenshot_clip(src, per_duration, sub_path)
        sub_clips.append(sub_path)
    sub_filelist = tmp / f"{tag}_filelist.txt"
    sub_filelist.write_text("\n".join(f"file '{p}'" for p in sub_clips), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(sub_filelist), "-c", "copy", str(out_path)])


def build_bumper_clip(src: Path, out_path: Path):
    # Bumper đã đúng W/H/FPS (dựng bằng generate_motion_graphic.py) -- chỉ chuẩn hoá codec để concat được.
    run(["ffmpeg", "-y", "-i", str(src), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path)])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--assets-dir", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    assets_dir = args.assets_dir or assets_dir_for(args.script)
    channel_dir = assets_dir.resolve().parent.parent
    voice_path = assets_dir / "voice.wav"
    scenes_dir = assets_dir / "scenes"
    screenshots_dir = assets_dir / "screenshots"
    out_path = args.out or (assets_dir / "draft.mp4")

    # Bumper mở/kết cố định của kênh (BẮT BUỘC theo strategy/08-nhan-dien-thuong-hieu.md
    # mục 4) -- tự động ghép vào đầu/cuối MỌI video nếu đã có sẵn 2 file này,
    # không cần thao tác gì thêm. Tạo 1 lần bằng generate_motion_graphic.py.
    intro_bumper = channel_dir / "assets" / "_brand" / "intro-bumper.mp4"
    outro_bumper = channel_dir / "assets" / "_brand" / "outro-bumper.mp4"

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
        intro_duration = 0.0
        outro_duration = 0.0

        if intro_bumper.exists():
            clip_path = tmp / "clip_00_intro.mp4"
            build_bumper_clip(intro_bumper, clip_path)
            intro_duration = ffprobe_duration(clip_path)
            print(f"  Bumper mở: {intro_duration:.1f}s <- {intro_bumper.name}")
            clip_paths.append(clip_path)
        else:
            print(f"  (Chưa có {intro_bumper} -- bỏ qua bumper mở, xem strategy/08-nhan-dien-thuong-hieu.md)")

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
                srcs = find_screenshots(screenshots_dir, s.index)
                if not srcs:
                    sys.exit(
                        f"Thiếu ảnh chụp màn hình cho cảnh #{s.index} trong {screenshots_dir} "
                        f"(đặt tên {s.index:02d}.png, hoặc {s.index:02d}a.png/{s.index:02d}b.png... "
                        f"nếu cần nhiều ảnh cho cảnh này). Mô tả cảnh cần chụp: {s.description}"
                    )
                print(f"  Cảnh #{s.index}: ảnh chụp màn hình ({len(srcs)} tấm), {duration:.1f}s <- {', '.join(p.name for p in srcs)}")
                build_screenshot_clip(srcs, duration, clip_path, tmp, f"scene{s.index:02d}")
            clip_paths.append(clip_path)

        if outro_bumper.exists():
            clip_path = tmp / "clip_99_outro.mp4"
            build_bumper_clip(outro_bumper, clip_path)
            outro_duration = ffprobe_duration(clip_path)
            print(f"  Bumper kết: {outro_duration:.1f}s <- {outro_bumper.name}")
            clip_paths.append(clip_path)
        else:
            print(f"  (Chưa có {outro_bumper} -- bỏ qua bumper kết, xem strategy/08-nhan-dien-thuong-hieu.md)")

        filelist = tmp / "filelist.txt"
        filelist.write_text("\n".join(f"file '{p}'" for p in clip_paths), encoding="utf-8")
        concatenated = tmp / "concatenated.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(filelist), "-c", "copy", str(concatenated)])

        # Bumper không có giọng đọc riêng -- chèn khoảng lặng đúng bằng độ dài
        # bumper mở/kết vào audio để khớp với video đã dài thêm (thay vì cắt
        # cụt bumper bằng -shortest).
        audio_path = voice_path
        if intro_duration > 0 or outro_duration > 0:
            padded_audio = tmp / "voice_padded.wav"
            af_parts = []
            if intro_duration > 0:
                af_parts.append(f"adelay={int(intro_duration * 1000)}:all=1")
            if outro_duration > 0:
                af_parts.append(f"apad=pad_dur={outro_duration:.3f}")
            run(["ffmpeg", "-y", "-i", str(voice_path), "-af", ",".join(af_parts), str(padded_audio)])
            audio_path = padded_audio

        out_path.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y", "-i", str(concatenated), "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", str(out_path),
        ])

    print(f"\n[assemble] Xong: {out_path}")
    print("Bước tiếp theo: mở file này trong CapCut để bật auto-caption tiếng Việt,")
    print("kiểm tra QC theo checklist ở strategy/05-quy-trinh-lam-video-nhanh.md, rồi xuất bản.")


if __name__ == "__main__":
    main()
