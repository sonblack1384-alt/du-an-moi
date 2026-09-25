# du-an-moi — Hệ thống xây kênh YouTube (khung sườn dùng chung, sản xuất zero-filming)

> **Bắt đầu từ đây:** đọc [`WORKLOG.md`](./WORKLOG.md) để biết trạng thái hiện tại và việc cần làm tiếp — đặc biệt nếu bạn đang mở repo này từ một phiên/tài khoản Claude khác. [`CLAUDE.md`](./CLAUDE.md) giải thích cách Claude nên vận hành trong repo này.

## Cấu trúc
- [`framework/`](./framework) — khung sườn dùng chung (8 file chiến lược có placeholder) để tạo bất kỳ kênh YouTube nào, không giới hạn chủ đề. Xem [`framework/README.md`](./framework/README.md) để biết cách nhân bản thành kênh mới.
- [`channels/ai-de-dung/`](./channels/ai-de-dung) — **kênh demo đầu tiên**, dùng khung sườn trên: "AI Dễ Dùng" (hướng dẫn ứng dụng AI vào công việc/kiếm tiền cho người Việt). Gồm:
  - `strategy/` — 8 file chiến lược đã điền đầy đủ
  - `backlog.md` — 100 ý tưởng video, theo dõi trạng thái
  - `content-calendar.md` — lịch đăng 4 tuần đầu
  - `scripts/` — kịch bản đầy đủ từng video (mỗi video có sẵn "Lời thoại thuần" + "Bảng cảnh AI" để chạy qua pipeline)
  - `assets/` — sinh ra khi chạy pipeline: giọng đọc, cảnh AI-video, ảnh chụp màn hình, video nháp
- [`pipeline/`](./pipeline) — **script tự động hoá sản xuất**, gọi Google Gemini API (Veo tạo video + Gemini TTS tạo giọng đọc) để ráp video nháp gần như không cần thao tác tay, ngoài việc chụp vài tấm ảnh màn hình thao tác thật. Xem [`pipeline/README.md`](./pipeline/README.md) để cài đặt và chạy — **cần bạn tự thêm `GEMINI_API_KEY` vào environment secrets trước** (không dán vào chat), và có tốn phí thật theo tài khoản Google AI của bạn.

Khi có kênh mới (chủ đề khác), thêm thư mục `channels/<tên-kênh>/` theo đúng cấu trúc trên — `pipeline/` dùng chung, không cần sửa gì.
