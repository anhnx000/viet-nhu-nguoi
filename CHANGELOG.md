# Changelog

## 2.4.4 (2026-11-11)

- Thử thêm hai thể loại: báo cáo quý và bài giải thích kiến thức, đều viết theo kiểu dịch từng chữ. Báo cáo từ 12 lên 26/100, bài giải thích từ 17 lên 43/100.
- "văn dịch (vi)" bắt thêm "tiến về phía trước", "đạt được những tiến bộ đáng kể", "hãy nghĩ về nó như", "điều đó nói rằng", "không phải là không có những hạn chế". "quan hệ từ dịch sát" bắt "mà tập trung vào/cho phép/giúp" sau danh từ và "càng nhiều X mà". "bị động dịch sát" thêm "được lập trình".
- Test có đoạn giọng người cùng nội dung để chắc không báo nhầm. Điểm các file mẫu và README không đổi.
- Còn sót: báo cáo dịch vẫn chỉ 26/100. Câu kiểu "Điều đáng nói là", "gửi lời cảm ơn đặc biệt đến" cũng là cách nói quen của báo Việt nên không đưa vào máy quét.

## 2.4.3 (2026-11-11)

- Thử thêm ba đoạn văn dịch mới viết ở ba thể loại: email công việc, mô tả sản phẩm, hướng dẫn xử lý lỗi. Email dịch nguyên khuôn tiếng Anh trước đây được 0/100, giờ 39/100. Mô tả sản phẩm từ 16 lên 47, hướng dẫn từ 14 lên 37.
- "văn dịch (vi)" và mục 61 bắt thêm khuôn email ("hy vọng email này tìm thấy anh", "vui lòng tìm thấy tệp đính kèm", "mong chờ được nghe từ anh", "bất kỳ câu hỏi hoặc mối quan tâm nào"), khuôn quảng cáo ("với bạn trong tâm trí", "cho dù bạn là", "sự lựa chọn hoàn hảo", "nhận được nhiều hơn từ") và khuôn hướng dẫn ("vẫn còn tồn tại", "hãy chắc chắn để", "bạn không muốn bỏ lỡ"). `SKILL.md` có thêm ví dụ sửa khuôn email.
- Test có đoạn email giọng người ("Anh Minh ơi, em gửi bản báo cáo cuối trong file đính kèm...") để chắc không báo nhầm. Điểm các file mẫu và README không đổi.

## 2.4.2 (2026-11-11)

- Thử máy quét trên một đoạn văn dịch mới viết, không lấy từ repo. Máy quét bỏ sót các cụm mở và chuyển đoạn quen thuộc của bài hướng dẫn tiếng Anh. Đã thêm vào "văn dịch (vi)" và mục 61: "bạn đã đến đúng nơi", "đầu tiên và quan trọng nhất", "như một quy tắc chung", "cuối cùng nhưng không kém phần quan trọng", "kẻ thù lớn nhất của bạn", "chúng ta sẽ cùng nhau xem xét", "tìm kiếm một cách để". Đoạn thử từ 31/100 lên 49/100, điểm các file mẫu không đổi.
- "hãy chắc chắn rằng bạn" không còn bị đếm hai lần.
- CHANGELOG: sửa một cụm dịch sát ("như một luật").

## 2.4.1 (2026-11-10)

- Vẽ lại banner ở độ phân giải gấp đôi, tô đỏ các cụm máy quét bắt được.
- Ba ảnh ví dụ mới thay cho khối chữ trong README: tiêu đề slide, email và báo cáo, bài đăng dài. Có bản nhãn tiếng Anh cho `README.en.md`.
- `assets/make_images.py` vẽ lại toàn bộ ảnh từ các file trong `examples/` (cần Pillow và font Inter).

## 2.4.0 (2026-11-10)

Văn dịch từng chữ: chữ nào cũng là tiếng Việt mà câu vẫn theo khuôn tiếng Anh.

