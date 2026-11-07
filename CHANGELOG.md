# Changelog

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
