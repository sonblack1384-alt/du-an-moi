# Pipeline sản xuất video tự động — mặc định 100% MIỄN PHÍ

> **Cập nhật 2026-09-26:** đã bỏ phụ thuộc vào Veo (trả phí) làm mặc định. Giờ pipeline tạo được **giọng đọc thật (Gemini TTS, miễn phí)** và **cảnh minh hoạ thật (đồ hoạ chuyển động dựng bằng Pillow + ffmpeg, miễn phí, không giới hạn)**. Veo chỉ còn là lựa chọn phụ (xem cuối file) khi muốn hình ảnh AI photorealistic và chấp nhận trả phí.

Dùng chung cho **mọi kênh** trong `channels/` — không cần sửa gì khi thêm kênh mới, chỉ cần trỏ đúng đường dẫn file kịch bản.

## Vì sao đổi từ Veo sang đồ hoạ tự dựng
Người dùng phản đối chi phí Veo (~$0.05-0.40/giây video tuỳ model, xem mục "Chi phí Veo" cuối file) và yêu cầu tìm hướng miễn phí thật. Đã thử: ElevenLabs, RunwayML, edge-tts, Google Translate TTS, FPT.AI, Zalo AI, VBee, HuggingFace, Replicate, Play.ht, Deepgram, Azure, Pexels, Pixabay, Yandex... **tất cả bị chặn bởi chính sách mạng của môi trường này** (chỉ domain Google API + AWS + Google Fonts gọi được). Thử cả Gemini native image generation (`gemini-3.1-flash-lite-image`...) — cũng bị chặn billing y hệt Veo (`limit: 0` free tier).

**Giải pháp thực tế:** phần lớn các cảnh "AI text-to-video" trong kịch bản thực chất là card đồ hoạ đơn giản (cảnh báo, so sánh, đồng hồ, CTA...), không cần hình ảnh photorealistic. `generate_motion_graphic.py` dựng thẳng các card này bằng Pillow (nền màu + chữ động, đúng bảng màu/font thương hiệu ở `channels/ai-de-dung/strategy/08-nhan-dien-thuong-hieu.md`, dùng font **Be Vietnam Pro** tải từ Google Fonts — domain này gọi được và có đủ dấu tiếng Việt) rồi áp hiệu ứng Ken Burns bằng ffmpeg — ghi ra đúng vị trí `assets/<slug>/scenes/NN.mp4` mà `generate_scenes.py` (Veo) từng ghi, nên `assemble.py` dùng chung, không cần sửa gì.

## ✅ Đã test thật (2026-09-26)
- **`generate_voice.py` (Gemini TTS):** hoạt động, đã tạo giọng đọc thật cho cả 16/16 video, miễn phí (quota 10 lượt/model/ngày, tính riêng theo từng model — xem `generate_voice.py` để đổi model nếu cần).
- **`generate_motion_graphic.py`:** hoạt động, đã dựng cảnh minh hoạ thật cho cả 16/16 video, miễn phí hoàn toàn, không giới hạn số lần chạy (chạy local, không gọi API nào).
- **`generate_scenes.py` (Veo):** vẫn dùng được nếu bật billing, nhưng không còn là mặc định — xem mục "Option phụ: Veo" cuối file.

## Cài đặt (1 lần)
```
pip install -r pipeline/requirements.txt
```
`ffmpeg` cũng cần có sẵn (`apt-get install ffmpeg` nếu phiên mới chưa có). Font Be Vietnam Pro Bold đã tải sẵn vào `pipeline/assets/fonts/` — nếu thiếu, tải lại:
```
curl -sL "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HSMIF8y.ttf" -o pipeline/assets/fonts/BeVietnamPro-Bold.ttf
```

## Chạy trọn 1 video (miễn phí)
```
python3 pipeline/generate_voice.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
python3 pipeline/generate_motion_graphic.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
python3 pipeline/assemble.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
```
`assemble.py` sẽ báo thiếu ảnh chụp màn hình nếu chưa có — chụp theo đúng mô tả trong "Bảng cảnh AI" của kịch bản, lưu vào `assets/<slug>/screenshots/NN.png` (NN = số thứ tự cảnh, 2 chữ số), rồi chạy lại.

