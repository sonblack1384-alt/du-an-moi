# 5. Quy trình sản xuất video — Zero-filming, mặc định 100% MIỄN PHÍ

> **Cập nhật (2026-09-26):** mặc định giờ là **KHÔNG cần người dùng tự chụp ảnh/quay/thao tác gì cả** — mọi cảnh (kể cả cảnh trước đây định demo giao diện phần mềm thật) đều dùng đồ hoạ chữ/icon tự dựng bằng `pipeline/generate_motion_graphic.py` (Pillow + ffmpeg, miễn phí, không giới hạn). Kết hợp giọng đọc thật (Gemini TTS), pipeline ráp được video hoàn chỉnh 100% tự động. Đánh đổi: mất cảnh "xem tận mắt thao tác trên giao diện thật" — nếu kênh mới cần độ tin cậy demo cao hơn mức đồ hoạ chữ/icon, có thể chọn dùng ảnh chụp màn hình thật cho MỘT SỐ cảnh (xem cuối mục Option A), nhưng đó là lựa chọn thêm, không phải mặc định. Chi tiết & lý do chọn hướng miễn phí này ở `../../pipeline/README.md`. AI-video trả phí (Veo, Pika, Kling, Runway...) chỉ còn là lựa chọn phụ khi cần ảnh photorealistic.

## Option A (mặc định, miễn phí, KHÔNG cần người dùng thao tác gì) — Tự host bằng `pipeline/`
1. **Lấy kịch bản có sẵn** — mỗi video trong `../backlog.md` có file ở `../scripts/NN-slug.md`, gồm "Lời thoại thuần" + "Bảng cảnh AI" (mọi dòng nên để Nguồn = "AI text-to-video" theo mặc định mới).
2. **Tạo giọng đọc** — `python3 pipeline/generate_voice.py <script.md>` (Gemini TTS, miễn phí trong hạn mức 10 lượt/model/ngày — quota tính riêng theo từng model, xem `pipeline/generate_voice.py` để đổi model nếu cần. **Giữ cố định 1 model/giọng cho toàn kênh, không tự đổi giọng giữa các video.**).
3. **Tạo TẤT CẢ cảnh minh hoạ** — `python3 pipeline/generate_motion_graphic.py <script.md>` (đồ hoạ chuyển động: chữ động + icon đơn giản theo đúng màu/font thương hiệu ở `08-nhan-dien-thuong-hieu.md`, dựng local bằng Pillow + ffmpeg, **miễn phí hoàn toàn, không giới hạn**). Phù hợp cho phần lớn cảnh minh hoạ/B-roll dạng chữ+icon; không tạo được ảnh photorealistic (xem Option B nếu cần).
4. **Ráp tự động** — `python3 pipeline/assemble.py <script.md>` (ffmpeg: Ken Burns, ghép cảnh + bumper, mux giọng đọc) → `assets/<slug>/draft.mp4`. **Không còn bước nào cần người dùng làm trước bước này.**
5. **Thumbnail, đăng tải, tối ưu SEO, tái sử dụng** — thumbnail template Canva; đăng tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu, chapters, pinned comment, end screen; sau 48h xem retention graph, cắt đoạn hay thành Shorts.

*(Tuỳ chọn nâng cấp: nếu muốn 1 vài cảnh dùng ảnh chụp màn hình thật thay vì đồ hoạ chữ, đổi Nguồn dòng đó thành "Ảnh chụp màn hình" và lưu ảnh vào `assets/<slug>/screenshots/NN.png` — `assemble.py` hỗ trợ cả 2 kiểu trộn lẫn.)*

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
định dạng đã dùng ở các video trước trong ../scripts/ (mặc định mọi dòng
Nguồn = "AI text-to-video" -- KHÔNG dùng "Ảnh chụp màn hình" trừ khi người
dùng chủ động muốn nâng cấp 1 vài cảnh), rồi chạy
`python3 pipeline/export_dashboard_data.py ../scripts` để cập nhật dashboard.
```
