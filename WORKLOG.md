# Nhật ký làm việc & trạng thái dự án

> **Đọc file này đầu tiên** khi mở repo ở bất kỳ phiên Claude/tài khoản nào khác. Mục "TRẠNG THÁI HIỆN TẠI" luôn được cập nhật ở đầu file — phần log bên dưới chỉ để tra cứu lịch sử.

---

## TRẠNG THÁI HIỆN TẠI
*(cập nhật lần cuối: mốc #4 — 2026-09-25)*

### Đã có
- **Khung sườn dùng chung** (`framework/`) — 8 file template + hướng dẫn tạo kênh mới, mặc định zero-filming.
- **Kênh demo "AI Dễ Dùng"** (`channels/ai-de-dung/`) — 8 file chiến lược, backlog 100 ý tưởng, lịch đăng 4 tuần, **8/8 kịch bản đầy đủ** — mỗi kịch bản giờ có thêm mục "Lời thoại thuần" (dán thẳng vào TTS) và "Bảng cảnh AI" (từng cảnh: ảnh chụp màn hình hay prompt AI-video).
- **`pipeline/` — automation thật gọi Google Gemini API** (Veo tạo video + Gemini TTS tạo giọng đọc + ffmpeg ráp): đã viết `common.py`, `generate_voice.py`, `generate_scenes.py`, `assemble.py`, `run_all.py`. Đã kiểm chứng kỹ thuật: parsing kịch bản chạy đúng (test với video #1), toàn bộ chuỗi ráp video (ffmpeg: scale/Ken Burns/concat/mux audio) chạy thành công end-to-end với dữ liệu giả lập (voice.wav giả, scene video giả, screenshot giả) → ra đúng file 1920x1080 H.264+AAC khớp độ dài giọng đọc.
- Đã xác nhận qua test mạng thật: `generativelanguage.googleapis.com` (Gemini API) gọi được từ môi trường này; `api.elevenlabs.io` và `api.runwayml.com` bị chặn bởi chính sách mạng — đây là lý do chọn Google Gemini API làm nền tảng automation thay vì các dịch vụ khác.

### Đang thiếu / chưa làm — ĐIỂM NGHẼN HIỆN TẠI
- **Chưa gọi API Veo/TTS thật lần nào** (không có key) — code gọi API dựa trên tài liệu Gemini API tại thời điểm viết, tên model (`veo-3.0-generate-001`, `gemini-2.5-flash-preview-tts`) và cách gọi SDK **chưa được xác minh với request thật**, có thể cần chỉnh khi chạy lần đầu.
- **Cần người dùng thêm `GEMINI_API_KEY` vào environment secrets** (cloud environment menu → Edit) — Claude không được yêu cầu dán key vào chat. Chưa có key này thì pipeline chỉ chạy được ở chế độ `--dry-run`.
- Sau khi có key: nên chạy thử 1 cảnh (`generate_scenes.py ... --only 1`) trước để xác nhận API hoạt động đúng, rồi mới chạy `run_all.py` cho từng video.
- Vẫn cần người dùng tự chụp vài tấm ảnh màn hình thao tác thật cho mỗi video (không phải quay, chỉ vài giây/tấm) — `run_all.py` sẽ liệt kê chính xác cần chụp gì.
- Chưa kiểm tra tên/handle "AI Dễ Dùng" có bị trùng trên YouTube ngoài đời chưa.
- Kịch bản video #9 trở đi chưa viết — viết tiếp sau khi có số liệu thật hoặc khi chạy hết 8 video hiện có.
- Chưa có kênh thứ 2 (chủ đề khác).

### Câu hỏi đang chờ người dùng quyết định
**Cần người dùng thêm `GEMINI_API_KEY` vào environment secrets để pipeline chạy được thật** (không phải câu hỏi cần trả lời trong chat — là 1 thao tác cần làm trong settings). Sau khi thêm key, báo lại cho Claude (ở phiên này hoặc phiên khác, WORKLOG này sẽ giúp phiên mới hiểu ngay bối cảnh) để chạy thử 1 cảnh trước khi chạy hàng loạt.

### Việc tiếp theo nên làm (theo thứ tự ưu tiên)
1. **Cần người dùng:** thêm `GEMINI_API_KEY` vào environment secrets.
2. Sau khi có key: Claude chạy thử `generate_scenes.py --only 1` + `generate_voice.py` cho 1 video để xác nhận API hoạt động đúng, chỉnh code nếu API đã đổi.
3. Chạy `run_all.py` cho từng video trong 8 video hiện có — mỗi lần sẽ dừng lại xin ảnh chụp màn hình nếu thiếu.
4. Người dùng chụp ảnh màn hình theo đúng danh sách được liệt kê, chạy lại để ra `draft.mp4`.
5. Mở draft trong CapCut bật auto-caption, xuất bản.
6. Sau khi có số liệu thật, viết tiếp kịch bản #9+ và/hoặc mở kênh thứ 2 từ `framework/template/`.

---

## LOG CHI TIẾT (mới nhất ở trên)

### Mốc #4 — 2026-09-25 — Zero-filming + pipeline automation thật (Gemini API)
**Người dùng yêu cầu (2 tin nhắn liên tiếp):** không có thời gian quay, hỏi có dùng được ảnh-chuyển-video/text-to-video không; và nhấn mạnh đã làm thì phải chất lượng, ra kết quả tốt nhất, kể cả tốn phí dùng "flow của Google" cũng được; cũng hỏi có nên làm 1 quy trình HTML không.

**Đã làm:**
1. Thiết kế lại toàn bộ định dạng sản xuất thành **zero-filming**: ảnh chụp màn hình (giây, không quay) + AI text-to-video cho cảnh hook/B-roll + giọng đọc AI + auto-assembly. Cập nhật `channels/ai-de-dung/strategy/00` và `05`, cùng bản tương ứng trong `framework/template/00` và `05` để mặc định dùng cho mọi kênh sau này.
2. Thêm mục **"Lời thoại thuần"** (văn bản đọc liên tục) và **"Bảng cảnh AI"** (từng cảnh: ảnh chụp màn hình hay prompt AI-video) vào cả 8 file kịch bản trong `channels/ai-de-dung/scripts/`.
3. Kiểm tra kỹ thuật mạng: `generativelanguage.googleapis.com` (Google Gemini API — chính là "Flow" người dùng nhắc tới) gọi được; `api.elevenlabs.io`/`api.runwayml.com` bị chặn.
4. Build `pipeline/` — automation thật bằng Python + Gemini API (Veo + TTS) + ffmpeg: `common.py` (parse kịch bản), `generate_voice.py`, `generate_scenes.py`, `assemble.py`, `run_all.py`, `requirements.txt`, `README.md`.
5. Test kỹ thuật: parsing kịch bản đúng (video #1: 4 cảnh AI-video, 2 cảnh ảnh chụp màn hình nhận diện chính xác); toàn bộ chuỗi ffmpeg trong `assemble.py` chạy thành công end-to-end với dữ liệu giả lập, ra đúng video 1920x1080 H.264+AAC khớp độ dài audio.
6. Đây thay cho việc chỉ làm "1 trang HTML" như người dùng hỏi — pipeline chạy server-side (Python) mạnh hơn và an toàn hơn (API key không lộ ra trình duyệt); có thể làm thêm dashboard HTML để xem trạng thái/nội dung ở bước sau nếu cần.

**Điểm nghẽn hiện tại:** chưa có `GEMINI_API_KEY` nên chưa gọi API thật được lần nào — code gọi Veo/TTS dựa trên tài liệu API tại thời điểm viết, chưa xác minh với request thật.

---

### Mốc #3 — 2026-09-25 — Hoàn thành kịch bản cho toàn bộ 4 tuần đầu
**Đã làm:** viết tiếp 4 kịch bản đầy đủ còn thiếu (video #5 AI miễn phí tốt nhất, #6 AI viết CV, #7 AI viết email, #8 Gemini trên điện thoại) trong `channels/ai-de-dung/scripts/`. Cập nhật `backlog.md` và `content-calendar.md` để phản ánh cả 8/8 video đã sẵn sàng quay.

**Kết quả:** toàn bộ phần lập kế hoạch + viết kịch bản mà Claude tự làm được cho 4 tuần đầu của kênh demo đã hoàn tất. Điểm nghẽn tiếp theo là khâu thực thi vật lý (quay/dựng/đăng) — thuộc về người dùng, không phải việc Claude có thể tự động hoá trong môi trường này.

---

### Mốc #2 — 2026-09-25 — Biến thành khung sườn dùng chung + hệ thống lịch sử làm việc
**Người dùng yêu cầu:** làm kênh "AI Dễ Dùng" thành bản demo cho khung sườn dùng chung để mở rộng nhiều kênh khác chủ đề sau này; tự động hoá mọi thứ có thể; chỉ hỏi ở mốc quan trọng; lưu lịch sử làm việc trong repo để mở lại từ tài khoản Claude khác vẫn tiếp tục được.

**Đã làm:**
- Tái cấu trúc repo: `strategy/` cũ → `channels/ai-de-dung/strategy/`.
- Tạo `framework/` — 8 file template có placeholder `{{...}}` + `framework/README.md` hướng dẫn nhân bản kênh mới.
- Tạo `CLAUDE.md` (tự động load cho mọi phiên Claude Code mở repo) — trỏ về file này, giải thích cấu trúc repo và giới hạn thật (không tự quay/dựng/đăng video được).
- Tạo `WORKLOG.md` (file này) làm nguồn trạng thái duy nhất, thiết kế để phiên/tài khoản Claude khác đọc và chạy tiếp được ngay.
- Tạo `channels/ai-de-dung/backlog.md` — chuyển 100 ý tưởng từ dạng danh sách sang bảng có cột trạng thái.
- Tạo `channels/ai-de-dung/content-calendar.md` — lịch đăng cụ thể 4 tuần đầu.
- Tự động viết thêm 3 kịch bản đầy đủ (video #2, #3, #4) trong `channels/ai-de-dung/scripts/`, nâng tổng số kịch bản sẵn sàng quay lên 4.

**Quyết định tự đưa ra (trong phạm vi "auto mọi thứ"):**
- Cấu trúc thư mục `framework/` + `channels/<slug>/` (hợp lý, dễ mở rộng, không cần hỏi vì có thể sửa lại dễ dàng).
- Thứ tự ưu tiên video #5-8 trong lịch 4 tuần lấy trực tiếp từ Tier 1 của backlog.

**Chưa làm/để lại cho vòng sau:** kịch bản #5-8, và bất kỳ hành động cần thao tác ngoài đời thật (quay/đăng).

---

### Mốc #1 — 2026-09-25 — Tạo bộ chiến lược 7 bước ban đầu
**Người dùng yêu cầu:** chạy tuần tự 7 prompt chiến lược YouTube (ảnh đính kèm) cho dự án `du-an-moi` (lúc đó đang trống).

**Quyết định cần hỏi → đã hỏi người dùng:** niche, định dạng, nguồn lực, mục tiêu. Người dùng trả lời: để Claude tự chọn niche đúng chuyên môn, định dạng để Claude tư vấn, nguồn lực solo/ngân sách thấp, mục tiêu để Claude tư vấn.

**Đã làm:**
- Chọn niche: "Ứng dụng AI vào công việc/kiếm tiền cho người Việt", định dạng faceless (screen recording + giọng đọc), tên kênh "AI Dễ Dùng".
- Viết đủ 7 file chiến lược (`strategy/00` đến `strategy/07` — sau này chuyển vào `channels/ai-de-dung/strategy/` ở Mốc #2), gồm cả 100 ý tưởng video và 1 kịch bản mẫu đầy đủ (video #1).
- Commit & push lên `claude/tender-meitner-0s76lt`.
