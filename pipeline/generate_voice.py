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

# CỐ ĐỊNH 1 model duy nhất cho toàn kênh -- KHÔNG tự động đổi sang model khác
# khi hết quota, để tránh giọng đọc nghe khác nhau giữa các video (dù cùng
# voice_name, các model khác nhau có thể render hơi khác chất lượng/âm sắc).
# Đổi model chuẩn của kênh: sửa đúng 1 dòng này rồi tạo lại toàn bộ voice.wav
# cho nhất quán, hoặc dùng --model để test 1 video riêng lẻ trước khi đổi hẳn.
TTS_MODEL = "gemini-3.8-flash-lite-tts"

# Các model khác đã kiểm chứng còn hoạt động (chỉ dùng qua --model khi test,
# KHÔNG dùng làm fallback tự động): gemini-3.8-flash-tts, gemini-3.1-flash-tts-preview.
# Quota miễn phí tính riêng theo từng model (10 lượt/ngày/model) -- nếu
# TTS_MODEL hết quota, script sẽ báo lỗi rõ ràng thay vì tự âm thầm đổi model.


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
    ap.add_argument("--model", default=TTS_MODEL, help=f"Model TTS (mặc định cố định: {TTS_MODEL} -- không tự đổi sang model khác)")
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

    print(f"[generate_voice] Model: {args.model}")
    client = get_client()
    try:
        response = client.models.generate_content(
            model=args.model,
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
    except Exception as e:  # noqa: BLE001 - báo lỗi rõ ràng, không âm thầm đổi model khác
        sys.exit(
            f"Lỗi khi gọi model {args.model}: {e}\n\n"
            f"KHÔNG tự động đổi sang model khác để giữ giọng đọc nhất quán cho cả kênh. "
            f"Nếu hết quota, đợi quota reset (thường theo ngày), hoặc chạy lại với "
            f"--model <model_khac> CHỈ khi chấp nhận giọng video này có thể khác nhẹ so với các video khác."
        )

    if not (response.candidates[0].content and response.candidates[0].content.parts):
        sys.exit(f"Model {args.model} trả về rỗng (có thể do bộ lọc an toàn). Thử lại hoặc kiểm tra nội dung lời thoại.")

    part = response.candidates[0].content.parts[0]
    audio_bytes = part.inline_data.data
    mime = getattr(part.inline_data, "mime_type", "") or ""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if audio_bytes[:4] == b"RIFF" or "wav" in mime.lower():
        # API đã trả về file .wav hoàn chỉnh (đã kiểm chứng thật, 2026-09) -- ghi thẳng, không bọc lại.
        out_path.write_bytes(audio_bytes)
    else:
        # Fallback: một số phiên bản model trả PCM thô, tự bọc thành .wav.
        sample_rate = 24000
        if "rate=" in mime:
            try:
                sample_rate = int(mime.split("rate=")[1].split(";")[0])
            except (ValueError, IndexError):
                pass
        out_path.write_bytes(pcm_to_wav_bytes(audio_bytes, sample_rate=sample_rate))
    print(f"[generate_voice] Đã lưu {out_path} (mime: {mime})")


if __name__ == "__main__":
    main()