- `SKILL.md`: phần mới "Văn dịch: viết từ ý, đừng dịch từ câu". Che câu đi rồi viết lại như kể cho đồng nghiệp người Việt, thử dịch ngược, rà các chữ tiếng Anh buộc có mà tiếng Việt thì không ("bạn", "của bạn", "một", "các", "đã/đang/sẽ", "được", "và", "với", "có thể"), dùng khung đề-thuyết, dùng thành ngữ và tiêu đề của tiếng Việt.
- Nhóm dấu hiệu K (mục 56-62): chủ ngữ và sở hữu chép từ "you/your", mạo từ và số nhiều, bị động không ai làm và vật vô tri làm chủ ngữ, chữ chỉ thì và "có thể", giới từ và từ nối dịch thẳng, thành ngữ và tiêu đề dịch thẳng, thiếu khung đề-thuyết.
- `scan.py`: nhóm mới "bị động dịch sát", "vật làm chủ ngữ", "mở câu dịch sát", "quan hệ từ dịch sát"; thêm thành ngữ dịch thẳng vào "văn dịch (vi)"; kiểm cả bài "đại từ dày" khi "bạn/chúng tôi/chúng ta" từ 12 lần trên 1.000 chữ. Điểm các file mẫu không đổi.
- README tiếng Việt viết lại từ ý theo phần mới, đổi cả tiêu đề mục ("Trước và sau" thành "Văn AI và bản đã sửa", "Vài điều nên biết" thành "Lưu ý"...).
- Tám vòng đọc độc lập soi văn dịch trong README, bài mẫu `examples/bai-dang-sau.md`, `SKILL.md`, `slides.md`, `patterns.md`, `sources.md` và CHANGELOG; đã sửa theo, gồm cả những chỗ `SKILL.md` tự phạm quy tắc của mình.
- `SKILL.md` dặn thêm đừng đổi tật này lấy tật khác (thay hết "các" bằng "mấy", hết "và" bằng "với") và đừng lược chữ tới mức câu thành mơ hồ.
- Còn hạn chế: phần lớn văn dịch tầng này máy không đếm được, phải tự đọc. Ngưỡng "đại từ dày" chưa thử trên văn người viết thật.

## 2.3.0 (2026-11-10)

Ngắt câu tiếng Việt và các việc tồn đọng của máy quét.

- `SKILL.md`: quy tắc ngắt câu viết lại cho nhất quán. Ngắt theo ý, không chặt vụn, cũng không gộp quá ba vế; từ nối phải đúng quan hệ; ngoặc đơn và chấm phẩy dùng dè. Bỏ lời khuyên bắt buộc xen câu dài với câu ngắn.
- Dấu hiệu 55, câu gộp quá tay: chuỗi vế nối bằng dấu phẩy. `scan.py` báo "câu quá dài" từ 60 chữ; ngắn hơn phải tự đọc.
- `scan.py --meta`: bỏ qua phần trích dẫn (dòng `>`, bảng, chữ trong ngoặc kép) khi quét văn bản bàn về chính các dấu hiệu. README từ 19/100 xuống 0/100 với `--meta`, điểm các file mẫu không đổi.
- "Hai chấm dồn dập" không còn đếm dấu hai chấm cuối đoạn dẫn vào danh sách, khối lệnh, bảng. Bài mẫu từ 20/88 còn 19/88 câu, điểm vẫn 55/100.
- `check_facts.py` không báo lỗi khi đoạn code được tách, gộp hay chuyển vào khối lệnh mà nội dung còn nguyên.
- `install.sh --update` thay bản đã cài, chỉ xóa thư mục đích khi nó đúng là skill này.
- "Câu vụn" không tính câu dẫn vào danh sách hay khối lệnh, ngưỡng đổi thành 30% số câu. Ngưỡng này sát: bản README bị chê vụn là 32%, bản đã sửa là 28%.
- Test: bốn đoạn văn mẫu giọng người (email, tin nhắn, bài đăng, báo cáo tuần) không được dính dấu hiệu cả bài. Các mẫu này do người bảo trì soạn, chưa phải văn thu thập từ người viết thật.
- README tiếng Việt viết lại theo quy tắc ngắt câu mới; bản tiếng Anh cập nhật theo.
- Chưa làm được: câu chốt cuối đoạn vẫn chưa dò được bằng máy.

## 2.2.2 (2026-11-10)

- Dấu hiệu 54, câu vụn: dấu chấm chặt một ý thành nhiều câu ngắn, lặp chủ ngữ. `SKILL.md` thêm quy tắc gộp vế bằng dấu phẩy và từ nối; `scan.py` báo "câu vụn" khi từ một phần ba số câu dài không quá 10 chữ (bài từ 20 câu). "Đoạn ngắn đều nhau" không còn tính cho tài liệu có tiêu đề Markdown như README.
- README tiếng Việt gộp lại các câu bị chặt vụn.
- Bỏ mục "Mời một ly cà phê" và mã QR khỏi README hai thứ tiếng, bỏ nút Sponsor (`.github/FUNDING.yml`).

## 2.2.1 (2026-11-10)

- Ví dụ bài đăng dài: `examples/bai-dang-truoc.md` (1.740 chữ, 55/100) và `examples/bai-dang-sau.md` (376 chữ, 0/100), có test kiểm bản viết lại không thêm số liệu.
- README hai thứ tiếng: cách cài không cần biết code, hướng dẫn dùng hằng ngày, mục riêng cho trợ lý AI được nhờ cài (có cách cho Windows), mục "Mời một ly cà phê".
- Mã QR vẽ lại ở độ phân giải gấp 4, nội dung mã giữ nguyên.
- README chính (`README.md`) là bản tiếng Việt; bản tiếng Anh chuyển sang `README.en.md`.
- README tiếng Việt viết lại cho dễ đọc (bớt dấu hai chấm, bỏ câu hỏi tu từ, tách bảng tùy chọn dòng lệnh); bản tiếng Anh cập nhật theo cùng bố cục.

