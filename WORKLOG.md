# Nhật ký làm việc & trạng thái dự án

> **Đọc file này đầu tiên** khi mở repo ở bất kỳ phiên Claude/tài khoản nào khác. Mục "TRẠNG THÁI HIỆN TẠI" luôn được cập nhật ở đầu file — phần log bên dưới chỉ để tra cứu lịch sử.

---

## TRẠNG THÁI HIỆN TẠI
*(cập nhật lần cuối: mốc #2 — 2026-09-25)*

### Đã có
- **Khung sườn dùng chung** (`framework/`) — 8 file template + hướng dẫn tạo kênh mới. Hoàn chỉnh, có thể dùng ngay cho kênh thứ 2.
- **Kênh demo "AI Dễ Dùng"** (`channels/ai-de-dung/`) — niche: ứng dụng AI vào công việc/kiếm tiền cho người Việt. Đã có:
  - 8 file chiến lược đầy đủ (`strategy/`)
  - Backlog 100 ý tưởng video, có trạng thái theo dõi (`backlog.md`)
  - Lịch đăng 4 tuần đầu (`content-calendar.md`)
  - **4 kịch bản đầy đủ sẵn sàng quay**: video #1-4 trong `scripts/` (xem `backlog.md` để biết chi tiết)

### Đang thiếu / chưa làm
- Video #5-8 trong lịch 4 tuần đầu (backlog #5-8) **chưa có kịch bản chi tiết** — mới có tên ý tưởng.
- Chưa quay/dựng/đăng video nào thật (Claude không thể tự làm phần này — xem mục "Giới hạn" trong `CLAUDE.md`).
- Chưa kiểm tra tên/handle "AI Dễ Dùng" có bị trùng trên YouTube ngoài đời chưa.
- Chưa có kênh thứ 2 (chủ đề khác) — khung sườn đã sẵn sàng để nhân bản khi có quyết định về chủ đề mới.

### Câu hỏi đang chờ người dùng quyết định
*(không có câu nào đang chặn tiến độ tại thời điểm này — Claude sẽ tự làm tiếp phần kịch bản #5-8 và chỉ dừng lại hỏi khi tới các mốc thật sự cần người quyết, ví dụ: chủ đề kênh thứ 2, hoặc khi cần xác nhận tên/handle chính thức trước khi đăng ký tài khoản YouTube thật.)*

### Việc tiếp theo nên làm (theo thứ tự ưu tiên)
1. Viết tiếp kịch bản đầy đủ cho video #5-8 (đang trong lịch 4 tuần đầu).
2. Sau khi có ≥8 kịch bản, người dùng tự quay/dựng/đăng theo `strategy/05-quy-trinh-lam-video-nhanh.md` (phần Claude không tự làm được).
3. Sau tuần 1-3 đăng thật, đối chiếu số liệu theo `strategy/07-doc-so-lieu.md`, cập nhật lại lịch tuần 5+.
4. Khi người dùng sẵn sàng mở kênh thứ 2: hỏi chủ đề mong muốn (hoặc để Claude tự đề xuất như lần này), rồi nhân bản từ `framework/template/`.

---

## LOG CHI TIẾT (mới nhất ở trên)

### Mốc #2 — 2026-09-25 — Biến thành khung sườn dùng chung + hệ thống lịch sử làm việc
**Người dùng yêu cầu:** làm kênh "AI Dễ Dùng" thành bản demo cho khung sườn dùng chung để mở rộng nhiều kênh khác chủ đề sau này; tự động hoá mọi thứ có thể; chỉ hỏi ở mốc quan trọng; lưu lịch sử làm việc trong repo để mở lại từ tài khoản Claude khác vẫn tiếp tục được.

**Đã làm:**
- Tái cấu trúc repo: `strategy/` cũ → `channels/ai-de-dung/strategy/`.
- Tạo `framework/` — 8 file template có placeholder `{{...}}` + `framework/README.md` hướng dẫn nhân bản kênh mới.
- Tạo `CLAUDE.md` (tự động load cho mọi phiên Claude Code mở repo) — trỏ về file này, giải thích cấu trúc repo và giới hạn thật (không tự quay/dựng/đăng video được).
- Tạo `WORKLOG.md` (file này) làm nguồn trạng thái duy nhất, thiết kế để phiên/tài khoản Claude khác đọc và chạy tiếp được ngay.
- Tạo `channels/ai-de-dung/backlog.md` — chuyển 100 ý tưởng từ dạng danh sách sang bảng có cột trạng thái.
- Tạo `channels/ai-de-dung/content-calendar.md` — lịch đăng cụ thể 4 tuần đầu.
- Tự động viết thêm 3 kịch bản đầy đủ (video #2, #3, #4) trong `channels/ai-de-dung/scripts/`, nâng tổng số kịch bản sẵn sàng quay lên 4.

**Quyết định tự đưa ra (trong phạm vi "auto mọi thứ"):**
- Cấu trúc thư mục `framework/` + `channels/<slug>/` (hợp lý, dễ mở rộng, không cần hỏi vì có thể sửa lại dễ dàng).
- Thứ tự ưu tiên video #5-8 trong lịch 4 tuần lấy trực tiếp từ Tier 1 của backlog.

**Chưa làm/để lại cho vòng sau:** kịch bản #5-8, và bất kỳ hành động cần thao tác ngoài đời thật (quay/đăng).

---

### Mốc #1 — 2026-09-25 — Tạo bộ chiến lược 7 bước ban đầu
**Người dùng yêu cầu:** chạy tuần tự 7 prompt chiến lược YouTube (ảnh đính kèm) cho dự án `du-an-moi` (lúc đó đang trống).

**Quyết định cần hỏi → đã hỏi người dùng:** niche, định dạng, nguồn lực, mục tiêu. Người dùng trả lời: để Claude tự chọn niche đúng chuyên môn, định dạng để Claude tư vấn, nguồn lực solo/ngân sách thấp, mục tiêu để Claude tư vấn.

**Đã làm:**
- Chọn niche: "Ứng dụng AI vào công việc/kiếm tiền cho người Việt", định dạng faceless (screen recording + giọng đọc), tên kênh "AI Dễ Dùng".
- Viết đủ 7 file chiến lược (`strategy/00` đến `strategy/07` — sau này chuyển vào `channels/ai-de-dung/strategy/` ở Mốc #2), gồm cả 100 ý tưởng video và 1 kịch bản mẫu đầy đủ (video #1).
- Commit & push lên `claude/tender-meitner-0s76lt`.
