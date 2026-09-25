# 5. Quy trình sản xuất video nhanh gấp 3 (có AI hỗ trợ)

## Mục tiêu
Rút quy trình từ ý tưởng → video đăng từ ~8 giờ xuống còn ~2.5-3 giờ/video long-form bằng cách dùng AI ở từng bước, phù hợp làm solo.

## Quy trình 8 bước

### 1. Nghiên cứu chủ đề (15 phút)
- Lấy từ danh sách 100 ý tưởng (`02-chon-niche.md`) hoặc backlog cập nhật hàng tuần.
- Dùng AI (Claude/ChatGPT) tra nhanh: điểm chính cần nói, sai lầm phổ biến người mới hay gặp, số liệu/ví dụ minh hoạ.
- Công cụ: Claude/ChatGPT, YouTube search suggest (kiểm tra từ khoá thật).

### 2. Viết kịch bản (20-30 phút)
- Dùng khung kịch bản chuẩn ở `03-kich-ban-hook-thumbnail.md`, để AI viết bản nháp theo khung, sau đó **biên tập lại bằng giọng văn cá nhân** (bắt buộc — tránh nội dung 100% AI không chỉnh sửa).
- Công cụ: Claude/ChatGPT với prompt template cố định (lưu sẵn trong `templates/prompt-viet-kich-ban.md`).

### 3. Lồng tiếng (15-20 phút)
- Ưu tiên tự thu âm bằng mic giá rẻ (chân thực, giọng thật tăng độ tin cậy).
- Nếu cần giọng phụ/đa dạng: dùng TTS tiếng Việt (ví dụ FPT.AI TTS, Google TTS) cho các đoạn phụ.

### 4. Quay màn hình/tư liệu (30-45 phút)
- Ghi lại đúng các bước sẽ hướng dẫn trước, không quay "diễn" trực tiếp để tránh phải quay lại nhiều lần.
- Công cụ: OBS Studio (miễn phí) cho screen recording.

### 5. Dựng video (45-60 phút)
- Dùng template dựng sẵn (intro, lower-third, outro) để không phải làm lại từ đầu mỗi lần.
- Cắt khoảng lặng tự động, thêm text overlay + pattern interrupt theo checklist QC bên dưới.
- Công cụ: CapCut (miễn phí, có auto-caption tiếng Việt) hoặc DaVinci Resolve nếu cần nâng cao.

### 6. Tạo thumbnail (10-15 phút)
- Dùng template Canva đã build sẵn (đổi ảnh/chữ, giữ bố cục nhất quán để tạo nhận diện kênh).
- Test nhanh bằng cách thu nhỏ ảnh xem còn rõ chữ không (giả lập hiển thị trên điện thoại).

### 7. Đăng tải & tối ưu SEO (10 phút)
- Điền tiêu đề/mô tả/tag theo từ khoá đã nghiên cứu ở bước 1.
- Thêm chapters, pinned comment dẫn playlist, end screen.

### 8. Xem lại số liệu & tái sử dụng nội dung (15 phút, làm sau 48h)
- Xem retention graph để rút kinh nghiệm cho video sau.
- Cắt 2-4 đoạn hay nhất thành Shorts/TikTok/Reels (đổi tỉ lệ khung hình 9:16, thêm caption lớn, hook riêng trong 1-2s đầu).

## Checklist kiểm soát chất lượng (QC) trước khi đăng
- [ ] Hook rõ ràng trong 3 giây đầu, không lan man
- [ ] Không có khoảng lặng > 1.5 giây chưa được cắt
- [ ] Text overlay không lỗi chính tả
- [ ] Âm lượng giọng đọc đồng đều, không rè
- [ ] Thumbnail rõ chữ khi thu nhỏ bằng kích thước điện thoại
- [ ] Tiêu đề khớp 100% nội dung (không giật tít sai)
- [ ] Có chapters/timestamps
- [ ] Có CTA + end screen dẫn đúng 1 video liên quan
- [ ] Đã thêm vào đúng playlist trụ cột nội dung

## Công cụ đề xuất (miễn phí/giá rẻ, phù hợp ngân sách thấp)
| Việc | Công cụ |
|---|---|
| Viết/nghiên cứu kịch bản | Claude, ChatGPT |
| Ghi màn hình | OBS Studio |
| Dựng video | CapCut |
| Thumbnail | Canva |
| TTS tiếng Việt | FPT.AI TTS / Google TTS |
| Quản lý lịch đăng | Google Sheets/Notion (lịch nội dung) |

## Mẫu prompt viết kịch bản (lưu để tái sử dụng)
```
Bạn là biên kịch video YouTube tiếng Việt chuyên về AI cho người mới.
Chủ đề video: [ĐIỀN CHỦ ĐỀ]
Đối tượng: nhân viên văn phòng/sinh viên VN, chưa rành AI
Viết kịch bản 6-8 phút theo cấu trúc: Hook (10s) → Xác nhận vấn đề (15s) →
Preview lộ trình (15s) → 3 bước hướng dẫn chính (demo màn hình) →
Kết quả/case study → CTA. Giọng văn gần gũi, câu ngắn, không thuật ngữ khó.
```
