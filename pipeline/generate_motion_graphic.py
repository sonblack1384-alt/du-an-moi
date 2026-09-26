#!/usr/bin/env python3
"""Tạo cảnh minh hoạ bằng đồ hoạ chuyển động dựng thẳng (Pillow + ffmpeg) --
THAY THẾ HOÀN TOÀN cho Veo. Không gọi API nào, không tốn phí, không giới hạn
số lần chạy. Dùng đúng bảng màu/font thương hiệu ở
../channels/ai-de-dung/strategy/08-nhan-dien-thuong-hieu.md.

Ghi ra đúng vị trí mà generate_scenes.py (Veo) từng ghi
(assets/<slug>/scenes/NN.mp4) nên KHÔNG cần sửa gì ở assemble.py -- 2 script
này thay thế cho nhau hoàn toàn, chọn 1 trong 2 tuỳ có billing Veo hay không.

Dùng:
    python3 pipeline/generate_motion_graphic.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
    python3 pipeline/generate_motion_graphic.py <script.md> --only 3 --dry-run
"""
import argparse
import math
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Scene, assets_dir_for, load_script  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

# Bảng màu + font thương hiệu -- xem strategy/08-nhan-dien-thuong-hieu.md.
# Đổi ở đây thì mọi cảnh dựng sau đều theo màu/font mới (không cần sửa từng nơi).
BG_COLOR = (0x14, 0x17, 0x1C)
ACCENT_COLOR = (0xE8, 0xA3, 0x3D)
TEXT_COLOR = (0xED, 0xEF, 0xF2)
W, H, FPS = 1920, 1080, 30
FONT_PATH = Path(__file__).resolve().parent / "assets" / "fonts" / "BeVietnamPro-Bold.ttf"


def wrap_text(draw: "ImageDraw.ImageDraw", text: str, font: "ImageFont.FreeTypeFont", max_width: int) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for w in words:
        trial = f"{current} {w}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def pick_style(description: str) -> str:
    d = description.lower()
    if any(k in d for k in ["cảnh báo", "lưu ý", "sai lầm", "warning"]):
        return "warning"
    if any(k in d for k in [" vs ", "so sánh", "khác nhau", "trước/sau", "trước / sau"]):
        return "compare"
    if any(k in d for k in ["cta", "đăng ký", "kết,", "kết quả + cta", "subscribe"]):
        return "cta"
    if any(k in d for k in ["đồng hồ", "thời gian", "giây", "phút"]):
        return "clock"
    return "plain"


_LEAD_IN_PATTERNS = [
    r"^cảnh mở đầu[^:]*:\s*",
    r"^cảnh kết,?\s*chữ\s*",
    r"^cảnh kết,?\s*",
    r"^minh hoạ\s*",
    r"^hình minh hoạ\s*",
    r"^đồ hoạ\s*",
    r"^ảnh chụp màn hình\s*",
]


def shorten_label(description: str, max_words: int = 6) -> str:
    import re

    text = description.split("(")[0].strip().strip(".")
    low = text.lower()
    for pat in _LEAD_IN_PATTERNS:
        m = re.match(pat, low)
        if m:
            text = text[m.end():].strip()
            low = text.lower()
    text = text.translate(str.maketrans("", "", "\"'“”")).strip(" \t—-:,;")
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    return " ".join(words).strip() or description[:40]


def draw_icon(draw: "ImageDraw.ImageDraw", style: str, cx: int, cy: int, size: int):
    if style == "warning":
        h = size
        pts = [(cx, cy - h), (cx - h, cy + h), (cx + h, cy + h)]
        draw.polygon(pts, outline=ACCENT_COLOR, width=6)
        draw.line([(cx, cy - h * 0.35), (cx, cy + h * 0.25)], fill=ACCENT_COLOR, width=8)
        draw.ellipse([cx - 4, cy + h * 0.45, cx + 4, cy + h * 0.55], fill=ACCENT_COLOR)
    elif style == "clock":
        r = size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ACCENT_COLOR, width=8)
        draw.line([(cx, cy), (cx, cy - r * 0.6)], fill=ACCENT_COLOR, width=6)
        draw.line([(cx, cy), (cx + r * 0.4, cy)], fill=ACCENT_COLOR, width=6)
    elif style == "cta":
        r = size
        draw.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.9], outline=ACCENT_COLOR, width=8)
        draw.polygon([(cx - r * 0.35, cy + r * 0.9), (cx + r * 0.35, cy + r * 0.9), (cx, cy + r * 1.3)], fill=ACCENT_COLOR)