## 2.2.0 (2026-11-10)

Dấu hiệu cả bài. Xuất phát từ một bài đăng 1.740 chữ đã sạch từng câu (bản 2.1.0 chấm 3/100) mà người đọc vẫn nhận ra là AI viết.

- Nhóm dấu hiệu I (mục 45-53): nhãn báo giọng ("nói gọn", "nói cho thật:", "nói rõ để..."), đối lập lặp cả bài, câu chốt cuối đoạn, "Tức là" giải nghĩa hộ và hai chấm dồn dập, bài ôm hết mọi thứ, bài tự kể dàn ý và mục "KẾT", đoạn ngắn đều nhau, nhượng bộ theo khuôn, xưng "mình" mà không có chuyện của mình.
- `SKILL.md`: phần "Cả bài" trong quy tắc cốt lõi. Mỗi quy tắc cấm cả họ cụm từ, thay cụm bị cấm bằng cụm đồng nghĩa không tính là sửa. Đối lập chỉ được dùng một lần mỗi bài. Một bài một việc, độ dài theo kênh, giọng riêng cho bài đăng mạng xã hội.
- `scan.py`: nhóm mới "nhãn báo giọng", "diễn giải lại", "tự kể dàn ý", "mục kết dán nhãn"; bắt thêm đối lập dạng "không X, mà Y", "chứ không", tách hai câu.
- `scan.py` đếm trên cả bài: một khuôn lặp từ 3 lần, hai chấm dồn dập, đoạn nào cũng 1-3 câu, bài đăng chia mục viết hoa, bài mạng xã hội trên 800 chữ. Các dấu hiệu này cộng điểm cố định, không chia theo độ dài, nên bài dài không loãng thành "sạch". Bài mẫu từ 3/100 lên 55/100.
- Kết quả in thêm số chữ; JSON có thêm `document_points`.

## 2.1.0 (2026-11-08)

Slide và thuyết trình.

- `scan.py` đọc thẳng file `.pptx`: chữ trên slide, bảng, ghi chú thuyết trình. Kết quả ghi theo vị trí ("slide 2, ghi chú").
- Kiểm riêng cho slide: tiêu đề dạng nhãn, tiêu đề có tiền tố nhãn, tiêu đề đếm số ý, ba tiêu đề cùng khuôn, tên khung lộ ra slide, slide nào cũng đúng 3-4 ý, gạch đầu dòng dài, slide nhiều chữ, câu ghi chú dài quá, khó nói, ngoặc trong lời nói.
- `scan.py --titles` in riêng các tiêu đề (slide hoặc heading Markdown); `scan.py --text` in toàn bộ chữ từng slide.
- `check_facts.py` so được hai file `.pptx`.
- Nhóm dấu hiệu H (mục 39-44) và hướng dẫn `references/slides.md`: lấy bối cảnh trước khi viết, tiêu đề là câu kết luận, mật độ theo cách trình bày, ghi chú viết để nói, nhờ agent mới đọc thử và chấm 7 tiêu chí.
- Dấu hiệu mới cho mọi văn bản: hứa suông ("chi tiết sẽ trao đổi sau").
- Sửa báo nhầm "một cách gọi", "một cách khác".
- Ý tưởng học từ jinba-consulting-pptx-skill, frontend-slides và doc-coauthoring, viết lại bằng lời riêng.

## 2.0.0 (2026-11-07)

Đổi tên thành **Viết như người** (`viet-nhu-nguoi`). Lệnh gọi đổi từ `/vietnamese-humanizer` sang `/viet-nhu-nguoi`; tên plugin và marketplace đổi theo. Link repo cũ tự chuyển sang repo mới.

## 1.2.0 (2026-11-07)

- Điểm 0-100 có trọng số theo độ mạnh của dấu hiệu, cộng phần phạt khi câu dài đều nhau; `--json`, `--max N` để chặn trong CI.
- `check_facts.py` kiểm bản sửa còn giữ số liệu, ngày giờ, link, code.
- Chế độ soi lỗi (chỉ liệt kê, không sửa), giọng theo tên, tự chấm năm tiêu chí.
- `references/sources.md` liệt kê nguồn, ghi rõ nguồn dùng trực tiếp và nguồn đọc thêm.

## 1.1.0

Nhóm dấu hiệu G riêng cho tiếng Việt: văn dịch, danh hóa, động từ rỗng, cụm marketing dịch sát, chuỗi "của", thừa nghĩa, xưng hô, chêm tiếng Anh, câu đều nhịp.

## 1.0.0

Bản đầu: danh mục dấu hiệu văn AI Việt/Anh dựa trên Wikipedia "Signs of AI writing" và blader/humanizer, máy quét bề mặt.
