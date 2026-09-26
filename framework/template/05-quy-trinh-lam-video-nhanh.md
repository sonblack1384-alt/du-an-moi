# 5. Quy trình sản xuất video — Zero-filming, mặc định 100% MIỄN PHÍ

> **Cập nhật:** nếu kênh dùng chung `pipeline/` của repo này (Gemini TTS + đồ hoạ chuyển động tự dựng bằng Pillow/ffmpeg), phần giọng đọc và cảnh minh hoạ **tự động hoá được thật, miễn phí, không giới hạn số lần chạy** — không chỉ soạn prompt để người dùng tự dán vào tool ngoài nữa. Chi tiết & lý do chọn hướng này ở `../../pipeline/README.md`. Đây là đường **mặc định**; AI-video trả phí (Veo, Pika, Kling, Runway...) chỉ còn là lựa chọn phụ khi cần ảnh photorealistic.

## Option A (mặc định, miễn phí) — Tự host bằng `pipeline/`
1. **Lấy kịch bản có sẵn** — mỗi video trong `../backlog.md` có file ở `../scripts/NN-slug.md`, gồm "Lời thoại thuần" + "Bảng cảnh AI".
2. **Tạo giọng đọc** — `python3 pipeline/generate_voice.py <script.md>` (Gemini TTS, miễn phí trong hạn mức 10 lượt/model/ngày — quota tính riêng theo từng model, xem `pipeline/generate_voice.py` để đổi model nếu cần. **Giữ cố định 1 model/giọng cho toàn kênh, không tự đổi giọng giữa các video.**).
3. **Tạo cảnh minh hoạ** — `python3 pipeline/generate_motion_graphic.py <script.md>` (đồ hoạ chuyển động: chữ động + icon đơn giản theo đúng màu/font thương hiệu ở `08-nhan-dien-thuong-hieu.md`, dựng local bằng Pillow + ffmpeg, **miễn phí hoàn toàn, không giới hạn**). Phù hợp cho phần lớn cảnh minh hoạ/B-roll dạng chữ+icon; không tạo được ảnh photorealistic (xem Option B nếu cần).
4. **Ảnh chụp màn hình** — các cảnh nguồn = "Ảnh chụp màn hình" (demo thao tác thật) vẫn cần người dùng tự chụp (vài giây/tấm, không phải quay — không AI nào thay được phần này), lưu vào `assets/<slug>/screenshots/NN.png`.
5. **Ráp tự động** — `python3 pipeline/assemble.py <script.md>` (ffmpeg: Ken Burns cho ảnh tĩnh, ghép cảnh, mux giọng đọc) → `assets/<slug>/draft.mp4`.
6. **Thumbnail, đăng tải, tối ưu SEO, tái sử dụng** — thumbnail template Canva; đăng tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu, chapters, pinned comment, end screen; sau 48h xem retention graph, cắt đoạn hay thành Shorts.

## Option B (phụ, tốn phí) — AI-video photorealistic
Chỉ dùng khi thật sự cần hình ảnh AI photorealistic (không phải card đồ hoạ chữ/icon) và chấp nhận trả phí thật:
- **`pipeline/generate_scenes.py`** (Veo qua Gemini API, cần bật billing — xem hướng dẫn & ước tính chi phí ở `../../pipeline/README.md`).
- Hoặc công cụ ngoài: {{CapCut AI / Pika / Kling / Runway — chọn theo ngôn ngữ/thị trường của kênh}}, dán prompt từ "Bảng cảnh AI".

## Bumper mở/kết cố định — BẮT BUỘC, làm 1 lần dùng cho mọi video
Xem `08-nhan-dien-thuong-hieu.md` mục 4. Trước khi ráp video đầu tiên, tạo **1 lần duy nhất** 2 file `intro-bumper.mp4` và `outro-bumper.mp4` (dùng `generate_motion_graphic.py` — miễn phí, không cần AI-video trả phí), lưu vào `../assets/_brand/`. Mọi video ghép: **Bumper mở → Hook riêng của video → nội dung → CTA → Bumper kết**.

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

## Công cụ đề xuất
| Việc | Công cụ |
|---|---|
| Viết/nghiên cứu kịch bản | Claude, ChatGPT |
| Giọng đọc AI | `pipeline/generate_voice.py` (Gemini TTS, miễn phí) |
| Cảnh minh hoạ/B-roll (chữ+icon) | `pipeline/generate_motion_graphic.py` (miễn phí, không giới hạn) |
| Ảnh chụp màn hình | Phím tắt chụp màn hình có sẵn |
| AI-video photorealistic (phụ, tốn phí) | `pipeline/generate_scenes.py` (Veo) hoặc {{CapCut AI / Pika / Kling / Runway}} |
| Ráp video | `pipeline/assemble.py` (ffmpeg) |
| Thumbnail | Canva |

## Mẫu prompt viết kịch bản (dùng khi viết video mới)
```
Bạn là biên kịch video YouTube tiếng Việt chuyên về {{NICHE}}.
Chủ đề video: [ĐIỀN CHỦ ĐỀ]
Đối tượng: {{ĐỐI_TƯỢNG}}
Viết kịch bản {{thời lượng}} theo cấu trúc: Hook (10s) → Xác nhận vấn đề (15s) →
Preview lộ trình (15s) → các bước hướng dẫn chính (demo màn hình) →
Kết quả/case study → CTA. Giọng văn {{mô tả giọng văn phù hợp niche}}.
Sau kịch bản, tự tách thêm "Lời thoại thuần" và "Bảng cảnh AI" theo đúng
định dạng đã dùng ở các video trước trong ../scripts/, rồi chạy
`python3 pipeline/export_dashboard_data.py ../scripts` để cập nhật dashboard.
```
