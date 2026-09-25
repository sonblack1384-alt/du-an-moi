# Hướng dẫn cho Claude khi làm việc trong repo này

**Việc đầu tiên khi mở repo này ở bất kỳ phiên/tài khoản nào: đọc `WORKLOG.md` ở gốc repo trước tiên.** File đó là nguồn sự thật duy nhất về trạng thái hiện tại, việc đang làm dở, và câu hỏi nào đang chờ người dùng quyết định — vì phiên chat (context) không lưu qua các tài khoản Claude khác nhau, chỉ có nội dung trong repo mới lưu được.

## Repo này là gì
Hệ thống xây kênh YouTube dùng **một khung sườn chung** (`framework/`) áp dụng cho nhiều kênh khác nhau (`channels/<tên-kênh>/`), mỗi kênh có thể khác chủ đề hoàn toàn nhưng dùng chung cấu trúc 8 file chiến lược + backlog + content calendar + scripts.

```
framework/
  README.md            <- cách tạo kênh mới từ khung
  template/*.md         <- 8 file khung có placeholder {{...}}
channels/
  ai-de-dung/            <- kênh demo đầu tiên (đã điền đầy đủ, dùng làm ví dụ mẫu)
    strategy/*.md        <- 8 file chiến lược đã điền
    backlog.md            <- theo dõi trạng thái từng ý tưởng video
    content-calendar.md   <- lịch đăng cụ thể
    scripts/*.md           <- kịch bản đầy đủ từng video
  <kênh mới sau này>/     <- lặp lại cấu trúc trên
WORKLOG.md              <- ĐỌC FILE NÀY TRƯỚC — trạng thái & lịch sử làm việc
```

## Cách vận hành mong muốn (người dùng đã yêu cầu rõ)
- **Tự động hoá tối đa**: tự nghiên cứu, tự viết chiến lược/kịch bản/kế hoạch, tự cập nhật backlog & lịch đăng — không hỏi người dùng những việc có thể tự quyết định hợp lý được.
- **Chỉ hỏi ở các mốc quan trọng thật sự cần người quyết**, ví dụ: chọn chủ đề/tên cho một kênh hoàn toàn mới, quyết định ngân sách/chi tiêu thật, các hành động không thể tự động hoá được (quay video thật, đăng lên YouTube thật, kết nối tài khoản AdSense thật) — những việc ngoài khả năng của Claude trong môi trường này.
- **Luôn cập nhật `WORKLOG.md` sau mỗi mốc quan trọng** (hoàn thành 1 kênh, hoàn thành 1 giai đoạn, có quyết định mới từ người dùng, có câu hỏi đang chờ) rồi `git commit` + `git push` ngay — vì đây là cách duy nhất một phiên Claude khác (tài khoản khác) tiếp tục được công việc.

## Giới hạn thật cần nói rõ với người dùng (không tự nhận là đã làm được)
Claude trong môi trường này **không thể**: quay/dựng video thật, ghi âm giọng đọc thật, đăng nhập YouTube Studio, tạo tài khoản AdSense, hay xác nhận tên kênh/handle chưa bị trùng ngoài đời (trừ khi có công cụ tìm kiếm web được dùng để kiểm tra). Mọi output ở đây là **tài liệu kế hoạch, kịch bản văn bản, checklist** — phần thực thi vật lý (quay/dựng/đăng) vẫn cần người dùng hoặc công cụ khác thực hiện.
