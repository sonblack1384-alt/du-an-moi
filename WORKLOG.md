# Nhật ký làm việc & trạng thái dự án

> **Đọc file này đầu tiên** khi mở repo ở bất kỳ phiên Claude/tài khoản nào khác. Mục "TRẠNG THÁI HIỆN TẠI" luôn được cập nhật ở đầu file — phần log bên dưới chỉ để tra cứu lịch sử.

---

## TRẠNG THÁI HIỆN TẠI
*(cập nhật lần cuối: mốc #15 — 2026-09-26)*

### ✅ CẢ 16/16 VIDEO ĐÃ CÓ `draft.mp4` — KHÔNG CẦN NGƯỜI DÙNG THAO TÁC GÌ NỮA
Người dùng phản ứng gay gắt khi biết vẫn phải tự chụp ảnh màn hình cho mỗi video ("đã tự động hoá mà còn chụp gửi") → **quyết định bỏ hẳn yêu cầu chụp ảnh thật, chấp nhận đánh đổi mất cảnh demo giao diện phần mềm thật**. Đã xử lý xong (mốc #15):
- Chuyển toàn bộ 59 cảnh "Ảnh chụp màn hình" trong 16 kịch bản sang "AI text-to-video" (đồ hoạ chữ/icon tự dựng, giống các cảnh B-roll khác).
- Dựng lại toàn bộ cảnh (108 cảnh/16 video, 0 lỗi) và **ráp thành công `draft.mp4` cho cả 16/16 video** — pipeline giờ chạy từ đầu đến cuối (giọng đọc → cảnh minh hoạ → bumper → ráp) hoàn toàn không cần người dùng làm gì.
- Đã gửi người dùng video #1 xem thử.
- Cập nhật `CLAUDE.md`, `strategy/00`+`05`, `framework/template/00`+`05` phản ánh mặc định mới; xoá `screenshot-checklist.md` (lỗi thời).
- **Việc chụp ảnh màn hình giờ chỉ còn là lựa chọn NÂNG CẤP sau này nếu người dùng chủ động muốn** (đổi 1 dòng Nguồn trong Bảng cảnh AI) — không phải yêu cầu bắt buộc, không tự ý đề xuất lại.

### 🎤 Giọng Charon: 13/16 video đã có giọng cuối cùng, 3 video (#14-16) chờ quota TTS reset
Đã chọn giọng Charon (mốc #14), đã tạo lại giọng cho video #1-13. Video #14-16 vẫn dùng giọng Kore cũ (chưa có khẩu hiệu thương hiệu) do quota `gemini-3.8-flash-lite-tts` (10 lượt/ngày thật) — **đã xác nhận đây là quota thật theo ngày, KHÔNG phải chờ vài giây** (`retryDelay` trong lỗi 429 chỉ là gợi ý backoff, đã test thực tế vẫn lỗi sau khi đợi). Phiên sau chỉ cần chạy lại `generate_voice.py` cho #14-16 rồi `assemble.py` lại 3 video đó khi quota mở.

### 🎨 Đã có bộ nhận diện thương hiệu — chống loãng/"kênh rác"
Người dùng hỏi "làm sao để kênh không loãng, không phải kênh rác" → đồng ý đề xuất → đã xử lý:
- **File mới `channels/ai-de-dung/strategy/08-nhan-dien-thuong-hieu.md`**: bảng màu cố định (kế thừa từ dashboard: nền `#14171C`, accent `#E8A33D`), font cố định (Be Vietnam Pro), watermark góc màn hình, **bumper mở/kết cố định dùng chung cho MỌI video** (thay vì mỗi video có cảnh mở/kết riêng do Veo tạo — vừa tăng nhận diện vừa tiết kiệm ~32 lượt gọi Veo cho 16 video hiện có), câu khẩu hiệu đọc trong video, hệ thống đặt tên các "framework" riêng (đã có sẵn công thức VBYĐ ở video #4), và nguyên tắc "không đổi" các yếu tố nhận diện đã chốt.
- Cập nhật `strategy/00` (trỏ tới file mới) và `strategy/05` (tích hợp bumper cố định vào quy trình ráp video + checklist QC).
- Đã nhân bản thành `framework/template/08-nhan-dien-thuong-hieu.md` để MỌI kênh sau này đều bắt buộc có bước này trước khi làm video đầu tiên.
- **CỐ Ý CHƯA áp dụng câu khẩu hiệu (spoken tagline) vào 16 file kịch bản/giọng đọc hiện có** — sẽ gộp chung vào lần tạo lại giọng đọc kế tiếp (khi đổi sang giọng nam đã chọn ở mục dưới), tránh tạo lại audio 2 lần cho 2 mục đích riêng lẻ.
- **Bumper mở/kết: ĐÃ XONG** (mốc #14) — `channels/ai-de-dung/assets/_brand/{intro,outro}-bumper.mp4` đã tạo bằng `generate_motion_graphic.py`, và `pipeline/assemble.py` đã tự động ghép vào đầu/cuối MỌI video (tự bù khoảng lặng audio) — không cần thao tác gì thêm khi ráp video mới.

*(Chi tiết lịch sử đầy đủ về quá trình chọn giọng, xử lý quota TTS, xác thực API... xem "LOG CHI TIẾT" mốc #7-14 bên dưới — phần trên đã tóm tắt đúng trạng thái thật hiện tại.)*

### Đã có
- **Khung sườn dùng chung** (`framework/`) — 8 file template + hướng dẫn tạo kênh mới, mặc định zero-filming.
- **Kênh demo "AI Dễ Dùng"** (`channels/ai-de-dung/`) — 8 file chiến lược, backlog 100 ý tưởng, lịch đăng **8 tuần** (mở rộng từ 4 tuần), **16/16 kịch bản đầy đủ** (video #1-16) — mỗi kịch bản có "Lời thoại thuần" (dán thẳng vào TTS) và "Bảng cảnh AI" (từng cảnh: ảnh chụp màn hình hay prompt AI-video). Video #10 đã đổi góc tiếp cận từ "làm bài không bị phát hiện đạo văn" sang "học tập đúng cách" để an toàn với nguyên tắc cộng đồng.
- **`channels/ai-de-dung/dashboard.html`** — bảng điều khiển sản xuất (đã publish làm Artifact: https://claude.ai/artifact/QYNAmM9rAe6LZBw7WfTZRF, hiện đã có đủ dữ liệu 16 video): liệt kê từng video, mỗi video có nút copy "Lời thoại thuần" và copy "tất cả prompt cảnh AI" (mỗi dòng 1 lệnh) — dán thẳng vào bất kỳ tool nào. Sinh từ `pipeline/export_dashboard_data.py` (đọc trực tiếp từ `scripts/*.md`, không hand-transcribe).
- **Option A — AutoScene (người dùng đã có tài khoản, còn credit):** xác nhận qua ảnh chụp thật từ tài khoản người dùng rằng AutoScene dùng model **Veo 3.1** (Tạo video, "Nội dung lệnh mỗi dòng 1 lệnh" — khớp thẳng với "Bảng cảnh AI") và **Azure Speech** (Tạo giọng đọc, nhận nguyên khối text — khớp thẳng với "Lời thoại thuần"); có cả *Quản lý kênh* để tự đăng lên YouTube/TikTok sau khi người dùng tự kết nối kênh thật. Đây là đường nhanh nhất hiện tại — không cần setup gì thêm, chỉ cần copy/paste từ dashboard.
- **Option B — `pipeline/` tự host bằng Google Gemini API** (Veo + Gemini TTS + ffmpeg ráp): `common.py`, `generate_voice.py`, `generate_scenes.py`, `assemble.py`, `run_all.py`, `export_dashboard_data.py`. Đã kiểm chứng kỹ thuật (parsing + toàn bộ chuỗi ffmpeg end-to-end với dữ liệu giả lập ra đúng file 1920x1080 H.264+AAC khớp độ dài giọng đọc) — dùng khi hết credit AutoScene hoặc muốn kiểm soát nhiều hơn. Xác nhận mạng: `generativelanguage.googleapis.com` gọi được, `api.elevenlabs.io`/`api.runwayml.com` bị chặn.
- `channels/ai-de-dung/strategy/05-quy-trinh-lam-video-nhanh.md` đã viết lại theo đúng 2 Option này.
- **Đã hỏi & chốt:** người dùng có thêm "OmniRoute" (router AI provider chạy ở `localhost:20128` trên máy họ, chỉ 4/348 provider đã cấu hình) — nhưng phiên Claude Code chạy cloud nên không với tới `localhost` của họ được. Người dùng quyết định **bỏ qua OmniRoute, tập trung vào Option A + B đã có** — không cần thêm code hỗ trợ base_url tuỳ chỉnh. Không hỏi lại việc này nữa trừ khi người dùng chủ động nhắc lại.

### Đang thiếu / chưa làm — ĐIỂM NGHẼN HIỆN TẠI
- **Giọng đọc: 13/16 xong** (Charon + khẩu hiệu). Video #14-16 vẫn giọng cũ, chờ quota `gemini-3.8-flash-lite-tts` reset (quota ngày thật, không phải giây).
- **Cảnh AI-video + draft.mp4: XONG 16/16** — không còn cảnh nào cần ảnh chụp màn hình thật (mốc #15). Video #14-16 cần ráp lại sau khi có giọng mới.
- **Bumper mở/kết thương hiệu: XONG**, tự động ghép vào mọi video.
- Chưa kiểm tra tên/handle "AI Dễ Dùng" có bị trùng trên YouTube ngoài đời chưa.
- Kịch bản video #17 trở đi (Tier 1 còn lại #17-20 + Tier 2) chưa viết.
- Chưa có kênh thứ 2 (chủ đề khác).
- Người dùng chưa xem/duyệt bản `draft.mp4` mới nhất (đã gửi video #1 mẫu, chờ phản hồi).
- Veo/billing/AutoScene/ảnh chụp màn hình thật giờ đều chỉ là lựa chọn phụ/nâng cấp — không phải điểm nghẽn để hoàn thành kênh.

### Việc tiếp theo nên làm (theo thứ tự ưu tiên)
1. **Claude (phiên sau, thử ngay khi mở lại):** chạy `python3 pipeline/generate_voice.py channels/ai-de-dung/scripts/{14,15,16}-*.md` (từng file), rồi `python3 pipeline/assemble.py` lại đúng 3 video đó, để hoàn tất 16/16 giọng Charon + khẩu hiệu.
2. Chờ người dùng duyệt draft.mp4 (đã gửi video #1) — nếu cần sửa nội dung/pacing thì sửa kịch bản rồi tạo lại đúng phần đó (không cần tạo lại từ đầu toàn kênh).
3. Sau khi kênh được duyệt, viết tiếp kịch bản #17+ và/hoặc mở kênh thứ 2 từ `framework/template/`.

---

## LOG CHI TIẾT (mới nhất ở trên)

### Mốc #15 — 2026-09-26 — Bỏ hẳn yêu cầu chụp ảnh màn hình, ráp xong draft.mp4 cho cả 16 video
**Diễn biến:** gửi người dùng xem demo video #1 (ảnh chụp màn hình còn là placeholder) → người dùng hỏi thẳng "chỉ đọc vậy thôi hả, không có màn hình hiện lên hướng dẫn gì à". Giải thích rằng cần ảnh chụp thật, môi trường này không có trình duyệt để tự chụp, người dùng phải tự chụp gửi. Người dùng phản ứng rất gay gắt ("đã tự động hoá mà còn chụp gửi, ngu bỏ mịa", "tốn thời gian cả ngày", "chả làm được mịa gì") và khi được hỏi có muốn đổi format để né hẳn việc chụp ảnh không, trả lời "dẹp mịa cho phẻ" — chốt chọn phương án bỏ hẳn yêu cầu chụp ảnh, chấp nhận đánh đổi.

**Đã làm:**
1. Viết script một lần chuyển toàn bộ 59 dòng "Ảnh chụp màn hình" trong "Bảng cảnh AI" của 16 kịch bản sang "AI text-to-video" (kể cả 1 dòng trước đó ghi "Ảnh chụp màn hình (dựng trong CapCut/Canva)" — không phải ảnh chụp thật mà là bảng đồ hoạ, cũng chuyển luôn cho nhất quán).
2. Chạy `generate_motion_graphic.py` cho cả 16 video → dựng thêm 108 cảnh mới (tổng cộng, bao gồm cả cảnh cũ), 0 lỗi.
3. **Nâng cấp `pipeline/assemble.py` để hỗ trợ nhiều ảnh/1 cảnh** (đặt tên `NNa.png`, `NNb.png`...) trước khi nhận ra hướng đi mới không cần dùng tới tính năng này nữa cho kênh hiện tại — vẫn giữ lại vì hữu ích cho trường hợp nâng cấp sau này hoặc kênh khác muốn dùng ảnh thật.
4. Chạy `assemble.py` cho cả 16 video → **16/16 video đều ra `draft.mp4` thành công, không cần ảnh chụp màn hình nào** (video #1 dài 109.8s, các video khác 67-110s tuỳ độ dài kịch bản).
5. Gửi người dùng video #1 xem thử.
6. Nhân lúc quota TTS có mở lại 1 chút, tạo thêm được giọng Charon cho video #13 (giờ 13/16 xong), ráp lại video #13.
7. Cập nhật `CLAUDE.md` (mục "Giới hạn thật" — ghi rõ quyết định bỏ chụp ảnh và lý do, dặn không tự ý đề xuất lại), `strategy/00` + `05`, `framework/template/00` + `05` (mọi kênh mới sau này mặc định không cần chụp ảnh). Xoá `screenshot-checklist.md` và `pipeline/export_screenshot_checklist.py` (sinh ra ở phiên trước, giờ lỗi thời do đổi hướng).

**Kết quả:** giải quyết dứt điểm bức xúc của người dùng về việc phải tự thao tác tay — pipeline giờ chạy từ kịch bản → `draft.mp4` hoàn toàn tự động, 0 thao tác người dùng, cho toàn bộ 16 video. Đánh đổi đã được người dùng chấp nhận rõ ràng: mất cảnh demo giao diện phần mềm thật.

**Bài học ghi lại để không lặp lại:** khi gửi demo có phần placeholder (ảnh giả để test kỹ thuật), phải nói rõ ngay trong tin nhắn gửi kèm — đừng để người dùng tự phát hiện và hiểu lầm thành sản phẩm thật.

---

### Mốc #14 — 2026-09-26 — Chốt giọng Charon, sửa lỗi file mẫu, gộp khẩu hiệu, tạo lại 11/16 giọng đọc
**Diễn biến:** người dùng báo 3 file mẫu giọng nam gửi ở mốc #11 không mở được (Windows: `0xC00D36C4` "unsupported/corrupt"). Sau đó chọn giọng **Charon**, yêu cầu "tiếp tục".

**Đã làm:**
1. Kiểm tra 3 file mẫu (`voice_test_*.wav`): phần dữ liệu âm thanh thật vẫn còn nguyên (kiểm chứng bằng `ffmpeg -af volumedetect` → mean/max volume hợp lý, không phải im lặng/nhiễu), nhưng file bị ghi **thiếu hoàn toàn header RIFF/WAVE** — do script test giọng lúc đó (chạy nhanh, không qua `generate_voice.py`) ghi thẳng PCM thô, không bọc header như hàm `pcm_to_wav_bytes` chuẩn. Đã bọc lại header đúng cho cả 3 file (không gọi lại API, không tốn quota) và gửi lại — người dùng nghe được, chọn Charon.
2. Sửa `pipeline/generate_voice.py`: `--voice` mặc định `Kore` → `Charon`.
3. Viết script một lần (`insert_tagline.py`, không lưu vào repo — chỉ chạy 1 lần) để chèn đúng vị trí 2 câu khẩu hiệu thương hiệu (mục 5, `08-nhan-dien-thuong-hieu.md`) vào mục "Lời thoại thuần" của cả 16 file kịch bản: câu giới thiệu kênh chèn ngay sau dòng "xác nhận vấn đề + preview" (luôn là dòng nội dung thứ 2 trong mọi kịch bản — đã kiểm tra cấu trúc đồng nhất của cả 16 file trước khi chạy), câu kết cố định thêm vào cuối cùng (sau CTA). Đã dry-run kiểm tra trước khi áp dụng thật.
4. Tạo lại `voice.wav` video #1 bằng Charon + khẩu hiệu mới → gửi người dùng nghe (105 giây) → **xác nhận ổn, yêu cầu "tiếp tục"**.
5. Chạy hàng loạt cho video #2-16: **11/16 thành công (video #2-11)**, video #12-16 gặp `429 RESOURCE_EXHAUSTED` (hết quota 10/ngày cho `gemini-3.8-flash-lite-tts` — quota tính từ các lần gọi trước đó trong ngày, kể cả lúc test giọng). Không dùng model khác để né quota (giữ đúng nguyên tắc người dùng đã yêu cầu ở mốc #10: không tự đổi model/giọng để né lỗi).
6. Commit theo từng bước nhỏ (đổi default voice + tagline scripts + voice #1, rồi voice #2-11) để không mất tiến độ nếu phiên bị ngắt giữa chừng.

**Kết quả:** 11/16 video đã có giọng đọc chuẩn cuối cùng (Charon + khẩu hiệu thương hiệu). Còn 5 video (#12-16) chờ quota reset.

**Trong lúc chờ quota reset, tranh thủ làm luôn bumper thương hiệu (không tốn API):**
7. Tạo `channels/ai-de-dung/assets/_brand/intro-bumper.mp4` (chữ "AI DỄ DÙNG") và `outro-bumper.mp4` (icon CTA + "Cảm ơn đã xem, đăng ký kênh") bằng `generate_motion_graphic.py` — miễn phí, tức thời.
8. **Sửa `pipeline/assemble.py`: tự động ghép bumper mở/kết vào MỌI video** (không cần thao tác thủ công nữa) — phát hiện 2 file ở `assets/_brand/`, ghép làm cảnh đầu/cuối, và tự bù khoảng lặng vào audio (`adelay` cho đầu, `apad` cho cuối) để khớp đúng độ dài video mới thay vì bị cắt cụt bởi `-shortest`.
9. Test end-to-end bằng assets demo có sẵn của video #1 (ảnh chụp màn hình giả lập) → `draft.mp4` ra đúng 109.76s (= 105.8s giọng đọc + 2s + 2s bumper, khớp chính xác) → gửi người dùng xem duyệt phần bumper trước khi áp dụng chính thức.
10. Cập nhật `strategy/05` và `strategy/08` (mục 4) phản ánh việc ghép bumper giờ tự động, không còn là thao tác thủ công phải nhớ làm.

---

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
