# 5. Quy trình sản xuất video — Zero-filming (100% AI, không quay/không thu âm tay)

> **Giới hạn cần biết:** Claude (trong môi trường này) không có công cụ tạo ảnh/video/audio thật — không tự render được file video. Những gì Claude làm được: viết kịch bản, tách lời thoại sẵn để dán vào tool AI, và soạn prompt hình ảnh cho từng cảnh (xem mục "Bảng cảnh AI" trong mỗi file ở `../scripts/`). Phần bấm generate/ghép/xuất video vẫn cần bạn thao tác trên các tool bên dưới — nhưng mỗi bước đó chỉ là copy-paste + bấm nút, không cần quay hay đọc thoại.

## Quy trình 6 bước (không còn bước "quay")

### 1. Lấy kịch bản có sẵn
Mỗi video trong `../backlog.md` đã có file kịch bản đầy đủ ở `../scripts/NN-slug.md`, gồm: lời thoại theo từng đoạn, và (từ video áp dụng pipeline mới) **"Lời thoại thuần"** + **"Bảng cảnh AI"** — 2 phần dùng trực tiếp cho các bước dưới.

### 2. Tạo giọng đọc AI (2-5 phút/video)
Dán phần **"Lời thoại thuần"** vào 1 trong các công cụ:
- **CapCut Text-to-Speech** (miễn phí, có giọng tiếng Việt tự nhiên, tích hợp sẵn trong bước dựng ở bước 5 — khuyên dùng vì đỡ phải chuyển file qua lại).
- **FPT.AI TTS** — giọng Việt chuyên biệt, có bản miễn phí giới hạn ký tự/tháng.
- **ElevenLabs** — chất lượng cao nhất, có giọng đa ngôn ngữ, cần trả phí cho hạn mức lớn.

### 3. Lấy ảnh chụp màn hình cho các cảnh demo thao tác (chụp, không quay — vài giây/tấm)
Với các cảnh trong "Bảng cảnh AI" ghi nguồn = **"Ảnh chụp màn hình"**: mở app/web đang hướng dẫn, chụp đúng khoảnh khắc mô tả (phím tắt chụp màn hình có sẵn trên máy). Không cần quay cả quá trình, chỉ cần 1 tấm ảnh tĩnh cho mỗi ý.

### 4. Tạo cảnh AI-video cho hook/B-roll (2-3 phút/cảnh)
Với các cảnh ghi nguồn = **"AI text-to-video"**: copy nguyên văn prompt trong bảng, dán vào 1 trong các công cụ:
- **CapCut AI Video Generator** (tích hợp sẵn trong CapCut, tiện nhất vì cùng app dựng).
- **Pika / Kling / Runway** (bản miễn phí giới hạn số lượt/tháng, chất lượng hình ảnh cao hơn CapCut cho cảnh phức tạp).

### 5. Dựng & ráp tự động
- **Cách nhanh nhất:** dán toàn bộ "Lời thoại thuần" vào **InVideo AI** hoặc **Pictory** — tool tự tách cảnh, tự chọn stock/AI B-roll khớp nội dung, tự chèn giọng đọc AI và phụ đề, ra 1 bản nháp hoàn chỉnh chỉ trong vài phút. Sau đó thay các đoạn stock chung chung bằng ảnh chụp màn hình thật + cảnh AI-video đã tạo ở bước 3-4 để video sát với hướng dẫn thật hơn.
- **Cách kiểm soát nhiều hơn:** dựng thủ công trong **CapCut** — kéo ảnh chụp màn hình + cảnh AI-video vào timeline theo đúng thứ tự trong kịch bản, bật "Smart Motion"/"Auto Reframe" (1 click) để ảnh tĩnh có chuyển động, gắn giọng đọc đã tạo, bật auto-caption tiếng Việt (1 click).
- Áp template intro/outro/lower-third đã lưu sẵn để không phải dựng lại từ đầu mỗi video.

### 6. Thumbnail, đăng tải, tối ưu SEO, tái sử dụng
Giữ nguyên như trước — không đổi vì không liên quan tới khâu quay:
- Thumbnail: template Canva cố định bố cục.
- Đăng: tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu, chapters, pinned comment, end screen.
- Sau 48h: xem retention graph, cắt đoạn hay thành Shorts (cũng dựng bằng CapCut từ chính các cảnh AI/ảnh đã có, không cần tạo mới).

## Checklist kiểm soát chất lượng (QC) trước khi đăng
- [ ] Giọng đọc AI phát âm đúng, tốc độ tự nhiên (nghe thử toàn bộ trước khi ráp)
- [ ] Ảnh/cảnh AI khớp đúng nội dung đang nói tại từng thời điểm (không bị lệch hình-tiếng)
- [ ] Ảnh tĩnh có hiệu ứng chuyển động, không bị "đứng hình" quá 2-3 giây
- [ ] Text overlay không lỗi chính tả
- [ ] Thumbnail rõ chữ khi thu nhỏ bằng kích thước điện thoại
- [ ] Tiêu đề khớp 100% nội dung
- [ ] Có chapters/timestamps, CTA + end screen, gắn đúng playlist trụ cột
- [ ] Nội dung có giá trị thông tin thật, không phải AI-slop lặp lại (xem lưu ý an toàn cộng đồng ở `00-tong-quan-kenh.md`)

## Công cụ đề xuất
| Việc | Công cụ | Ghi chú |
|---|---|---|
| Viết/nghiên cứu kịch bản | Claude, ChatGPT | Đã có sẵn ở `../scripts/` |
| Giọng đọc AI | CapCut TTS / FPT.AI / ElevenLabs | Ưu tiên CapCut để đỡ chuyển file |
| Ảnh chụp màn hình | Phím tắt chụp màn hình có sẵn | Không cần phần mềm riêng |
| AI text-to-video (hook/B-roll) | CapCut AI / Pika / Kling / Runway | Dùng prompt có sẵn trong từng kịch bản |
| Dựng tự động từ kịch bản | InVideo AI / Pictory | Nhanh nhất, ra bản nháp trong vài phút |
| Dựng có kiểm soát | CapCut | Auto-caption + Smart Motion 1-click |
| Thumbnail | Canva | Template cố định bố cục |

## Mẫu prompt viết kịch bản (giữ nguyên, dùng khi viết video mới)
```
Bạn là biên kịch video YouTube tiếng Việt chuyên về AI cho người mới.
Chủ đề video: [ĐIỀN CHỦ ĐỀ]
Đối tượng: nhân viên văn phòng/sinh viên VN, chưa rành AI
Viết kịch bản 6-8 phút theo cấu trúc: Hook (10s) → Xác nhận vấn đề (15s) →
Preview lộ trình (15s) → 3 bước hướng dẫn chính (demo màn hình) →
Kết quả/case study → CTA. Giọng văn gần gũi, câu ngắn, không thuật ngữ khó.
Sau kịch bản, tự tách thêm "Lời thoại thuần" và "Bảng cảnh AI" theo đúng
định dạng đã dùng ở các video trước trong ../scripts/.
```