## Chạy hàng loạt nhiều video
```
for f in channels/ai-de-dung/scripts/*.md; do
  python3 pipeline/generate_voice.py "$f"
  python3 pipeline/generate_motion_graphic.py "$f"
done
```
(Chạy `assemble.py` riêng từng video sau khi đã có đủ ảnh chụp màn hình thật.)

## Sau khi có draft.mp4
Mở trong CapCut để bật auto-caption tiếng Việt (1 click) và kiểm tra checklist QC ở `../channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md`, rồi xuất bản.

## Cấu trúc file
| File | Việc | Tốn phí? |
|---|---|---|
| `common.py` | Parse kịch bản `.md` (lời thoại + bảng cảnh), tạo Gemini client | — |
| `generate_voice.py` | Gọi Gemini TTS, xuất `assets/<slug>/voice.wav` | Miễn phí (quota 10/model/ngày) |
| `generate_motion_graphic.py` | Dựng đồ hoạ chuyển động bằng Pillow+ffmpeg, xuất `assets/<slug>/scenes/NN.mp4` | **Miễn phí, không giới hạn** |
| `generate_scenes.py` | (Phụ) Gọi Veo, xuất cùng vị trí trên | Trả phí, cần billing |
| `assemble.py` | Ráp voice + scenes + screenshots bằng ffmpeg thành `assets/<slug>/draft.mp4` | — |
| `run_all.py` | Chạy voice + Veo (`generate_scenes.py`) + assemble liền mạch — **lưu ý: dùng Veo, không dùng `generate_motion_graphic.py`** | Trả phí (do gọi Veo) |
| `export_dashboard_data.py` | Xuất lời thoại + bảng cảnh của mọi kịch bản thành JSON, dùng để cập nhật `dashboard.html` | — |

---

## Option phụ: dùng Veo (trả phí) thay vì đồ hoạ tự dựng

Chỉ cân nhắc khi thật sự cần hình ảnh AI photorealistic thay vì card đồ hoạ chữ/icon.

### Cách 1 — AutoScene (nếu có tài khoản còn credit)
Mở `channels/ai-de-dung/dashboard.html`, copy "Lời thoại thuần" dán vào *Tạo giọng đọc*, copy "Bảng cảnh AI" dán vào *Tạo video* (ô "Nội dung lệnh, mỗi dòng 1 lệnh"). Chi tiết ở `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md`.

### Cách 2 — `pipeline/generate_scenes.py` (Gemini API trực tiếp)
Cần bật billing tại aistudio.google.com trước:
1. **Thêm API credential** — Environment settings → API credentials → "+ Add credential": Name tuỳ ý, Allowed websites = `generativelanguage.googleapis.com`, Custom headers → Name: `x-goog-api-key`, Prefix: để trống, Value: dán API key thật. **Không dán key vào chat.**
2. Bật billing đúng project gắn với key đó (xem link "Set up billing" ngay tại trang API Keys của Google AI Studio — tránh nhầm sang project Cloud khác).
3. Test 1 cảnh trước khi chạy hàng loạt: `python3 pipeline/generate_scenes.py <script.md> --only 1`

**Chi phí Veo (giá Vertex AI, tham khảo — Gemini Developer API có thể chênh lệch nhẹ):**
| Model | Giá/giây | Giá/clip 8s |
|---|---|---|
| Veo 3.1 Lite (rẻ nhất, AutoScene mặc định) | $0.05 (720p) | $0.40 |
| Veo 3.1 Fast | $0.25 | $2.00 |
| Veo 3.1 (đầy đủ) | $0.40 | $3.20 |

Toàn bộ 16 video hiện có cần khoảng ~50 cảnh AI-video → **~$20-25 nếu dùng bản Lite** cho trọn bộ (một lần, không phải mỗi ngày). Luôn test 1 cảnh trước, xem Cloud Console báo giá thật, trước khi chạy hàng loạt.

**Model đã xác nhận qua `client.models.list()` (2026-09):**
- TTS: `gemini-3.8-flash-tts`, `gemini-3.1-flash-tts-preview`, `gemini-3.8-flash-lite-tts` (mỗi model quota riêng 10/ngày)
- Veo: `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, `veo-3.1-lite-generate-preview`
- Tên model có thể tiếp tục đổi theo thời gian — nếu gặp lỗi `404 NOT_FOUND`, chạy `client.models.list()` để lấy tên mới.
