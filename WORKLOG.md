# Nhật ký làm việc & trạng thái dự án

> **Đọc file này đầu tiên** khi mở repo ở bất kỳ phiên Claude/tài khoản nào khác. Mục "TRẠNG THÁI HIỆN TẠI" luôn được cập nhật ở đầu file — phần log bên dưới chỉ để tra cứu lịch sử.

---

## TRẠNG THÁI HIỆN TẠI
*(cập nhật lần cuối: mốc #13 — 2026-09-26)*

### 🎬 ĐỘT PHÁ: cảnh AI-video giờ MIỄN PHÍ HOÀN TOÀN, không cần Veo/billing nữa
Người dùng phản đối mạnh chi phí Veo ("nghĩ cách free đi, trên mạng đầy cách mà bạn chọn cách này thì để tôi làm lun chứ cần gì bạn nữa?"). Đã tìm và xác thực xong hướng miễn phí thật:
- **`pipeline/generate_motion_graphic.py`** (mới) — dựng thẳng cảnh minh hoạ bằng Pillow + ffmpeg (không gọi API nào), theo đúng bảng màu/font thương hiệu ở `08-nhan-dien-thuong-hieu.md` (nền `#14171C`, accent `#E8A33D`, font Be Vietnam Pro Bold tải từ Google Fonts). Ghi ra đúng vị trí `assets/<slug>/scenes/NN.mp4` mà Veo từng ghi → `assemble.py` dùng chung, không cần sửa gì.
- **Đã chạy demo video #1, người dùng xác nhận ổn, rồi chạy hàng loạt cho toàn bộ 16 video còn lại** ("tiếp tục") → **kết quả: 45/45 cảnh AI-video của cả 16/16 video đã dựng xong, miễn phí 100%, 0 lỗi.**
- Veo/`generate_scenes.py` vẫn giữ trong code làm lựa chọn phụ (nếu sau này muốn ảnh photorealistic thật và chấp nhận trả phí — đã tính sẵn giá thật ở `pipeline/README.md`), nhưng **không còn là điểm nghẽn của kênh nữa**.
- Đã cập nhật `pipeline/README.md`, `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md`, `framework/template/05` và `framework/template/08` để phản ánh hướng miễn phí này làm mặc định cho mọi kênh (kể cả kênh mới sau này).
- **Điểm nghẽn thật còn lại của kênh demo giờ CHỈ CÒN**: (1) người dùng chọn giọng nam, (2) người dùng tự chụp ảnh màn hình thật cho từng video — 2 việc này không có cách nào Claude tự làm được trong môi trường này.

### 🎨 Đã có bộ nhận diện thương hiệu — chống loãng/"kênh rác"
Người dùng hỏi "làm sao để kênh không loãng, không phải kênh rác" → đồng ý đề xuất → đã xử lý:
- **File mới `channels/ai-de-dung/strategy/08-nhan-dien-thuong-hieu.md`**: bảng màu cố định (kế thừa từ dashboard: nền `#14171C`, accent `#E8A33D`), font cố định (Be Vietnam Pro), watermark góc màn hình, **bumper mở/kết cố định dùng chung cho MỌI video** (thay vì mỗi video có cảnh mở/kết riêng do Veo tạo — vừa tăng nhận diện vừa tiết kiệm ~32 lượt gọi Veo cho 16 video hiện có), câu khẩu hiệu đọc trong video, hệ thống đặt tên các "framework" riêng (đã có sẵn công thức VBYĐ ở video #4), và nguyên tắc "không đổi" các yếu tố nhận diện đã chốt.
- Cập nhật `strategy/00` (trỏ tới file mới) và `strategy/05` (tích hợp bumper cố định vào quy trình ráp video + checklist QC).
- Đã nhân bản thành `framework/template/08-nhan-dien-thuong-hieu.md` để MỌI kênh sau này đều bắt buộc có bước này trước khi làm video đầu tiên.
- **CỐ Ý CHƯA áp dụng câu khẩu hiệu (spoken tagline) vào 16 file kịch bản/giọng đọc hiện có** — sẽ gộp chung vào lần tạo lại giọng đọc kế tiếp (khi đổi sang giọng nam đã chọn ở mục dưới), tránh tạo lại audio 2 lần cho 2 mục đích riêng lẻ.
- **Chưa tạo file `intro-bumper.mp4`/`outro-bumper.mp4` thật** — giờ KHÔNG cần Veo nữa, có thể tạo ngay bằng `generate_motion_graphic.py` (xem mốc #13) — chỉ còn thiếu bước soạn 2 câu mô tả ngắn cho mỗi bumper rồi chạy script, chưa làm vì đang ưu tiên xong 45 cảnh của 16 video trước.

### 🎤 Đang chờ người dùng chọn GIỌNG NAM — sẽ tạo lại toàn bộ 16 video sau khi chọn
Người dùng yêu cầu đổi sang giọng nam (hiện đang dùng "Kore" — giọng nữ), và không muốn trộn nam/nữ giữa các video. Đã tạo 3 mẫu giọng nam bằng model `gemini-3.1-flash-tts-preview` (chỉ dùng để test giọng, không phải model chuẩn sản xuất) và gửi người dùng nghe: **Puck, Charon, Fenrir** — hết quota model test sau 3 mẫu này, chưa test thêm được (Orus, Algenib... để dành nếu người dùng muốn nghe thêm, đợi quota mai reset).

**Sự cố đã sửa (2026-09-26):** 3 file mẫu gửi lần đầu bị lỗi "không mở được" trên máy người dùng (Windows báo `0xC00D36C4`) — do file gốc là PCM thô ghi thẳng, thiếu hoàn toàn header RIFF/WAVE (khác với `generate_voice.py` — script chuẩn đã kiểm tra và bọc header đúng, 16 file `voice.wav` thật trong git không bị lỗi này). Đã bọc lại header WAV cho đúng 3 file mẫu từ dữ liệu PCM gốc (không cần gọi lại API, không tốn thêm quota) và gửi lại — xác nhận qua `ffmpeg -af volumedetect` là có âm thanh thật (không phải file rỗng/nhiễu).

**Đang chờ người dùng chọn 1 trong 3 (hoặc xin nghe thêm giọng khác).** Sau khi chọn xong:
1. Sửa `pipeline/generate_voice.py`: đổi `--voice` mặc định (hiện đang hardcode "Kore" ở `argparse` default) sang tên giọng nam đã chọn.
2. Tạo lại **toàn bộ 16/16 file `voice.wav`** bằng model chuẩn `gemini-3.8-flash-lite-tts` + giọng nam mới chọn — không chỉ 11 file bị lệch model như tính toán ở mốc #10 nữa, vì đằng nào cũng phải tạo lại hết do đổi giọng (nam thay nữ), nên bỏ luôn kế hoạch "chỉ tạo lại 11 file" ở mốc #10.
3. Quota 10/ngày/model — 16 file có thể cần chia làm 2 ngày nếu dùng chung 1 model.

### ⚠️ (Đã lỗi thời — xem mục trên) Giọng đọc 16/16 KHÔNG ĐỒNG NHẤT model — đang chờ người dùng nghe & quyết định
Người dùng yêu cầu: "giữ 1 giọng đọc, đừng thay đổi liên tục khi đổi model". Đúng — do cơ chế tự xoay vòng ở mốc #9, hiện tại:
- **Video #1-8, #10, #14, #15 (11 video)** dùng model `gemini-3.8-flash-tts`
- **Video #9, #11, #12, #13, #16 (5 video)** dùng model `gemini-3.8-flash-lite-tts`
- Cùng `voice_name="Kore"` nhưng khác model — có thể nghe hơi khác chất lượng/âm sắc.

**Đã sửa `pipeline/generate_voice.py`:** bỏ hoàn toàn cơ chế tự động xoay vòng model. Giờ `TTS_MODEL` là **1 hằng số cố định duy nhất** (`gemini-3.8-flash-lite-tts`), không tự đổi khi lỗi/hết quota — script sẽ báo lỗi rõ ràng và dừng lại thay vì âm thầm dùng model khác. Muốn đổi model chuẩn của kênh: sửa đúng 1 dòng `TTS_MODEL` rồi tạo lại toàn bộ cho nhất quán.

**Đã gửi người dùng 2 file mẫu để so sánh:** video #1 (model `gemini-3.8-flash-tts`) và video #9 (model `gemini-3.8-flash-lite-tts`) — **đang chờ người dùng nghe và trả lời có khác biệt rõ không**, trước khi quyết định có cần tạo lại 11 video #1-8,10,14,15 bằng model `gemini-3.8-flash-lite-tts` cho đồng nhất hay không (chưa tạo lại để tránh tốn quota nếu hoá ra không cần thiết — quota `gemini-3.8-flash-lite-tts` hôm nay đã dùng ~7/10, không đủ tạo lại cả 11 video trong 1 ngày).

**Nếu người dùng xác nhận "có, tạo lại cho giống nhau" ở phiên sau:** chạy `python3 pipeline/generate_voice.py channels/ai-de-dung/scripts/0{1,2,3,4,5,6,7,8}-*.md channels/ai-de-dung/scripts/10-*.md channels/ai-de-dung/scripts/14-*.md channels/ai-de-dung/scripts/15-*.md` (từng file một, script không nhận nhiều file cùng lúc — cần lặp) — model mặc định giờ đã là `gemini-3.8-flash-lite-tts` nên không cần thêm `--model`. Có thể cần chia làm nhiều ngày do quota 10/ngày.

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
- **Giọng đọc: XONG 16/16** (nhưng đang chờ chọn giọng nam để tạo lại — xem mục trên).
- **Cảnh AI-video: XONG 45/45 (16/16 video), miễn phí, 0 lỗi (mốc #13)** — không còn cần Veo/billing cho bước này nữa.
- **Bumper mở/kết thương hiệu:** chưa tạo file thật (chỉ còn thiếu bước chạy `generate_motion_graphic.py`, không còn bị chặn bởi billing).
- Chưa có video hoàn chỉnh (draft.mp4) nào ngoài demo video #1 (dùng ảnh chụp màn hình giả lập) — vì còn thiếu ảnh chụp màn hình thật cho mọi video.
- **Vẫn cần người dùng tự chụp vài tấm ảnh màn hình thao tác thật cho mỗi video** (không phải quay, chỉ vài giây/tấm) — không có cách tự động nào thay được, đây là điểm nghẽn thật duy nhất còn lại để ráp `draft.mp4` hàng loạt.
- Chưa kiểm tra tên/handle "AI Dễ Dùng" có bị trùng trên YouTube ngoài đời chưa.
- Kịch bản video #17 trở đi (Tier 1 còn lại #17-20 + Tier 2) chưa viết.
- Chưa có kênh thứ 2 (chủ đề khác).
- Veo/billing/AutoScene giờ chỉ còn là lựa chọn phụ (nếu muốn ảnh photorealistic) — không còn là điểm nghẽn để hoàn thành kênh.

### Câu hỏi đang chờ người dùng quyết định (bổ sung)
**Nghe 2 file mẫu đã gửi (video #1 vs video #9) — có khác giọng rõ không?** Nếu có/nghi ngờ, báo Claude tạo lại 11 video dùng sai model cho đồng nhất (xem hướng dẫn ở mục trên). Nếu nghe giống nhau, không cần làm gì thêm — giữ nguyên 16 file hiện tại.

### Câu hỏi đang chờ người dùng quyết định (trước đó — vẫn còn hiệu lực)
**Không có câu hỏi cần trả lời trong chat.** Người dùng đã dặn: tiếp tục làm song song, không hỏi lại, tự lưu tiến độ vào WORKLOG cho phiên sau. Việc duy nhất cần người dùng: **bật billing tại aistudio.google.com** rồi báo lại (không phải trả lời câu hỏi — là 1 thao tác). Khi có billing:
1. Claude chạy `generate_voice.py` cho 8 video #9-16 còn thiếu giọng đọc.
2. Claude chạy `generate_scenes.py --only 1` cho video #1 để xác nhận Veo hoạt động, rồi chạy hàng loạt qua `run_all.py`.
3. Nếu phiên hiện tại đã đóng, phiên mới đọc file này sẽ biết chính xác: 8/16 voice (video #1-8) đã có sẵn **trong git** tại `channels/ai-de-dung/assets/*/voice.wav` — clone repo là có ngay, không cần tạo lại.

### Việc tiếp theo nên làm (theo thứ tự ưu tiên)
1. **Người dùng:** chọn 1 trong 3 giọng nam đã gửi (Puck/Charon/Fenrir) hoặc xin nghe thêm.
2. Sau khi chọn xong: Claude tạo lại toàn bộ 16/16 `voice.wav` với giọng mới + gộp luôn câu khẩu hiệu thương hiệu (xem mục "Đang chờ chọn giọng nam" ở trên) — có thể cần chia 2 ngày do quota 10/ngày/model.
3. Claude tạo 2 file `intro-bumper.mp4`/`outro-bumper.mp4` bằng `generate_motion_graphic.py` (không còn bị chặn, chỉ cần soạn 2 câu mô tả ngắn).
4. **Người dùng:** tự chụp ảnh màn hình thật theo "Bảng cảnh AI" của từng video (điểm nghẽn thật duy nhất còn lại).
5. Sau khi có ảnh chụp màn hình, Claude chạy `assemble.py` ra `draft.mp4` cho từng video, nghe/xem thử video đầu trước khi làm hàng loạt.
6. Sau khi có video thật + số liệu, viết tiếp kịch bản #17+ và/hoặc mở kênh thứ 2 từ `framework/template/`.

---

## LOG CHI TIẾT (mới nhất ở trên)

### Mốc #13 — 2026-09-26 — Thay Veo bằng đồ hoạ chuyển động tự dựng — MIỄN PHÍ, xong 16/16 video
**Yêu cầu người dùng (rất gay gắt):** "vẫn thốn lắm... nghĩ cách free đi, trên mạng đầy cách mà bạn chọn cách này thì để tôi làm lun chứ cần gì bạn nữa? bạn là chuyên gia trong lĩnh vực này mà?" — sau khi biết Veo cần bật billing thật và ước tính chi phí ~$20-25 cho cả kênh (dùng bản Lite).

**Đã làm:**
1. Kiểm tra thực tế mọi hướng miễn phí khác trước khi kết luận: ElevenLabs, RunwayML, edge-tts, Google Translate TTS, FPT.AI, Zalo AI, VBee, HuggingFace, Replicate, Play.ht, Deepgram, Azure, Pexels, Pixabay, Yandex — tất cả bị chặn bởi chính sách mạng môi trường này. Gemini native image generation (`gemini-3.1-flash-lite-image`...) cũng bị chặn billing giống Veo (`limit: 0` free tier).
2. **Nhận ra bản chất vấn đề:** phần lớn cảnh "AI text-to-video" trong kịch bản chỉ là card đồ hoạ đơn giản (cảnh báo, so sánh, đồng hồ, CTA chữ) — không cần ảnh photorealistic. Viết `pipeline/generate_motion_graphic.py`: dựng thẳng bằng Pillow (đúng bảng màu/font thương hiệu, tải font Be Vietnam Pro Bold thật từ Google Fonts — domain này gọi được và có đủ dấu tiếng Việt, đã xác nhận qua `fc-scan`) rồi áp hiệu ứng Ken Burns bằng ffmpeg. Ghi ra đúng vị trí `assets/<slug>/scenes/NN.mp4` mà `generate_scenes.py` (Veo) từng ghi → **`assemble.py` dùng chung, không cần sửa gì** — 2 script thay thế nhau hoàn toàn.
3. Xử lý các chi tiết chất lượng: tự nhận diện style cảnh theo từ khoá trong mô tả (`pick_style`: cảnh báo/so sánh/CTA/đồng hồ/thông thường), vẽ icon tương ứng bằng primitives của Pillow, rút gọn mô tả dài dòng thành nhãn chữ ngắn hiển thị trên khung hình (`shorten_label` — lọc bỏ các cụm dẫn nhập như "Cảnh mở đầu:", "Ảnh chụp màn hình", dấu ngoặc kép thừa), watermark tên kênh cố định góc dưới phải.
4. **Test demo video #1 trước** (voice + graphics + ảnh chụp màn hình giả lập), gửi người dùng xem/nghe xác nhận ổn.
5. Người dùng xác nhận, yêu cầu "tiếp tục" → chạy hàng loạt `generate_motion_graphic.py` cho toàn bộ video #2-16 (chạy nền, không cần theo dõi liên tục).
6. **Kết quả xác nhận qua log + kiểm tra thư mục:** 45/45 cảnh AI-video của cả 16/16 video đã dựng xong thành công, 0 lỗi thật (chỉ có 1 kết quả khớp "lỗi" trong log là do trùng từ trong nội dung mô tả cảnh, không phải lỗi chạy).
7. Cập nhật tài liệu để phản ánh hướng mới làm mặc định: viết lại `pipeline/README.md` (Veo giờ là "Option phụ", có kèm bảng giá thật đã tra cứu Vertex AI pricing), viết lại `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md` (đã làm ở phiên trước khi bị ngắt), và nhân bản triết lý này sang `framework/template/05-quy-trinh-lam-video-nhanh.md` + `framework/template/08-nhan-dien-thuong-hieu.md` (mục bumper) để mọi kênh mới sau này mặc định miễn phí ngay từ đầu, không phải đi qua đường Veo rồi mới quay lại tìm hướng free như kênh demo này.

**Kết quả:** giải quyết dứt điểm phản đối chi phí của người dùng — kênh demo giờ **không còn điểm nghẽn tài chính nào** để hoàn thành sản xuất. Veo vẫn giữ trong code làm lựa chọn phụ, không xoá, phòng khi sau này muốn ảnh photorealistic thật và chấp nhận trả phí.

**Chưa làm:** bumper mở/kết thật (chỉ còn thiếu bước chạy script + soạn 2 câu mô tả, không còn bị chặn kỹ thuật); giọng nam vẫn đang chờ người dùng chọn; ảnh chụp màn hình thật vẫn cần người dùng tự làm.

---

### Mốc #12 — 2026-09-26 — Xây bộ nhận diện thương hiệu chống loãng
**Diễn biến:** Claude chủ động hỏi ý kiến người dùng (câu hỏi định hướng, 2-3 câu) về việc làm sao tránh kênh trông "loãng"/"kênh rác" khi 100% sản xuất bằng AI. Người dùng đồng ý đề xuất, yêu cầu xử lý luôn.

**Đã làm:**
1. Viết `channels/ai-de-dung/strategy/08-nhan-dien-thuong-hieu.md` — 7 mục: bảng màu, font, watermark, bumper mở/kết cố định (kèm 2 prompt Veo cụ thể), câu khẩu hiệu, hệ thống đặt tên framework riêng (VBYĐ), nguyên tắc không đổi tuỳ tiện.
2. Cập nhật `strategy/00-tong-quan-kenh.md` (thêm mục trỏ tới brand guide) và `strategy/05-quy-trinh-lam-video-nhanh.md` (thêm bước bắt buộc tạo bumper 1 lần + checklist QC mới).
3. Nhân bản thành `framework/template/08-nhan-dien-thuong-hieu.md` với placeholder — để mọi kênh mới sau này qua `framework/` đều có bước này ngay từ đầu, không phải nghĩ lại từ số 0.
4. **Quyết định có chủ đích:** không áp dụng câu khẩu hiệu vào giọng đọc/kịch bản hiện có ngay — gộp vào đợt tạo lại giọng nam sắp tới (mốc #11) để tránh tốn quota TTS 2 lần liên tiếp cho 2 lý do khác nhau.

**Chưa làm (cần Veo, đang chờ billing):** tạo file `intro-bumper.mp4`/`outro-bumper.mp4` thật từ 2 prompt đã viết sẵn.

---

### Mốc #11 — 2026-09-26 — Test giọng nam theo yêu cầu người dùng
**Yêu cầu người dùng:** "Đang miễn phí, dùng giọng nào cũng được, cố gắng giọng nam được không? Hay phải trộn cả nữ?"

**Đã làm:** Tạo 3 file mẫu giọng nam (Puck, Charon, Fenrir) cùng đọc 1 câu tiếng Việt, dùng model `gemini-3.1-flash-tts-preview` (chỉ để test, không phải model chuẩn) để không đụng vào quota của `gemini-3.8-flash-lite-tts` (model chuẩn sản xuất). Gửi cả 3 cho người dùng nghe. Hết quota model test sau 3 mẫu (còn Orus, Algenib chưa test được, để dành nếu cần).

**Đang chờ:** người dùng chọn 1 giọng nam. Kế hoạch cũ ở mốc #10 (chỉ tạo lại 11/16 video bị lệch model) **không còn áp dụng** — vì đổi giọng nữ sang nam thì phải tạo lại cả 16/16 video, không phân biệt model cũ dùng gì.

---

### Mốc #10 — 2026-09-26 — Bỏ auto-rotate model TTS, giữ giọng đọc nhất quán
**Yêu cầu người dùng:** "Cố gắng giữ 1 giọng đọc, đừng thay đổi liên tục khi đổi model được không?"

**Đã làm:**
1. Kiểm tra lại: cơ chế xoay vòng ở mốc #9 khiến 11/16 video dùng `gemini-3.8-flash-tts`, 5/16 dùng `gemini-3.8-flash-lite-tts` — đúng như người dùng lo ngại, không nhất quán.
2. Sửa `pipeline/generate_voice.py`: xoá hoàn toàn logic thử lần lượt nhiều model. Thay bằng 1 hằng số `TTS_MODEL` cố định (chọn `gemini-3.8-flash-lite-tts` vì còn nhiều quota nhất tính tới lúc này). Khi model lỗi/hết quota, script dừng lại và báo lỗi rõ ràng thay vì âm thầm đổi model khác.
3. Gửi người dùng 2 file mẫu để tự nghe so sánh: video #1 (`gemini-3.8-flash-tts`) và video #9 (`gemini-3.8-flash-lite-tts`) — chưa vội tạo lại 11 video vì (a) chưa chắc 2 model nghe khác nhau thật sự, (b) quota `gemini-3.8-flash-lite-tts` hôm nay gần hết (đã dùng ~7/10), không đủ tạo lại hết 11 video trong 1 lần.

**Đang chờ:** người dùng nghe 2 file, xác nhận có cần tạo lại 11 video #1-8,10,14,15 cho đồng nhất hay không.

---

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
