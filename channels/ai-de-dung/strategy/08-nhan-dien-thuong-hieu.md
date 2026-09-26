# 8. Nhận diện thương hiệu — chống "kênh rác", chống loãng

> **Nguyên tắc gốc:** dùng AI để sản xuất không phải là rủi ro — rủi ro là không có gì lặp lại giữa các video khiến kênh trông như một đống clip AI rời rạc, không phải "một kênh". Cách chống lại: chọn vài yếu tố cố định, lặp lại y hệt ở MỌI video, không đổi theo thời gian trừ khi chủ động rebrand.

## 1. Bảng màu cố định (dùng cho MỌI thumbnail, text overlay, end-card)
Kế thừa đúng bảng màu đã dùng ở `dashboard.html` để đồng bộ toàn bộ hệ sinh thái kênh (dashboard + video):
- **Nền tối:** `#14171C`
- **Accent chính (điểm nhấn, CTA, chữ nổi bật):** `#E8A33D` (amber)
- **Chữ chính:** `#EDEFF2`
- **Chữ phụ/mờ:** `#8A93A1`
- Không dùng thêm màu accent nào khác ngoài amber cho các yếu tố nhận diện (tiêu đề kênh, khung viền, nút CTA). Màu minh hoạ nội dung bên trong video có thể đa dạng, nhưng khung/viền/watermark luôn amber-trên-nền-tối.

## 2. Font cố định
- **Tiêu đề/thumbnail/text overlay lớn:** 1 font duy nhất — chọn **"Be Vietnam Pro" (Bold)** (hỗ trợ tiếng Việt đầy đủ dấu, đậm, dễ đọc trên thumbnail nhỏ).
- **Phụ đề/caption:** font mặc định của CapCut/tool auto-caption là đủ, không cần cố định (khó kiểm soát), nhưng giữ màu chữ trắng + viền đen để đồng nhất phong cách phụ đề.

## 3. Watermark / bug góc màn hình
Toàn bộ video có 1 chữ nhỏ góc dưới bên phải: **"AI DỄ DÙNG"**, font Be Vietnam Pro, màu amber, mờ 60-70% opacity, xuất hiện từ giây đầu tới giây cuối. Làm 1 lần trong CapCut/Canva dưới dạng overlay có thể lưu template, áp lại cho mọi video — không tốn thêm chi phí AI.

## 4. Bumper mở đầu & kết thúc CỐ ĐỊNH (thay vì mỗi video 1 cảnh AI-video riêng)
Đây là thay đổi quan trọng nhất để chống loãng: **thay vì để Veo tạo cảnh mở đầu/kết thúc khác nhau cho từng video** (như đang làm ở "Bảng cảnh AI" hiện tại), tạo **đúng 1 bumper mở + 1 bumper kết**, dùng lại y hệt cho cả 16 video (và mọi video sau này). Lợi ích kép: (a) người xem thấy đúng 2-3 giây quen mặt là biết ngay đang xem kênh nào, (b) tiết kiệm ~32 lượt gọi Veo (2 cảnh × 16 video) vì chỉ cần tạo 1 lần.

**Prompt Veo cho bumper mở (1.5-2 giây, tạo 1 lần, lưu vào `channels/ai-de-dung/assets/_brand/intro-bumper.mp4`):**
```
Minimal flat motion graphic, dark navy background (#14171C), the text
"AI DỄ DÙNG" appearing letter by letter in bold amber (#E8A33D) sans-serif
font at center, subtle glow pulse, clean tech aesthetic, no camera shake, 2 seconds
```

**Prompt Veo cho bumper kết (2 giây, tạo 1 lần, lưu vào `channels/ai-de-dung/assets/_brand/outro-bumper.mp4`):**
```
Minimal flat motion graphic, same dark navy background (#14171C), amber
(#E8A33D) subscribe bell icon pulsing gently, text "AI DỄ DÙNG" fading in
below it, clean tech aesthetic, calm and simple, 2 seconds
```

**Cách áp dụng vào quy trình sản xuất (`05-quy-trinh-lam-video-nhanh.md`):** khi ráp video (CapCut hoặc `pipeline/assemble.py`), luôn ghép `intro-bumper.mp4` làm cảnh đầu tiên và `outro-bumper.mp4` làm cảnh cuối cùng của MỌI video — trước cảnh hook riêng của từng video, không thay thế hook (hook riêng vẫn cần để giữ chân người xem theo nội dung cụ thể). Tức là: **Bumper mở (2s, cố định) → Hook riêng của video (đặc thù nội dung) → ... → CTA → Bumper kết (2s, cố định)**.

## 5. Câu khẩu hiệu đọc trong video (spoken tagline) — ÁP DỤNG Ở ĐỢT TẠO LẠI GIỌNG ĐỌC SẮP TỚI
Để tránh tạo lại giọng đọc 2 lần liên tiếp (đang chờ người dùng chọn giọng nam), câu khẩu hiệu dưới đây **chưa được thêm vào 16 file kịch bản hiện tại** — sẽ gộp chung vào lần tạo lại giọng đọc kế tiếp (khi đổi sang giọng nam đã chọn). Ghi lại đây để không quên:

- **Câu giới thiệu kênh** (chèn ngay sau đoạn "xác nhận vấn đề + preview", trước khi vào nội dung chính, ở MỌI video):
  > "Đây là AI Dễ Dùng — kênh giúp bạn dùng AI thật đơn giản, không cần biết code, không lý thuyết dài dòng."
- **Câu kết cố định** (chèn ngay sau CTA, trước khi hết video, ở MỌI video):
  > "AI Dễ Dùng — dễ thật mà. Hẹn gặp lại ở video sau!"

## 6. Hệ thống đặt tên riêng cho các "framework" tự nghĩ ra
Khi kênh tự đúc kết ra 1 công thức/khung làm việc riêng (không phải liệt kê chung chung từ AI), luôn đặt tên viết tắt tiếng Việt riêng và nhắc lại xuyên suốt các video liên quan — biến nó thành tài sản thương hiệu thay vì kiến thức trôi nổi. Đã có sẵn 1 cái:
- **Công thức VBYĐ** (Vai trò – Bối cảnh – Yêu cầu – Định dạng), giới thiệu ở video #4 (`04-cach-viet-prompt-hieu-qua.md`) — mọi video sau này có nhắc tới việc viết prompt nên gọi lại đúng tên "công thức VBYĐ" thay vì giải thích lại từ đầu, và dẫn link/gợi ý xem lại video #4.
- Khuyến khích tạo thêm các công thức tương tự cho các nhóm nội dung khác (ví dụ 1 khung đánh giá công cụ AI riêng dùng cho mọi video "so sánh & đánh giá") khi viết kịch bản mới — xem `02-chon-niche.md` phần nhóm nội dung.

## 7. Nguyên tắc "không đổi" (checklist trước khi đổi bất kỳ yếu tố nhận diện nào)
Trước khi đổi giọng đọc, màu, font, hoặc bumper đã chốt — tự hỏi: "đổi có phải vì mục tiêu thương hiệu lâu dài không, hay chỉ vì tiện đúc trong lúc sản xuất?". Chỉ đổi khi có lý do chiến lược rõ ràng (ví dụ: nghiên cứu cho thấy giọng hiện tại không hợp đối tượng), ghi lại lý do đổi vào `WORKLOG.md`, và đổi đồng loạt cho toàn bộ video hiện có — không để tồn tại 2 phiên bản nhận diện cùng lúc.
