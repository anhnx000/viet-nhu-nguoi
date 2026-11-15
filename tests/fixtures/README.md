# Bài mẫu để thử bộ kiểm tra

`ai-opus/`: 16 bài Claude Opus (mức medium) viết ngày 15/11/2026 theo đề bài thường gặp, không bật skill. Tên người, công ty, số liệu trong bài đều do mô hình tự nghĩ ra. Đây là bộ đã dùng để chỉnh các kiểm của bản 2.7.0.

`nguoi-viet/`: 6 đoạn văn xuôi đã thuộc về công chúng, lấy từ Wikisource tiếng Việt: Nam Cao (*Chí Phèo*, *Một bữa no*), Thạch Lam (*Gió lạnh đầu mùa*, bài về cốm trong *Hà Nội băm sáu phố phường*), Vũ Trọng Phụng (*Lục sì*, *Bụng trẻ con*).

`tests/test_scan.py` giữ khoảng cách giữa hai bộ: bài mô hình viết phải có trung bình từ 12 điểm, ít nhất 9 bài từ 10 điểm trở lên, còn bài người viết thì không bài nào tới 10. Sửa bộ kiểm tra mà test này hỏng thì xem lại trước khi nới ngưỡng.
