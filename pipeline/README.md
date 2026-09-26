# Pipeline sản xuất video tự động (Gemini API — Veo + TTS)

> **Có tài khoản AutoScene (hoặc tool tương tự) còn credit?** Dùng luôn tool đó trước — nhanh hơn, không cần setup gì. Mở `channels/ai-de-dung/dashboard.html`, copy "Lời thoại thuần" dán vào *Tạo giọng đọc*, copy "Bảng cảnh AI" dán vào *Tạo video* (ô "Nội dung lệnh, mỗi dòng 1 lệnh"). Chi tiết ở `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md` (Option A). Pipeline dưới đây là **Option B** — tự host bằng Gemini API trực tiếp, dùng khi không có/hết credit AutoScene hoặc muốn kiểm soát nhiều hơn.

Bộ script Python gọi thẳng API của Google để tự động hoá tối đa phần sản xuất: **giọng đọc AI (Gemini TTS)** và **cảnh video AI (Veo)**. Phần duy nhất còn cần tay người: chụp vài tấm ảnh màn hình thao tác thật (không phải quay), vì AI-video không thể tái tạo chính xác giao diện phần mềm thật.

Dùng chung cho **mọi kênh** trong `channels/` — không cần sửa gì khi thêm kênh mới, chỉ cần trỏ đúng đường dẫn file kịch bản.

## Vì sao chọn Google Gemini API (không phải ElevenLabs/Runway/Pika)
Đã kiểm tra thực tế trong môi trường chạy: `generativelanguage.googleapis.com` (Gemini API, gồm Veo + TTS) **gọi được**. `api.elevenlabs.io` và `api.runwayml.com` **bị chặn** bởi chính sách mạng của môi trường này. Vì vậy pipeline này dùng 100% Google Gemini API.

## ✅ Đã test thật (2026-09-26) — xem WORKLOG.md mốc #7 để biết chi tiết
- **TTS (giọng đọc): hoạt động thật**, đã tạo file `.wav` thật cho video #1, nghe ổn.
- **Veo (video): bị chặn bởi billing** — tài khoản Google AI cần bật billing/plan trả phí mới dùng được Veo (lỗi `429 RESOURCE_EXHAUSTED` nếu chưa bật). Bật tại https://aistudio.google.com/ → Billing.
- Tên model đã cập nhật theo API thật tại thời điểm test: TTS = `gemini-3.8-flash-tts`, Veo = `veo-3.1-generate-preview`. Model có thể tiếp tục đổi theo thời gian — nếu gặp lỗi `404 NOT_FOUND` nhắc tên model mới, cập nhật lại `TTS_MODEL`/`VEO_MODEL` trong `generate_voice.py`/`generate_scenes.py`.
- **Tốn phí thật** theo tài khoản Google AI của bạn khi bật billing — Veo tính phí theo giây video, TTS tính theo ký tự.
- Claude không tự chạy các script này để tốn phí thay bạn trừ khi được yêu cầu trực tiếp trong phiên chat.

## Cài đặt (1 lần)
1. **Thêm API key** — dùng mục **"API credentials"** trong Environment settings (menu môi trường cloud → Edit), **không phải** mục "Environment variables" (mục đó cấm chứa secret). Bấm "+ Add credential":
   - **Name** (tên credential, tuỳ ý): ví dụ `Gemini API`
   - **Allowed websites**: `generativelanguage.googleapis.com`
   - **Custom headers** → Name: `x-goog-api-key`, Prefix: để trống, Value: dán API key thật (lấy tại Google AI Studio)
   - Bấm **Connect**. Hệ thống sẽ tự tiêm header này vào mọi request tới domain trên — code không bao giờ thấy giá trị key thật (`pipeline/common.py::get_api_key()` chỉ trả về 1 chuỗi placeholder, không đọc secret từ đâu cả). **Không dán key vào chat.**
2. Cài thư viện (đã cài sẵn trong phiên hiện tại, chạy lại nếu phiên mới):
   ```
   pip install -r pipeline/requirements.txt
   ```
   `ffmpeg` cũng cần có sẵn (đã cài qua `apt-get install ffmpeg` trong phiên hiện tại).

## Chạy thử an toàn (khuyên làm trước, gần như miễn phí)
```
python3 pipeline/generate_voice.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md --dry-run
python3 pipeline/generate_scenes.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md --dry-run
```
Hai lệnh trên **không gọi API**, chỉ in ra nội dung/prompt sẽ gửi đi — dùng để kiểm tra file kịch bản parse đúng trước khi tốn phí thật.

Khi đã thêm API credential, thử 1 cảnh Veo trước để xác nhận billing đã bật:
```
python3 pipeline/generate_scenes.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md --only 1
```

## Chạy trọn 1 video
```
python3 pipeline/run_all.py channels/ai-de-dung/scripts/01-chatgpt-la-gi.md
```
Script sẽ: tạo giọng đọc → tạo các cảnh AI-video → kiểm tra ảnh chụp màn hình đã có đủ chưa (nếu thiếu, liệt kê chính xác cần chụp gì và dừng lại) → ráp thành `channels/ai-de-dung/assets/01-chatgpt-la-gi/draft.mp4`.

Chụp màn hình theo đúng mô tả trong mục "Bảng cảnh AI" của file kịch bản, lưu vào `assets/<slug>/screenshots/NN.png` (NN = số thứ tự cảnh, 2 chữ số), rồi chạy lại lệnh trên.

## Sau khi có draft.mp4
Mở trong CapCut để bật auto-caption tiếng Việt (1 click) và kiểm tra checklist QC ở `../channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md`, rồi xuất bản.

## Chạy hàng loạt nhiều video
Chưa có script batch riêng (cố ý — nên chạy từng video một, xem kết quả trước khi tốn phí cho video tiếp theo). Có thể lặp thủ công:
```
for f in channels/ai-de-dung/scripts/0{1,2,3,4}-*.md; do
  python3 pipeline/run_all.py "$f"
done
```

## Cấu trúc file
| File | Việc |
|---|---|
| `common.py` | Parse kịch bản `.md` (lời thoại + bảng cảnh), tạo Gemini client |
| `generate_voice.py` | Gọi Gemini TTS, xuất `assets/<slug>/voice.wav` |
| `generate_scenes.py` | Gọi Veo cho từng cảnh "AI text-to-video", xuất `assets/<slug>/scenes/NN.mp4` |
| `assemble.py` | Ráp voice + scenes + screenshots bằng ffmpeg thành `assets/<slug>/draft.mp4` |
| `run_all.py` | Chạy cả 3 bước trên theo đúng thứ tự cho 1 video |
| `export_dashboard_data.py` | Xuất lời thoại + bảng cảnh của mọi kịch bản thành JSON, dùng để cập nhật `dashboard.html` |
