# du-an-moi — Hệ thống xây kênh YouTube (khung sườn dùng chung)

> **Bắt đầu từ đây:** đọc [`WORKLOG.md`](./WORKLOG.md) để biết trạng thái hiện tại và việc cần làm tiếp — đặc biệt nếu bạn đang mở repo này từ một phiên/tài khoản Claude khác. [`CLAUDE.md`](./CLAUDE.md) giải thích cách Claude nên vận hành trong repo này.

## Cấu trúc
- [`framework/`](./framework) — khung sườn dùng chung (8 file chiến lược có placeholder) để tạo bất kỳ kênh YouTube nào, không giới hạn chủ đề. Xem [`framework/README.md`](./framework/README.md) để biết cách nhân bản thành kênh mới.
- [`channels/ai-de-dung/`](./channels/ai-de-dung) — **kênh demo đầu tiên**, dùng khung sườn trên: "AI Dễ Dùng" (hướng dẫn ứng dụng AI vào công việc/kiếm tiền cho người Việt). Gồm:
  - `strategy/` — 8 file chiến lược đã điền đầy đủ
  - `backlog.md` — 100 ý tưởng video, theo dõi trạng thái
  - `content-calendar.md` — lịch đăng 4 tuần đầu
  - `scripts/` — kịch bản đầy đủ từng video, sẵn sàng quay

Khi có kênh mới (chủ đề khác), thêm thư mục `channels/<tên-kênh>/` theo đúng cấu trúc trên.
