#!/usr/bin/env python3
"""Tạo giọng đọc AI (Gemini TTS) từ phần "Lời thoại thuần" trong 1 file kịch bản.

Dùng:
    python3 pipeline/generate_voice.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
    python3 pipeline/generate_voice.py <script.md> --voice Kore --dry-run

--dry-run: chỉ in ra văn bản sẽ gửi đi + nơi sẽ lưu file, KHÔNG gọi API
(dùng để kiểm tra parsing mà không tốn phí, không cần API key).
"""
import argparse
import struct
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import assets_dir_for, get_client, load_script  # noqa: E402

TTS_MODEL = "gemini-2.5-flash-preview-tts"


def pcm_to_wav_bytes(pcm_bytes: bytes, sample_rate: int = 24000, channels: int = 1, sample_width: int = 2) -> bytes:
    import io

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("script", type=Path, help="Đường dẫn file kịch bản .md")
    ap.add_argument("--voice", default="Kore", help="Tên giọng đọc prebuilt của Gemini TTS (mặc định: Kore)")
    ap.add_argument("--out", type=Path, default=None, help="Đường dẫn file .wav xuất ra (mặc định: assets/<slug>/voice.wav)")
    ap.add_argument("--dry-run", action="store_true", help="Chỉ in ra, không gọi API")
    args = ap.parse_args()

    narration, _ = load_script(args.script)
    if not narration.strip():
        sys.exit(f"Không tìm thấy mục 'Lời thoại thuần' trong {args.script} — kiểm tra lại định dạng file kịch bản.")

    out_path = args.out or (assets_dir_for(args.script) / "voice.wav")

    print(f"[generate_voice] Script: {args.script}")
    print(f"[generate_voice] Số ký tự lời thoại: {len(narration)}")
    print(f"[generate_voice] Giọng: {args.voice}")
    print(f"[generate_voice] Sẽ lưu vào: {out_path}")

    if args.dry_run:
        print("\n--- NỘI DUNG LỜI THOẠI (dry-run, chưa gọi API) ---\n")
        print(narration)
        return

    from google.genai import types

    client = get_client()
    response = client.models.generate_content(
        model=TTS_MODEL,
        contents=narration,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=args.voice)
                )
            ),
        ),
    )
    part = response.candidates[0].content.parts[0]
    pcm_bytes = part.inline_data.data
    mime = getattr(part.inline_data, "mime_type", "") or ""
    sample_rate = 24000
    if "rate=" in mime:
        try:
            sample_rate = int(mime.split("rate=")[1].split(";")[0])
        except (ValueError, IndexError):
            pass

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(pcm_to_wav_bytes(pcm_bytes, sample_rate=sample_rate))
    print(f"[generate_voice] Đã lưu {out_path} ({sample_rate}Hz)")


if __name__ == "__main__":
    main()
