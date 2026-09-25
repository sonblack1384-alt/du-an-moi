#!/usr/bin/env python3
"""Xuất dữ liệu 8 kịch bản (tiêu đề, trạng thái, lời thoại, bảng cảnh) thành JSON
để nhúng vào dashboard HTML. Không phụ thuộc network/API key -- chỉ đọc file .md.

Dùng:
    python3 pipeline/export_dashboard_data.py channels/ai-de-dung/scripts > data.json
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import parse_narration, parse_scenes  # noqa: E402


def parse_meta(md_text: str, path: Path):
    title_line = next((l for l in md_text.splitlines() if l.startswith("# ")), "")
    m = re.search(r'"([^"]+)"', title_line)
    title = m.group(1) if m else path.stem

    meta_line = next((l for l in md_text.splitlines() if l.startswith("**Trụ cột:**")), "")
    pillar = re.search(r"\*\*Trụ cột:\*\*\s*([^·]+)", meta_line)
    fmt = re.search(r"\*\*Định dạng:\*\*\s*([^·]+)", meta_line)
    status = re.search(r"\*\*Trạng thái:\*\*\s*(.+)$", meta_line)

    section = None
    lines = md_text.splitlines()
    for i, l in enumerate(lines):
        if l.strip() == "## Tiêu đề đề xuất":
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    section = lines[j].strip().strip('"')
                    break
            break

    return {
        "title": title,
        "suggestedTitle": section or title,
        "pillar": (pillar.group(1).strip() if pillar else ""),
        "format": (fmt.group(1).strip() if fmt else ""),
        "status": (status.group(1).strip() if status else ""),
    }


def main():
    scripts_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("channels/ai-de-dung/scripts")
    videos = []
    for path in sorted(scripts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_meta(text, path)
        narration = parse_narration(text)
        scenes = parse_scenes(text)
        videos.append({
            "slug": path.stem,
            **meta,
            "narration": narration,
            "scenes": [
                {
                    "index": s.index,
                    "time": s.time_range,
                    "description": s.description,
                    "source": s.source,
                    "isAiVideo": s.is_ai_video,
                    "prompt": s.prompt if s.is_ai_video else "",
                    "note": s.note,
                }
                for s in scenes
            ],
        })
    print(json.dumps(videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
