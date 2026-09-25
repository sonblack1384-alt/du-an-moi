"""Shared helpers for the zero-filming production pipeline.

Parses the standard script markdown files (see channels/*/scripts/*.md) and
wraps the Gemini API client. Every script in this pipeline reads
GEMINI_API_KEY (or GOOGLE_API_KEY as a fallback) from the environment --
never hardcode a key here, and never pass one on the command line where it
could end up in shell history.
"""
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit(
            "Thiếu API key. Hãy thêm GEMINI_API_KEY (hoặc GOOGLE_API_KEY) vào "
            "environment secrets (cloud environment menu -> Edit), không dán "
            "trực tiếp vào lệnh hay vào code."
        )
    return key


def get_client():
    from google import genai

    return genai.Client(api_key=get_api_key())


@dataclass
class Scene:
    index: int
    time_range: str
    description: str
    source: str  # "Ảnh chụp màn hình" hoặc "AI text-to-video"
    note: str  # ghi chú, hoặc prompt cho AI text-to-video

    @property
    def is_ai_video(self) -> bool:
        return "ai text-to-video" in self.source.lower() or "text-to-video" in self.source.lower()

    @property
    def prompt(self) -> str:
        """Trích prompt AI-video ra khỏi cột ghi chú (bỏ ngoặc kép bao ngoài nếu có)."""
        text = self.note.strip()
        m = re.search(r'"([^"]+)"', text)
        return m.group(1) if m else text

    @property
    def duration_seconds(self) -> float:
        """Ước lượng độ dài (giây) từ chuỗi thời điểm dạng '0:00-0:10'."""
        m = re.match(r"\s*(\d+):(\d+)\s*-\s*(\d+):(\d+)", self.time_range)
        if not m:
            return 5.0
        m1, s1, m2, s2 = (int(x) for x in m.groups())
        return max(1.0, (m2 * 60 + s2) - (m1 * 60 + s1))


def slug_from_path(script_path: Path) -> str:
    return script_path.stem  # ví dụ "01-chatgpt-la-gi"


def parse_section(md_text: str, heading_prefix: str) -> str:
    """Trả về nội dung nằm dưới heading '## <heading_prefix>...' tới heading '## ' kế tiếp."""
    lines = md_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## ") and heading_prefix in line:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].strip().startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def parse_narration(md_text: str) -> str:
    """Ghép các đoạn blockquote trong mục 'Lời thoại thuần' thành 1 văn bản liên tục."""
    section = parse_section(md_text, "Lời thoại thuần")
    paragraphs, current = [], []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            content = stripped.lstrip(">").strip()
            if content:
                current.append(content)
        else:
            if current:
                paragraphs.append(" ".join(current))
                current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def parse_scenes(md_text: str) -> list[Scene]:
    """Đọc bảng markdown trong mục 'Bảng cảnh AI' thành danh sách Scene."""
    section = parse_section(md_text, "Bảng cảnh AI")
    rows = [l for l in section.splitlines() if l.strip().startswith("|")]
    scenes = []
    idx = 0
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower().startswith("thời điểm") or set(cells[0]) <= {"-", ":"}:
            continue  # header hoặc dòng phân cách
        idx += 1
        scenes.append(Scene(index=idx, time_range=cells[0], description=cells[1], source=cells[2], note=cells[3]))
    return scenes


def load_script(script_path: Path):
    text = Path(script_path).read_text(encoding="utf-8")
    return parse_narration(text), parse_scenes(text)


def assets_dir_for(script_path: Path) -> Path:
    # channels/<kênh>/scripts/NN-slug.md -> channels/<kênh>/assets/NN-slug/
    channel_dir = Path(script_path).resolve().parent.parent
    return channel_dir / "assets" / slug_from_path(Path(script_path))