def build_frame(description: str, style: str) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype(str(FONT_PATH), 84)
    font_small = ImageFont.truetype(str(FONT_PATH), 40)

    if style == "compare":
        draw.rectangle([0, 0, W // 2 - 4, H], fill=(0x1C, 0x21, 0x29))
        draw.rectangle([W // 2 + 4, 0, W, H], fill=BG_COLOR)
        draw.line([(W // 2, 0), (W // 2, H)], fill=ACCENT_COLOR, width=6)
        vs_font = ImageFont.truetype(str(FONT_PATH), 70)
        bbox = draw.textbbox((0, 0), "VS", font=vs_font)
        draw.text(((W - (bbox[2] - bbox[0])) / 2, (H - (bbox[3] - bbox[1])) / 2 - 200), "VS", font=vs_font, fill=ACCENT_COLOR)

    label = "ĐĂNG KÝ KÊNH" if style == "cta" else shorten_label(description)
    lines = wrap_text(draw, label, font_title, max_width=int(W * 0.72))
    line_height = font_title.size + 20
    total_h = line_height * len(lines)
    start_y = H // 2 - total_h // 2 + 60

    if style in ("warning", "clock", "cta"):
        draw_icon(draw, style, W // 2, start_y - 140, 90)

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, start_y + i * line_height), line, font=font_title, fill=TEXT_COLOR)

    # thanh gạch chân màu accent, đúng nhận diện thương hiệu
    underline_y = start_y + total_h + 30
    draw.rectangle([W // 2 - 70, underline_y, W // 2 + 70, underline_y + 8], fill=ACCENT_COLOR)

    # watermark góc dưới phải (đồng bộ với watermark xuyên suốt video ở strategy/08)
    wm_bbox = draw.textbbox((0, 0), "AI DỄ DÙNG", font=font_small)
    draw.text((W - (wm_bbox[2] - wm_bbox[0]) - 50, H - 90), "AI DỄ DÙNG", font=font_small, fill=ACCENT_COLOR)

    return img


def render_clip(frame: Image.Image, duration: float, out_path: Path):
    with tempfile.TemporaryDirectory() as tmp:
        png_path = Path(tmp) / "frame.png"
        frame.save(png_path)
        frames = max(1, int(duration * FPS))
        subprocess.run(
            [
                "ffmpeg", "-y", "-loop", "1", "-i", str(png_path), "-t", f"{duration:.3f}",
                "-vf", f"zoompan=z='min(zoom+0.0006,1.1)':d={frames}:s={W}x{H}:fps={FPS}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not FONT_PATH.exists():
        sys.exit(f"Thiếu font {FONT_PATH} -- tải Be Vietnam Pro Bold về đúng đường dẫn này trước.")

    _, scenes = load_script(args.script)
    ai_scenes = [s for s in scenes if s.is_ai_video]
    if args.only is not None:
        ai_scenes = [s for s in ai_scenes if s.index == args.only]
    if not ai_scenes:
        sys.exit("Không tìm thấy cảnh 'AI text-to-video' nào (hoặc --only không khớp).")

    out_dir = args.out_dir or (assets_dir_for(args.script) / "scenes")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[generate_motion_graphic] {len(ai_scenes)} cảnh cần dựng -> {out_dir}")
    for s in ai_scenes:
        style = pick_style(s.description)
        label = "ĐĂNG KÝ KÊNH" if style == "cta" else shorten_label(s.description)
        out_path = out_dir / f"{s.index:02d}.mp4"
        print(f"\n--- Cảnh #{s.index} ({s.time_range}) style={style} -> {out_path.name} ---")
        print(f"Chữ hiển thị: {label}")
        if args.dry_run:
            continue
        frame = build_frame(s.description, style)
        render_clip(frame, s.duration_seconds, out_path)
        print(f"Đã lưu {out_path}")

    if args.dry_run:
        print("\n(--dry-run: chưa dựng file nào)")


if __name__ == "__main__":
    main()
