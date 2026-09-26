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
    strategy/*.md        <- 8 file chiến lược đã điền (05 = quy trình sản xuất zero-filming)
    backlog.md            <- theo dõi trạng thái từng ý tưởng video
    content-calendar.md   <- lịch đăng cụ thể
    scripts/*.md           <- kịch bản đầy đủ từng video, mỗi file có thêm mục
                              "Lời thoại thuần" (dán vào TTS) và "Bảng cảnh AI"
                              (mặc định 2026-09-26: TOÀN BỘ cảnh = AI text-to-video
                              dựng bằng generate_motion_graphic.py -- KHÔNG còn
                              yêu cầu người dùng chụp ảnh màn hình thật, xem mục
                              "Giới hạn thật" bên dưới)
    assets/                <- sinh ra khi chạy pipeline/ (voice.wav, scenes/, draft.mp4)
  <kênh mới sau này>/     <- lặp lại cấu trúc trên
pipeline/                <- script Python gọi Gemini API (Veo + TTS) để tự động ráp
                             video nháp từ kịch bản — dùng chung cho mọi kênh, xem
                             pipeline/README.md trước khi chạy (cần GEMINI_API_KEY,
                             tốn phí thật, code viết theo API tại thời điểm viết nên
                             cần dry-run/chạy thử 1 cảnh trước khi chạy hàng loạt)
WORKLOG.md              <- ĐỌC FILE NÀY TRƯỚC — trạng thái & lịch sử làm việc
```

## Cách vận hành mong muốn (người dùng đã yêu cầu rõ)
- **Tự động hoá tối đa**: tự nghiên cứu, tự viết chiến lược/kịch bản/kế hoạch, tự cập nhật backlog & lịch đăng — không hỏi người dùng những việc có thể tự quyết định hợp lý được.
- **Chỉ hỏi ở các mốc quan trọng thật sự cần người quyết**, ví dụ: chọn chủ đề/tên cho một kênh hoàn toàn mới, quyết định ngân sách/chi tiêu thật, các hành động không thể tự động hoá được (quay video thật, đăng lên YouTube thật, kết nối tài khoản AdSense thật) — những việc ngoài khả năng của Claude trong môi trường này.
- **Luôn cập nhật `WORKLOG.md` sau mỗi mốc quan trọng** (hoàn thành 1 kênh, hoàn thành 1 giai đoạn, có quyết định mới từ người dùng, có câu hỏi đang chờ) rồi `git commit` + `git push` ngay — vì đây là cách duy nhất một phiên Claude khác (tài khoản khác) tiếp tục được công việc.

## Giới hạn thật cần nói rõ với người dùng (không tự nhận là đã làm được)
Từ khi có `pipeline/` (Gemini TTS + `generate_motion_graphic.py`), Claude **tự ráp được video nháp hoàn chỉnh KHÔNG CẦN người dùng thao tác gì** (giọng đọc thật + đồ hoạ chữ/icon thật + bumper + ffmpeg, miễn phí, không giới hạn) — đã kiểm chứng bằng test kỹ thuật (xem `pipeline/README.md`). **Quyết định 2026-09-26 (yêu cầu rõ ràng của người dùng): bỏ hẳn yêu cầu chụp ảnh màn hình thật** — trước đó pipeline vẫn cần người dùng tự chụp vài ảnh cho cảnh demo phần mềm, người dùng phản đối việc này ("đã tự động hoá mà còn chụp gửi"), nên đã chuyển 100% cảnh sang đồ hoạ AI tự dựng, đánh đổi mất phần "xem tận mắt thao tác trên giao diện thật". Đừng tự ý đề xuất quay lại yêu cầu chụp ảnh trừ khi người dùng chủ động hỏi lại.

Giới hạn thật còn lại:
- Cần `GEMINI_API_KEY` do người dùng tự thêm vào environment secrets (Claude không có sẵn, không được yêu cầu người dùng dán key vào chat).
- TTS có quota miễn phí giới hạn thật theo ngày (10 lượt/model/ngày) — không phải lỗi, cần đợi quota reset khi hết.
- Nếu sau này người dùng MUỐN Veo (ảnh AI photorealistic, trả phí) hoặc muốn nâng cấp lại một số cảnh bằng ảnh chụp màn hình thật, cả 2 vẫn hỗ trợ được (xem `pipeline/README.md`) — nhưng đây là lựa chọn thêm, không phải mặc định, không tự ý bật lại.
- Claude **không thể**: đăng nhập YouTube Studio, tạo tài khoản AdSense thật, hay xác nhận tên kênh/handle chưa bị trùng ngoài đời (trừ khi dùng công cụ tìm kiếm web để kiểm tra). Khâu đăng tải/quản lý kênh thật vẫn cần người dùng thực hiện.
- Code gọi API (tên model TTS/Veo, cách gọi SDK) viết theo tài liệu Gemini API tại thời điểm viết — API có thể đổi theo thời gian, nên luôn `--dry-run`/chạy thử 1 cảnh trước khi chạy hàng loạt (xem `pipeline/README.md`).
