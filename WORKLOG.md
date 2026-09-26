# Nhật ký làm việc & trạng thái dự án

> **Đọc file này đầu tiên** khi mở repo ở bất kỳ phiên Claude/tài khoản nào khác. Mục "TRẠNG THÁI HIỆN TẠI" luôn được cập nhật ở đầu file — phần log bên dưới chỉ để tra cứu lịch sử.

---

## TRẠNG THÁI HIỆN TẠI
*(cập nhật lần cuối: mốc #9 — 2026-09-26)*

### 🎙️ 16/16 giọng đọc thật ĐÃ XONG — hoàn toàn miễn phí, không cần billing
Sau khi video #9-16 bị chặn quota ở model `gemini-3.8-flash-tts` (10 lượt/ngày), nghiên cứu theo yêu cầu người dùng ("tìm giọng miễn phí khác, test trước khi đầu tư"):
- **Đã thử các dịch vụ TTS miễn phí khác** (edge-tts/Bing, Google Translate TTS, FPT.AI, Zalo AI, VBee, Viettel AI, HuggingFace, Replicate, Play.ht, Murf, Deepgram, Azure Cognitive Services, StreamElements, VoiceRSS, Yandex) — **tất cả đều bị chặn bởi chính sách mạng của môi trường này**, chỉ domain của Google và AWS mới gọi được. `texttospeech.googleapis.com` (Google Cloud TTS, khác Gemini) gọi được nhưng gần như chắc chắn cũng cần bật billing tương tự Veo (chưa thử vì cần người dùng thêm domain này vào Allowed websites của credential trước).
- **Phát hiện quan trọng, không tốn thêm phí:** quota miễn phí của Gemini TTS tính **riêng theo từng model**, không dùng chung. `gemini-3.8-flash-tts` hết quota nhưng `gemini-3.1-flash-tts-preview` và `gemini-3.8-flash-lite-tts` vẫn còn nguyên.
- Đã sửa `generate_voice.py`: tự động thử lần lượt `TTS_MODELS = [gemini-3.8-flash-tts, gemini-3.1-flash-tts-preview, gemini-3.8-flash-lite-tts]`, dùng model đầu tiên còn quota. Thêm `--model` để ép dùng đúng 1 model.
- **Kết quả: tạo xong toàn bộ 16/16 giọng đọc thật, miễn phí 100%**, đã commit vào git (`channels/ai-de-dung/assets/*/voice.wav`).

### 🎉 Option B (pipeline tự host) ĐÃ XÁC THỰC THẬT — TTS chạy được, Veo cần bật billing
Người dùng đã thêm key qua cơ chế **"API credentials"** trong Environment settings (không phải "Environment variables" — mục đó cấm secrets). Cơ chế này khác thiết kế ban đầu: **key KHÔNG nằm trong `os.environ`**, mà hệ thống tự tiêm header xác thực vào mọi request HTTPS đi tới domain đã khai báo (`generativelanguage.googleapis.com`) ở tầng network proxy — code không bao giờ thấy giá trị key thật. Đã cập nhật `pipeline/common.py`: `get_api_key()` giờ chỉ trả về 1 chuỗi placeholder bất kỳ (SDK cần có giá trị để khởi tạo, nhưng auth thật đến từ proxy).

**Đã test thật và xác nhận:**
- `generate_voice.py` (Gemini TTS) — **THÀNH CÔNG**, đã tạo file giọng đọc thật cho video #1 (100 giây), gửi người dùng nghe. API trả về file `.wav` hoàn chỉnh (RIFF header có sẵn), không phải PCM thô như code cũ giả định — đã sửa `generate_voice.py` để ghi thẳng bytes khi phát hiện RIFF/wav, không bọc lại qua `wave` module nữa.
- `generate_scenes.py` (Veo) — **THẤT BẠI**: lỗi `429 RESOURCE_EXHAUSTED` — tài khoản Google AI của người dùng chưa bật billing/đủ quota cho Veo. Đã báo người dùng vào aistudio.google.com bật billing.
- **Tên model đã lỗi thời trong code cũ, đã sửa theo model thật list được từ API (2026-09):**
  - TTS: `gemini-2.5-flash-preview-tts` → `gemini-3.8-flash-tts`
  - Veo: `veo-3.0-generate-001` → `veo-3.1-generate-preview` (thêm `--model` flag để chọn `-fast`/`-lite` nếu cần rẻ hơn; AutoScene mặc định dùng `-lite`)
  - Model text `gemini-2.5-flash` cũng đã bị deprecate, model hiện tại là `gemini-3.8-flash` (chỉ dùng để test, không dùng trong pipeline chính).

### Đã có
- **Khung sườn dùng chung** (`framework/`) — 8 file template + hướng dẫn tạo kênh mới, mặc định zero-filming.
- **Kênh demo "AI Dễ Dùng"** (`channels/ai-de-dung/`) — 8 file chiến lược, backlog 100 ý tưởng, lịch đăng **8 tuần** (mở rộng từ 4 tuần), **16/16 kịch bản đầy đủ** (video #1-16) — mỗi kịch bản có "Lời thoại thuần" (dán thẳng vào TTS) và "Bảng cảnh AI" (từng cảnh: ảnh chụp màn hình hay prompt AI-video). Video #10 đã đổi góc tiếp cận từ "làm bài không bị phát hiện đạo văn" sang "học tập đúng cách" để an toàn với nguyên tắc cộng đồng.
- **`channels/ai-de-dung/dashboard.html`** — bảng điều khiển sản xuất (đã publish làm Artifact: https://claude.ai/artifact/QYNAmM9rAe6LZBw7WfTZRF, hiện đã có đủ dữ liệu 16 video): liệt kê từng video, mỗi video có nút copy "Lời thoại thuần" và copy "tất cả prompt cảnh AI" (mỗi dòng 1 lệnh) — dán thẳng vào bất kỳ tool nào. Sinh từ `pipeline/export_dashboard_data.py` (đọc trực tiếp từ `scripts/*.md`, không hand-transcribe).
- **Option A — AutoScene (người dùng đã có tài khoản, còn credit):** xác nhận qua ảnh chụp thật từ tài khoản người dùng rằng AutoScene dùng model **Veo 3.1** (Tạo video, "Nội dung lệnh mỗi dòng 1 lệnh" — khớp thẳng với "Bảng cảnh AI") và **Azure Speech** (Tạo giọng đọc, nhận nguyên khối text — khớp thẳng với "Lời thoại thuần"); có cả *Quản lý kênh* để tự đăng lên YouTube/TikTok sau khi người dùng tự kết nối kênh thật. Đây là đường nhanh nhất hiện tại — không cần setup gì thêm, chỉ cần copy/paste từ dashboard.
- **Option B — `pipeline/` tự host bằng Google Gemini API** (Veo + Gemini TTS + ffmpeg ráp): `common.py`, `generate_voice.py`, `generate_scenes.py`, `assemble.py`, `run_all.py`, `export_dashboard_data.py`. Đã kiểm chứng kỹ thuật (parsing + toàn bộ chuỗi ffmpeg end-to-end với dữ liệu giả lập ra đúng file 1920x1080 H.264+AAC khớp độ dài giọng đọc) — dùng khi hết credit AutoScene hoặc muốn kiểm soát nhiều hơn. Xác nhận mạng: `generativelanguage.googleapis.com` gọi được, `api.elevenlabs.io`/`api.runwayml.com` bị chặn.
- `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md` đã viết lại theo đúng 2 Option này.
- **Đã hỏi & chốt:** người dùng có thêm "OmniRoute" (router AI provider chạy ở `localhost:20128` trên máy họ, chỉ 4/348 provider đã cấu hình) — nhưng phiên Claude Code chạy cloud nên không với tới `localhost` của họ được. Người dùng quyết định **bỏ qua OmniRoute, tập trung vào Option A + B đã có** — không cần thêm code hỗ trợ base_url tuỳ chỉnh. Không hỏi lại việc này nữa trừ khi người dùng chủ động nhắc lại.

### Đang thiếu / chưa làm — ĐIỂM NGHẼN HIỆN TẠI
- **Giọng đọc: XONG 16/16, không còn việc gì ở đây.**
- **Cần người dùng bật billing tại aistudio.google.com** (Billing/Plan) — chặn duy nhất còn lại, chỉ ảnh hưởng tới **Veo** (tạo cảnh AI-video). Không có cách miễn phí nào thay Veo trong môi trường này (đã thử hết các domain TTS/AI khác, đều bị chặn mạng — xem log mốc #9).
- Chưa có video hoàn chỉnh (draft.mp4) nào — cần Veo hoạt động trước.
- Vẫn cần người dùng tự chụp vài tấm ảnh màn hình thao tác thật cho mỗi video (không phải quay, chỉ vài giây/tấm).
- Chưa kiểm tra tên/handle "AI Dễ Dùng" có bị trùng trên YouTube ngoài đời chưa.
- Kịch bản video #17 trở đi (Tier 1 còn lại #17-20 + Tier 2) chưa viết.
- Chưa có kênh thứ 2 (chủ đề khác).
- Option A (AutoScene) người dùng chưa báo lại đã thử hay chưa — vẫn là đường thay thế nếu billing Google AI tiếp tục vướng.

### Câu hỏi đang chờ người dùng quyết định
**Không có câu hỏi cần trả lời trong chat.** Người dùng đã dặn: tiếp tục làm song song, không hỏi lại, tự lưu tiến độ vào WORKLOG cho phiên sau. Việc duy nhất cần người dùng: **bật billing tại aistudio.google.com** rồi báo lại (không phải trả lời câu hỏi — là 1 thao tác). Khi có billing:
1. Claude chạy `generate_voice.py` cho 8 video #9-16 còn thiếu giọng đọc.
2. Claude chạy `generate_scenes.py --only 1` cho video #1 để xác nhận Veo hoạt động, rồi chạy hàng loạt qua `run_all.py`.
3. Nếu phiên hiện tại đã đóng, phiên mới đọc file này sẽ biết chính xác: 8/16 voice (video #1-8) đã có sẵn **trong git** tại `channels/ai-de-dung/assets/*/voice.wav` — clone repo là có ngay, không cần tạo lại.

### Việc tiếp theo nên làm (theo thứ tự ưu tiên)
1. **Người dùng:** bật billing cho Veo tại aistudio.google.com, báo lại Claude.
2. Claude chạy thử lại `generate_scenes.py --only 1` cho video #1 → nếu OK, chạy `run_all.py` cho video #1 trọn vẹn (voice + scenes, dừng lại xin ảnh chụp màn hình nếu thiếu).
3. Người dùng chụp ảnh màn hình theo danh sách được liệt kê, Claude chạy `assemble.py` ra `draft.mp4` đầu tiên — nghe/xem thử trước khi làm hàng loạt.
4. Nếu ổn, lặp lại cho video #2-16 (có thể chạy `generate_voice.py` cho tất cả trước vì không cần billing thêm).
5. Song song: Option A (AutoScene) vẫn là phương án thay thế nếu billing Google AI có vấn đề — dashboard đã sẵn sàng cho việc này.
6. Sau khi có video thật + số liệu, viết tiếp kịch bản #17+ và/hoặc mở kênh thứ 2 từ `framework/template/`.

---

## LOG CHI TIẾT (mới nhất ở trên)

### Mốc #9 — 2026-09-26 — Hoàn thành 16/16 giọng đọc miễn phí bằng xoay vòng model
**Yêu cầu người dùng:** "Nghiên cứu thêm các giọng miễn phí khác đi, test thử nghiệm ok mới đầu tư nha."

**Đã làm:**
1. Test reachability hàng loạt domain TTS miễn phí phổ biến: edge-tts (speech.platform.bing.com), Google Translate TTS, FPT.AI, Zalo AI, VBee, Viettel AI, HuggingFace, Replicate, Play.ht, Murf, Deepgram, Azure Cognitive Services, AWS Polly, StreamElements, VoiceRSS, Yandex, Google Cloud Text-to-Speech. Kết quả: **chỉ domain Google (đã dùng) và AWS Polly gọi được** — mọi domain khác bị chặn bởi chính sách mạng môi trường này (không phải do tài khoản).
2. Test `texttospeech.googleapis.com` (Cloud TTS, sản phẩm khác Gemini) — gọi được nhưng cần API key riêng scope vào domain này (credential hiện tại chỉ scope `generativelanguage.googleapis.com`) và gần chắc chắn cũng cần billing như mọi Cloud API khác — không theo đuổi tiếp vì lợi ích không rõ ràng so với công sức.
3. AWS Polly gọi được nhưng cần chữ ký SigV4 (access key + secret, không phải header tĩnh) — cơ chế "API credentials" của môi trường này chỉ hỗ trợ header tĩnh, không ký được SigV4 → không khả thi mà không có thêm code phức tạp.
4. **Phát hiện chính, giải quyết được vấn đề mà không cần domain mới:** quota miễn phí Gemini TTS tính riêng theo từng model. Test trực tiếp 4 model → `gemini-3.1-flash-tts-preview` và `gemini-3.8-flash-lite-tts` còn nguyên quota dù `gemini-3.8-flash-tts` đã hết.
5. Sửa `pipeline/generate_voice.py`: đổi từ 1 model cố định sang danh sách `TTS_MODELS`, tự thử lần lượt tới khi có model thành công; thêm `--model` để ép dùng 1 model cụ thể.
6. Chạy lại cho video #9 (test) rồi #10-16 (hàng loạt) → **tất cả 16/16 video giờ có giọng đọc thật**, không tốn thêm phí, không cần bật billing.

**Kết quả:** đúng yêu cầu người dùng — tận dụng hết giải pháp miễn phí trước khi cần đầu tư. Billing giờ chỉ còn cần cho Veo (video AI), không còn cần cho giọng đọc.

---

### Mốc #8 — 2026-09-26 — 8/16 giọng đọc thật (video #1-8), phát hiện free-tier 10/ngày
Chạy `generate_voice.py` hàng loạt cho video #2-16 (video #1 đã có từ trước): video #1-8 thành công, video #9-16 thất bại vì `429 RESOURCE_EXHAUSTED — GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue: 10` cho model `gemini-3.8-flash-tts` — xác nhận tài khoản đang ở gói miễn phí hoàn toàn (không chỉ Veo). Sửa `.gitignore` để giữ lại `voice.wav` trong git (tốn quota/tiền thật để tạo) nhưng vẫn loại `scenes/`, `screenshots/`, `draft.mp4` (rẻ/miễn phí để tạo lại). Commit 8 file `.wav` đầu tiên. (Vấn đề "10/ngày" này được giải quyết ngay sau đó ở Mốc #9.)

---

### Mốc #7 — 2026-09-26 — Xác thực Option B thật: TTS chạy được, Veo cần billing
**Diễn biến:** người dùng loay hoay thêm `GEMINI_API_KEY` qua UI Environment settings (đã gửi nhiều ảnh chụp màn hình thật). Hoá ra nền tảng này dùng cơ chế **"API credentials"** (khác "Environment variables") — tạo 1 credential tên "GEMINI API" áp cho domain `generativelanguage.googleapis.com`, hệ thống tự tiêm header xác thực ở tầng proxy, code không bao giờ thấy key thật.

**Đã làm:**
1. Sửa `pipeline/common.py::get_api_key()` — bỏ yêu cầu đọc `os.environ`, giờ trả về placeholder bất kỳ (vẫn ưu tiên env var thật nếu chạy ngoài môi trường này).
2. Test thật `generate_content` với model `gemini-2.5-flash` → lỗi 404 (model bị deprecate) → phát hiện tên model hiện tại qua `client.models.list()` → cập nhật `TTS_MODEL` = `gemini-3.8-flash-tts`, `VEO_MODEL` = `veo-3.1-generate-preview` (thêm `--model` flag để đổi sang `-fast`/`-lite`).
3. Test thật `generate_voice.py` cho video #1 → **thành công**, file `.wav` 100 giây, gửi người dùng nghe qua SendUserFile. Phát hiện & sửa: API trả `.wav` hoàn chỉnh (RIFF header), không phải PCM thô — code cũ sẽ bọc sai, đã sửa để ghi thẳng bytes khi phát hiện RIFF.
4. Test thật `generate_scenes.py --only 1` (Veo) cho video #1 → lỗi `429 RESOURCE_EXHAUSTED` — tài khoản chưa bật billing cho Veo. Báo người dùng bật billing tại aistudio.google.com.
5. Cập nhật WORKLOG với điểm nghẽn mới (billing Veo) thay cho điểm nghẽn cũ (thiếu key — đã qua).

**Kết quả:** Option B giờ đã được xác thực kỹ thuật thật (không còn là "chưa test"), chỉ còn chặn bởi billing phía người dùng.

---

### Mốc #6 — 2026-09-25 — Viết tiếp video #9-16, mở rộng lịch đăng lên 8 tuần
**Bối cảnh:** trong lúc chờ người dùng thêm `GEMINI_API_KEY` (đã thử dán key vào chat, bị hệ thống tự chặn vì lộ credential — xem mục "Câu hỏi đang chờ"), người dùng yêu cầu "tiếp tục song song việc khác". Việc tiếp theo trong danh sách ưu tiên là mở rộng backlog.

**Đã làm:**
1. Viết 8 kịch bản đầy đủ mới (video #9-16), theo đúng format zero-filming (Lời thoại thuần + Bảng cảnh AI) như #1-8.
2. **Đổi góc tiếp cận video #10**: ý tưởng gốc trong backlog là "làm bài tập không bị phát hiện đạo văn" — cố tình viết lại thành "dùng ChatGPT hỗ trợ học tập & viết bài đúng cách", tập trung vào học thật thay vì né tránh công cụ kiểm tra, để không cổ suý gian lận học thuật.
3. Cập nhật `backlog.md` (trạng thái + link kịch bản cho #9-16) và mở rộng `content-calendar.md` từ 4 tuần lên 8 tuần (thêm tuần 5-8, có checkpoint xem số liệu ở đầu tuần 7).
4. Chạy lại `pipeline/export_dashboard_data.py` (giờ đọc đúng 16 video), nhúng lại vào `dashboard.html`, sửa 1 chỗ hardcode "8 video" trong hiển thị bước 1 thành tính động theo `videos.length`. Republish Artifact (cùng URL, version 3).

**Kết quả:** kênh demo giờ có 16 kịch bản sẵn sàng (đủ cho 8 tuần đăng), dashboard phản ánh đúng số liệu mới.

---

### Mốc #5 — 2026-09-25 — Dashboard + phát hiện người dùng đã có AutoScene (Veo 3.1 + Azure Speech)
**Diễn biến:** người dùng hỏi có nên làm "1 quy trình html" không, dẫn nguồn https://www.autoscene.app/tao-video-ai-tu-dong (không fetch được, bị chặn mạng). Sau đó người dùng gửi liên tiếp nhiều ảnh chụp màn hình **từ chính tài khoản AutoScene của họ** (tên "Huynh", còn 2.000 credit): trang StoryFlow, trang Tạo hình ảnh, trang Tạo video (model **Veo 3.1 - Lite**, ô "Nội dung lệnh — mỗi dòng 1 lệnh"), trang Tạo giọng đọc (nền tảng **Azure Speech**, ô nhận nguyên khối văn bản), và trang Quản lý kênh (kết nối YouTube/TikTok để đăng tự động).

**Đã làm:**
1. Viết `pipeline/export_dashboard_data.py` — parse tất cả kịch bản thành JSON (phát hiện và fix luôn 1 lỗi: video #8 bị thiếu mục "Lời thoại thuần"/"Bảng cảnh AI" do bỏ dở lúc bị ngắt giữa chừng ở mốc trước).
2. Build `channels/ai-de-dung/dashboard.html` — trang gốc (không sao chép autoscene.app), thiết kế theo mô hình sản xuất mà cả 2 bên đều dùng: danh sách 8 video, mỗi video có nút copy "Lời thoại thuần" và nút copy "tất cả prompt cảnh AI" (mỗi dòng 1 lệnh — đúng định dạng ô nhập của AutoScene). Publish làm Artifact: https://claude.ai/artifact/QYNAmM9rAe6LZBw7WfTZRF, gửi file cho người dùng qua SendUserFile.
3. Viết lại `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md` thành 2 Option rõ ràng: **A = AutoScene** (đã có tài khoản, dùng ngay, không cần setup) và **B = pipeline/ tự host** (dự phòng, cần `GEMINI_API_KEY`). Cập nhật `pipeline/README.md` trỏ ngược về Option A ở đầu file.
4. Cập nhật 4 bước hiển thị trên dashboard để phản ánh đúng: bước 2-3 (chia cảnh, lồng tiếng) đã "Dán vào AutoScene" được ngay (không còn "blocked"), bước 4 (đăng) ghi rõ cần người dùng tự kết nối kênh thật ở *Quản lý kênh*.

**Kết quả:** người dùng có đường đi nhanh nhất tới video thật — không cần chờ API key nào — nhờ tài khoản AutoScene có sẵn. Pipeline Gemini API tự host (mốc #4) vẫn giữ nguyên làm phương án B.

---

### Mốc #4 — 2026-09-25 — Zero-filming + pipeline automation thật (Gemini API)
**Người dùng yêu cầu (2 tin nhắn liên tiếp):** không có thời gian quay, hỏi có dùng được ảnh-chuyển-video/text-to-video không; và nhấn mạnh đã làm thì phải chất lượng, ra kết quả tốt nhất, kể cả tốn phí dùng "flow của Google" cũng được; cũng hỏi có nên làm 1 quy trình HTML không.

**Đã làm:**
1. Thiết kế lại toàn bộ định dạng sản xuất thành **zero-filming**: ảnh chụp màn hình (giây, không quay) + AI text-to-video cho cảnh hook/B-roll + giọng đọc AI + auto-assembly. Cập nhật `channels/ai-de-dung/strategy/00` và `05`, cùng bản tương ứng trong `framework/template/00` và `05` để mặc định dùng cho mọi kênh sau này.
2. Thêm mục **"Lời thoại thuần"** (văn bản đọc liên tục) và **"Bảng cảnh AI"** (từng cảnh: ảnh chụp màn hình hay prompt AI-video) vào cả 8 file kịch bản trong `channels/ai-de-dung/scripts/`.
3. Kiểm tra kỹ thuật mạng: `generativelanguage.googleapis.com` (Google Gemini API — chính là "Flow" người dùng nhắc tới) gọi được; `api.elevenlabs.io`/`api.runwayml.com` bị chặn.
4. Build `pipeline/` — automation thật bằng Python + Gemini API (Veo + TTS) + ffmpeg: `common.py` (parse kịch bản), `generate_voice.py`, `generate_scenes.py`, `assemble.py`, `run_all.py`, `requirements.txt`, `README.md`.
5. Test kỹ thuật: parsing kịch bản đúng (video #1: 4 cảnh AI-video, 2 cảnh ảnh chụp màn hình nhận diện chính xác); toàn bộ chuỗi ffmpeg trong `assemble.py` chạy thành công end-to-end với dữ liệu giả lập, ra đúng video 1920x1080 H.264+AAC khớp độ dài audio.
6. Đây thay cho việc chỉ làm "1 trang HTML" như người dùng hỏi — pipeline chạy server-side (Python) mạnh hơn và an toàn hơn (API key không lộ ra trình duyệt); có thể làm thêm dashboard HTML để xem trạng thái/nội dung ở bước sau nếu cần.

**Điểm nghẽn hiện tại:** chưa có `GEMINI_API_KEY` nên chưa gọi API thật được lần nào — code gọi Veo/TTS dựa trên tài liệu API tại thời điểm viết, chưa xác minh với request thật.

---

### Mốc #3 — 2026-09-25 — Hoàn thành kịch bản cho toàn bộ 4 tuần đầu
**Đã làm:** viết tiếp 4 kịch bản đầy đủ còn thiếu (video #5 AI miễn phí tốt nhất, #6 AI viết CV, #7 AI viết email, #8 Gemini trên điện thoại) trong `channels/ai-de-dung/scripts/`. Cập nhật `backlog.md` và `content-calendar.md` để phản ánh cả 8/8 video đã sẵn sàng quay.

**Kết quả:** toàn bộ phần lập kế hoạch + viết kịch bản mà Claude tự làm được cho 4 tuần đầu của kênh demo đã hoàn tất. Điểm nghẽn tiếp theo là khâu thực thi vật lý (quay/dựng/đăng) — thuộc về người dùng, không phải việc Claude có thể tự động hoá trong môi trường này.

---

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
