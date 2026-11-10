# Changelog

## 2.2.1 (2026-11-10)

- Ví dụ bài đăng dài: `examples/bai-dang-truoc.md` (1.740 chữ, 55/100) và `examples/bai-dang-sau.md` (376 chữ, 0/100), có test kiểm bản viết lại không thêm số liệu.
- README hai thứ tiếng: cách cài không cần biết code, hướng dẫn dùng hằng ngày, mục riêng cho trợ lý AI được nhờ cài (có cách cho Windows), mục "Mời một ly cà phê".
- Mã QR vẽ lại ở độ phân giải gấp 4, nội dung mã giữ nguyên.
- README chính (`README.md`) là bản tiếng Việt; bản tiếng Anh chuyển sang `README.en.md`.
- README tiếng Việt viết lại cho dễ đọc (bớt dấu hai chấm, bỏ câu hỏi tu từ, tách bảng tùy chọn dòng lệnh); bản tiếng Anh cập nhật theo cùng bố cục.

## 2.2.0 (2026-11-10)

Dấu hiệu cả bài. Xuất phát từ một bài đăng 1.740 chữ đã sạch từng câu (bản 2.1.0 chấm 3/100) mà người đọc vẫn nhận ra là AI viết.

- Nhóm dấu hiệu I (mục 45-53): nhãn báo giọng ("nói gọn", "nói cho thật:", "nói rõ để..."), đối lập lặp cả bài, câu chốt cuối đoạn, "Tức là" giải nghĩa hộ và hai chấm dồn dập, bài ôm hết mọi thứ, bài tự kể dàn ý và mục "KẾT", đoạn ngắn đều nhau, nhượng bộ theo khuôn, xưng "mình" mà không có chuyện của mình.
- `SKILL.md`: phần "Cả bài" trong quy tắc cốt lõi. Mỗi quy tắc cấm cả họ cụm từ, thay cụm bị cấm bằng cụm đồng nghĩa không tính là sửa. Đối lập có ngân sách một lần mỗi bài. Một bài một việc, độ dài theo kênh, giọng riêng cho bài đăng mạng xã hội.
- `scan.py`: nhóm mới "nhãn báo giọng", "diễn giải lại", "tự kể dàn ý", "mục kết dán nhãn"; bắt thêm đối lập dạng "không X, mà Y", "chứ không", tách hai câu.
- `scan.py` đếm trên cả bài: một khuôn lặp từ 3 lần, hai chấm dồn dập, đoạn nào cũng 1-3 câu, bài đăng chia mục viết hoa, bài mạng xã hội trên 800 chữ. Các dấu hiệu này cộng điểm cố định, không chia theo độ dài, nên bài dài không loãng thành "sạch". Bài mẫu từ 3/100 lên 55/100.
- Kết quả in thêm số chữ; JSON có thêm `document_points`.

## 2.1.0 (2026-11-08)

Slide và thuyết trình.

- `scan.py` đọc thẳng file `.pptx`: chữ trên slide, bảng, ghi chú thuyết trình. Kết quả ghi theo vị trí ("slide 2, ghi chú").
- Kiểm riêng cho slide: tiêu đề dạng nhãn, tiêu đề có tiền tố nhãn, tiêu đề đếm số ý, ba tiêu đề cùng khuôn, tên khung lộ ra slide, slide nào cũng đúng 3-4 ý, gạch đầu dòng dài, slide nhiều chữ, câu ghi chú quá dài để nói, ngoặc trong lời nói.
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
