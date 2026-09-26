# 5. Quy trình sản xuất video — Zero-filming, mặc định 100% MIỄN PHÍ

> **Cập nhật quan trọng:** pipeline tự host (`pipeline/`) giờ tự tạo được **giọng đọc thật** (Gemini TTS) và **cảnh minh hoạ thật** (đồ hoạ chuyển động dựng bằng Pillow/ffmpeg) — hoàn toàn miễn phí, không cần API key trả phí, không cần bật billing, không giới hạn số lần chạy. Đây là đường **mặc định, ưu tiên dùng trước**. Veo/AutoScene chỉ còn là lựa chọn phụ khi muốn ảnh AI photorealistic và chấp nhận trả phí.

## Dashboard tổng hợp
Mở [`../dashboard.html`](../dashboard.html) (hoặc bản đã publish) để xem toàn bộ video kèm nút copy lời thoại/prompt từng cảnh.

## Option A (mặc định, miễn phí) — Tự host bằng `pipeline/`
Chi tiết đầy đủ ở `../../../pipeline/README.md`. Tóm tắt các bước:

1. **Lấy kịch bản có sẵn** — mỗi video trong `../backlog.md` có file ở `../scripts/NN-slug.md`, gồm "Lời thoại thuần" + "Bảng cảnh AI".
2. **Tạo giọng đọc** — `python3 pipeline/generate_voice.py <script.md>` (Gemini TTS, model cố định xem `pipeline/generate_voice.py`, miễn phí trong hạn mức 10 lượt/model/ngày — quota tính riêng theo từng model).
3. **Tạo cảnh minh hoạ** — `python3 pipeline/generate_motion_graphic.py <script.md>` (đồ hoạ chuyển động: chữ động + icon đơn giản theo đúng màu/font thương hiệu ở `08-nhan-dien-thuong-hieu.md`, dựng local bằng Pillow + ffmpeg, **miễn phí hoàn toàn, không giới hạn**).
4. **Ảnh chụp màn hình** — các cảnh nguồn = "Ảnh chụp màn hình" vẫn cần bạn tự chụp (vài giây/tấm, không phải quay — không AI nào thay được phần này), lưu vào `assets/<slug>/screenshots/NN.png`.
5. **Ráp tự động** — `python3 pipeline/assemble.py <script.md>` (ffmpeg: Ken Burns cho ảnh tĩnh, ghép cảnh, mux giọng đọc) → `assets/<slug>/draft.mp4`.
6. **Thumbnail, đăng tải, tối ưu SEO, tái sử dụng** — thumbnail template Canva; đăng tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu, chapters, pinned comment, end screen; sau 48h xem retention graph, cắt đoạn hay thành Shorts.

## Option B (phụ, tốn phí) — Veo qua AutoScene hoặc `pipeline/generate_scenes.py`
Chỉ dùng khi muốn hình ảnh AI photorealistic (không phải đồ hoạ chữ/icon) và chấp nhận trả phí thật (xem ước tính chi phí ở `pipeline/README.md`). Hai cách:
- **AutoScene** (nếu có tài khoản còn credit): *Tạo giọng đọc* dán "Lời thoại thuần" → *Tạo video* (model Veo) bật "Mỗi dòng 1 lệnh", dán "Copy tất cả prompt" từ dashboard → StoryFlow ráp thành phẩm. AutoScene → *Quản lý kênh* để đăng tự động (chỉ bạn kết nối được tài khoản thật).
- **`pipeline/generate_scenes.py`** (Gemini API, cần bật billing tại aistudio.google.com — xem hướng dẫn & ước tính chi phí ở `pipeline/README.md`).

## Bumper mở/kết cố định — BẮT BUỘC, làm 1 lần dùng cho mọi video
Xem `08-nhan-dien-thuong-hieu.md` mục 4. Trước khi ráp video đầu tiên, tạo **1 lần duy nhất** 2 file `intro-bumper.mp4` và `outro-bumper.mp4` (dùng chính `generate_motion_graphic.py` — miễn phí, không cần Veo), lưu vào `../assets/_brand/`. Mọi video ghép: **Bumper mở → Hook riêng của video → nội dung → CTA → Bumper kết**.

## Checklist kiểm soát chất lượng (QC) trước khi đăng
- [ ] Giọng đọc AI phát âm đúng, tốc độ tự nhiên (nghe thử toàn bộ trước khi ráp)
- [ ] Ảnh/cảnh khớp đúng nội dung đang nói tại từng thời điểm (không bị lệch hình-tiếng)
- [ ] Ảnh tĩnh có hiệu ứng chuyển động, không bị "đứng hình" quá 2-3 giây
- [ ] Text overlay không lỗi chính tả
- [ ] Thumbnail rõ chữ khi thu nhỏ bằng kích thước điện thoại
- [ ] Tiêu đề khớp 100% nội dung
- [ ] Có chapters/timestamps, CTA + end screen, gắn đúng playlist trụ cột
- [ ] Nội dung có giá trị thông tin thật, không phải AI-slop lặp lại (xem lưu ý an toàn cộng đồng ở `00-tong-quan-kenh.md`)
- [ ] Có bumper mở + bumper kết cố định, watermark góc màn hình xuyên suốt, đúng font/màu thương hiệu

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
