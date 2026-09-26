# 8. Nhận diện thương hiệu — chống "kênh rác", chống loãng

> **Nguyên tắc gốc:** dùng AI để sản xuất không phải là rủi ro — rủi ro là không có gì lặp lại giữa các video khiến kênh trông như một đống clip AI rời rạc, không phải "một kênh". Cách chống lại: chọn vài yếu tố cố định, lặp lại y hệt ở MỌI video, không đổi theo thời gian trừ khi chủ động rebrand.

## 1. Bảng màu cố định
{{Chọn 1 màu nền + 1 màu accent duy nhất, dùng cho MỌI thumbnail/text overlay/end-card/dashboard của kênh này. Không thêm màu accent thứ 2 cho các yếu tố nhận diện.}}

## 2. Font cố định
{{1 font cho tiêu đề/thumbnail/text overlay lớn — ưu tiên font hỗ trợ tốt ngôn ngữ chính của kênh.}}

## 3. Watermark / bug góc màn hình
{{1 chữ/logo nhỏ góc màn hình, xuất hiện xuyên suốt mọi video, làm 1 lần trong tool dựng, lưu template để tái sử dụng.}}

## 4. Bumper mở/kết cố định — BẮT BUỘC, làm 1 lần dùng cho mọi video
Thay vì để AI tạo cảnh mở đầu/kết thúc khác nhau cho từng video, tạo **đúng 1 bumper mở + 1 bumper kết**, dùng lại y hệt cho mọi video của kênh. Lợi ích kép: người xem nhận diện kênh ngay trong 2 giây đầu, và tiết kiệm số lượt gọi AI-video (chỉ tạo 1 lần thay vì mỗi video 1 lần).

Cách rẻ nhất: dựng bằng `pipeline/generate_motion_graphic.py` (miễn phí, không giới hạn, đúng màu/font thương hiệu đã chọn ở trên) — chỉ cần soạn 1 câu mô tả ngắn cho mỗi bumper (ví dụ tên kênh + khẩu hiệu cho bumper mở, lời cảm ơn + CTA cho bumper kết), lưu vào `channels/<kênh>/assets/_brand/intro-bumper.mp4` và `outro-bumper.mp4`. Chỉ cân nhắc AI-video trả phí (Veo...) nếu muốn hình ảnh photorealistic thay vì card chữ/icon.

{{Nếu chọn hướng AI-video trả phí, viết sẵn 2 prompt cụ thể cho bumper mở/kết ở đây, theo đúng bảng màu + font đã chọn ở trên.}}

**Cấu trúc mọi video:** Bumper mở (cố định) → Hook riêng của video (đặc thù nội dung) → nội dung → CTA → Bumper kết (cố định).

## 5. Câu khẩu hiệu đọc trong video (spoken tagline)
{{1 câu giới thiệu kênh cố định chèn sau phần "xác nhận vấn đề + preview", và 1 câu kết cố định chèn sau CTA — dùng y hệt ở mọi video. Nếu kênh đã có sẵn video/giọng đọc trước khi viết brand guide này, GỘP việc thêm câu khẩu hiệu vào lần tạo lại giọng đọc kế tiếp (khi cần đổi giọng/model vì lý do khác) thay vì tạo lại riêng — tránh tốn quota/phí 2 lần cho cùng 1 mục đích.}}

## 6. Hệ thống đặt tên riêng cho các "framework" tự nghĩ ra
Khi kênh tự đúc kết ra 1 công thức/khung làm việc riêng (không phải liệt kê chung chung từ AI), luôn đặt tên viết tắt riêng và nhắc lại xuyên suốt các video liên quan — biến nó thành tài sản thương hiệu thay vì kiến thức trôi nổi.

{{Liệt kê các framework/công thức riêng đã tạo ra, video nào giới thiệu, và cách các video khác nên nhắc lại.}}

## 7. Nguyên tắc "không đổi"
Trước khi đổi giọng đọc, màu, font, hoặc bumper đã chốt — tự hỏi: "đổi có phải vì mục tiêu thương hiệu lâu dài không, hay chỉ vì tiện đúc trong lúc sản xuất?". Chỉ đổi khi có lý do chiến lược rõ ràng, ghi lại lý do vào `WORKLOG.md`, và đổi đồng loạt cho toàn bộ video hiện có — không để tồn tại 2 phiên bản nhận diện cùng lúc.
