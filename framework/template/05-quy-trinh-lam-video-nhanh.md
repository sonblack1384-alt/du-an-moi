# 5. Quy trình sản xuất video — Zero-filming (100% AI, không quay/không thu âm tay)

> **Giới hạn cần biết:** Claude không có công cụ tạo ảnh/video/audio thật — không tự render được file video. Claude làm được: viết kịch bản, tách lời thoại thuần để dán vào tool AI, và soạn prompt hình ảnh cho từng cảnh (mục "Bảng cảnh AI" trong mỗi file ở `../scripts/`). Phần bấm generate/ghép/xuất video vẫn cần người dùng thao tác trên tool — nhưng mỗi bước chỉ là copy-paste + bấm nút, không cần quay hay đọc thoại.

## Quy trình 6 bước
1. **Lấy kịch bản có sẵn** — mỗi video trong `../backlog.md` có file ở `../scripts/NN-slug.md` gồm lời thoại + "Lời thoại thuần" + "Bảng cảnh AI".
2. **Tạo giọng đọc AI** — dán "Lời thoại thuần" vào {{công cụ TTS phù hợp ngôn ngữ/thị trường của kênh, ví dụ CapCut TTS/FPT.AI/ElevenLabs cho tiếng Việt}}.
3. **Chụp màn hình cho cảnh demo thao tác thật** (chụp, không quay — vài giây/tấm) — theo đúng mô tả trong "Bảng cảnh AI" có nguồn = "Ảnh chụp màn hình".
4. **Tạo cảnh AI-video cho hook/B-roll** — copy prompt trong "Bảng cảnh AI" có nguồn = "AI text-to-video", dán vào CapCut AI / Pika / Kling / Runway.
5. **Dựng & ráp tự động** — nhanh nhất: dán "Lời thoại thuần" vào InVideo AI/Pictory để ra bản nháp tự động, rồi thay các đoạn stock chung chung bằng ảnh/cảnh đã tạo ở bước 3-4. Kiểm soát nhiều hơn: dựng tay trong CapCut, bật Smart Motion + auto-caption (1 click).
6. **Thumbnail, đăng tải, tối ưu SEO, tái sử dụng** — giữ nguyên checklist thông thường (template Canva, tiêu đề/mô tả/tag theo từ khoá, chapters, pinned comment, end screen, cắt Shorts sau 48h từ cảnh đã có).

## Checklist kiểm soát chất lượng (QC) trước khi đăng
- [ ] Giọng đọc AI phát âm đúng, tốc độ tự nhiên
- [ ] Ảnh/cảnh AI khớp đúng nội dung đang nói tại từng thời điểm
- [ ] Ảnh tĩnh có hiệu ứng chuyển động, không "đứng hình" quá 2-3 giây
- [ ] Text overlay không lỗi chính tả
- [ ] Thumbnail rõ chữ khi thu nhỏ
- [ ] Tiêu đề khớp 100% nội dung
- [ ] Có chapters/timestamps, CTA + end screen, gắn đúng playlist
- [ ] Nội dung có giá trị thông tin thật, không phải AI-slop lặp lại

## Công cụ đề xuất
| Việc | Công cụ |
|---|---|
| Viết/nghiên cứu kịch bản | Claude, ChatGPT |
| Giọng đọc AI | {{TTS phù hợp ngôn ngữ/thị trường}} |
| Ảnh chụp màn hình | Phím tắt chụp màn hình có sẵn |
| AI text-to-video (hook/B-roll) | CapCut AI / Pika / Kling / Runway |
| Dựng tự động từ kịch bản | InVideo AI / Pictory |
| Dựng có kiểm soát | CapCut (auto-caption + smart motion) |
| Thumbnail | Canva |

## Mẫu prompt viết kịch bản (lưu để tái sử dụng)
```
Bạn là biên kịch video YouTube tiếng Việt chuyên về {{NICHE}}.
Chủ đề video: [ĐIỀN CHỦ ĐỀ]
Đối tượng: {{ĐỐI_TƯỢNG}}
Viết kịch bản {{thời lượng}} theo cấu trúc: Hook (10s) → Xác nhận vấn đề (15s) →
Preview lộ trình (15s) → các bước hướng dẫn chính → Kết quả/case study → CTA.
Giọng văn {{mô tả giọng văn phù hợp niche}}.
Sau kịch bản, tách thêm "Lời thoại thuần" (toàn bộ câu thoại nối liền, không
timecode/nhãn) và "Bảng cảnh AI" (mỗi cảnh: thời điểm | mô tả hình cần có |
nguồn = Ảnh chụp màn hình hoặc AI text-to-video kèm prompt cụ thể).
```
