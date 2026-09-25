# 5. Quy trình sản xuất video — Zero-filming (100% AI, không quay/không thu âm tay)

> **Giới hạn cần biết:** Claude (trong môi trường này) không có công cụ tạo ảnh/video/audio thật — không tự render được file video. Những gì Claude làm được: viết kịch bản, tách lời thoại sẵn để dán vào tool AI, và soạn prompt hình ảnh cho từng cảnh (xem mục "Bảng cảnh AI" trong mỗi file ở `../scripts/`). Phần bấm generate/ghép/xuất video vẫn cần bạn thao tác trên tool — nhưng mỗi bước đó chỉ là copy-paste + bấm nút, không cần quay hay đọc thoại.

## Dashboard tổng hợp
Mở [`../dashboard.html`](../dashboard.html) (hoặc bản đã publish) để xem cả 8 video kèm nút copy lời thoại/prompt từng cảnh — dán trực tiếp vào tool ở Option A hoặc B bên dưới, không cần mở từng file kịch bản thủ công.

## Option A — Dùng AutoScene (đã có tài khoản, khuyên dùng vì nhanh nhất)
Nếu bạn đã có tài khoản AutoScene còn credit, đây là đường ngắn nhất — AutoScene tự vận hành Veo (tạo video) + Azure Speech (giọng đọc) phía sau, không cần setup gì thêm:

1. **Tạo giọng đọc**: mở AutoScene → *Tạo giọng đọc* → dán nguyên khối "Lời thoại thuần" của video vào ô "Nội dung văn bản" → chọn ngôn ngữ Tiếng Việt + giọng đọc → Tạo Voice.
2. **Tạo cảnh AI-video**: mở AutoScene → *Tạo video* (model Veo 3.1) → bật toggle "Mỗi dòng 1 lệnh" → dán khối "Copy tất cả prompt" (từ dashboard, đúng thứ tự cảnh) vào ô "Nội dung lệnh" → chọn tỉ lệ khung hình (16:9 cho long-form) và thời lượng mỗi cảnh (8 giây/lệnh — khớp với độ dài mỗi cảnh trong bảng) → Tạo video.
3. **Ảnh chụp màn hình**: các cảnh nguồn = "Ảnh chụp màn hình" vẫn cần bạn tự chụp (vài giây/tấm, không phải quay) — AutoScene không thể tái tạo chính xác giao diện phần mềm thật.
4. **Ráp & xuất**: dùng StoryFlow của AutoScene để ráp giọng đọc + cảnh AI-video + ảnh chụp màn hình thành video hoàn chỉnh, xuất MP4.
5. **Đăng tự động** (tuỳ chọn): AutoScene → *Quản lý kênh* → *Thêm mới* để kết nối kênh YouTube/TikTok thật — chỉ bạn làm được bước kết nối tài khoản này. Sau khi kết nối, AutoScene có thể tự đăng theo lịch.

## Option B — Tự host bằng `pipeline/` (Gemini API, không phụ thuộc credit AutoScene)
Dự phòng khi hết credit AutoScene hoặc muốn kiểm soát nhiều hơn — xem chi tiết ở `../../../pipeline/README.md`. Tóm tắt 6 bước:

1. **Lấy kịch bản có sẵn** — mỗi video trong `../backlog.md` có file ở `../scripts/NN-slug.md`, gồm lời thoại theo đoạn + "Lời thoại thuần" + "Bảng cảnh AI".
2. **Tạo giọng đọc AI** — `python3 pipeline/generate_voice.py <script.md>` (Gemini TTS), hoặc dán "Lời thoại thuần" vào CapCut TTS/FPT.AI/ElevenLabs.
3. **Ảnh chụp màn hình** — như Option A bước 3, lưu vào `assets/<slug>/screenshots/NN.png`.
4. **Cảnh AI-video** — `python3 pipeline/generate_scenes.py <script.md>` (Veo), hoặc dán prompt vào CapCut AI/Pika/Kling/Runway.
5. **Ráp tự động** — `python3 pipeline/assemble.py <script.md>` (ffmpeg: Ken Burns cho ảnh tĩnh, ghép cảnh, mux giọng đọc) → `assets/<slug>/draft.mp4`. Hoặc `python3 pipeline/run_all.py <script.md>` chạy cả bước 2+4+5 liền mạch.
6. **Thumbnail, đăng tải, tối ưu SEO, tái sử dụng** — thumbnail template Canva; đăng tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu, chapters, pinned comment, end screen; sau 48h xem retention graph, cắt đoạn hay thành Shorts.

## Checklist kiểm soát chất lượng (QC) trước khi đăng — áp dụng cho cả 2 Option
- [ ] Giọng đọc AI phát âm đúng, tốc độ tự nhiên (nghe thử toàn bộ trước khi ráp)
- [ ] Ảnh/cảnh AI khớp đúng nội dung đang nói tại từng thời điểm (không bị lệch hình-tiếng)
- [ ] Ảnh tĩnh có hiệu ứng chuyển động, không bị "đứng hình" quá 2-3 giây
- [ ] Text overlay không lỗi chính tả
- [ ] Thumbnail rõ chữ khi thu nhỏ bằng kích thước điện thoại
- [ ] Tiêu đề khớp 100% nội dung
- [ ] Có chapters/timestamps, CTA + end screen, gắn đúng playlist trụ cột
- [ ] Nội dung có giá trị thông tin thật, không phải AI-slop lặp lại (xem lưu ý an toàn cộng đồng ở `00-tong-quan-kenh.md`)

## Mẫu prompt viết kịch bản (dùng khi viết video mới)
```
Bạn là biên kịch video YouTube tiếng Việt chuyên về AI cho người mới.
Chủ đề video: [ĐIỀN CHỦ ĐỀ]
Đối tượng: nhân viên văn phòng/sinh viên VN, chưa rành AI
Viết kịch bản 6-8 phút theo cấu trúc: Hook (10s) → Xác nhận vấn đề (15s) →
Preview lộ trình (15s) → 3 bước hướng dẫn chính (demo màn hình) →
Kết quả/case study → CTA. Giọng văn gần gũi, câu ngắn, không thuật ngữ khó.
Sau kịch bản, tự tách thêm "Lời thoại thuần" và "Bảng cảnh AI" theo đúng
định dạng đã dùng ở các video trước trong ../scripts/, rồi chạy
`python3 pipeline/export_dashboard_data.py ../scripts` để cập nhật dashboard.
```
