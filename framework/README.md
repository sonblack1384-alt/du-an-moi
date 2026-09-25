# Khung sườn xây kênh YouTube (dùng chung cho nhiều kênh)

Đây là bộ khung 7 bước (+ 1 file tổng quan) dùng để lập chiến lược cho **bất kỳ kênh YouTube nào**, bất kể chủ đề. Kênh demo đầu tiên dùng khung này là [`channels/ai-de-dung/`](../channels/ai-de-dung) — mở file đó ra để xem một bộ đã điền đầy đủ làm ví dụ mẫu.

## Cấu trúc khung (`template/`)
| File | Nội dung |
|---|---|
| `00-tong-quan-kenh.md` | Niche, định dạng, đối tượng, USP, lý do an toàn với nguyên tắc cộng đồng |
| `01-ke-hoach-tron-goi.md` | Định vị kênh, trụ cột nội dung, lịch đăng, hệ thống tăng trưởng, lịch thực thi tuần |
| `02-chon-niche.md` | Nghiên cứu nhu cầu/cạnh tranh/SEO + 100 ý tưởng video đầu tiên |
| `03-kich-ban-hook-thumbnail.md` | Công thức hook/tiêu đề/thumbnail + cấu trúc kịch bản chuẩn |
| `04-thuat-toan-tang-truong.md` | Giải thích chỉ số & chiến lược tăng trưởng thuật toán |
| `05-quy-trinh-lam-video-nhanh.md` | Quy trình sản xuất 8 bước + checklist QC + công cụ |
| `06-ke-hoach-kiem-tien.md` | Lộ trình kiếm tiền theo 3 giai đoạn tăng trưởng |
| `07-doc-so-lieu.md` | Khung đánh giá số liệu hàng tuần/tháng |

Mỗi kênh mới còn có thêm (không nằm trong `template/`, tự tạo theo mẫu ở kênh demo):
- `backlog.md` — bảng theo dõi trạng thái từng ý tưởng video (chưa làm/đang làm/đã đăng)
- `content-calendar.md` — lịch đăng cụ thể theo tuần
- `scripts/` — kịch bản đầy đủ từng video, đặt tên `NN-slug.md`

## Cách tạo kênh mới từ khung này
1. Tạo thư mục `channels/<ten-kenh-slug>/`.
2. Copy toàn bộ `framework/template/*.md` vào `channels/<ten-kenh-slug>/strategy/`.
3. Điền các placeholder `{{...}}` trong từng file — **chỉ cần quyết định 5 thứ gốc** ở bước 1 (xem `template/00-tong-quan-kenh.md`), các file còn lại suy ra logic từ đó (có thể tự động hoá bằng AI dựa trên 5 quyết định gốc, không cần hỏi lại từng chi tiết nhỏ).
4. Tạo `backlog.md`, `content-calendar.md`, `scripts/` theo đúng mẫu đã làm ở `channels/ai-de-dung/`.
5. Ghi 1 mục mới vào `WORKLOG.md` ở gốc repo (mục "Kênh mới: <tên>") để mọi phiên Claude sau đều biết kênh này đã tồn tại và đang ở giai đoạn nào.

## Nguyên tắc chung áp dụng cho mọi kênh
- Không nội dung y tế/tài chính đưa lời khuyên đầu tư trực tiếp (nhóm YMYL rủi ro cao) trừ khi có kiểm duyệt chuyên môn rõ ràng.
- Không giật tít sai nội dung thật, không nhạc/hình ảnh vi phạm bản quyền.
- Luôn qua biên tập thủ công trước khi đăng, không đăng nguyên văn bản AI-generated 100%.
- Tiết lộ rõ nội dung tài trợ/affiliate.
