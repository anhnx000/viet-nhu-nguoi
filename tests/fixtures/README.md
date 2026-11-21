# Bài mẫu để thử bộ kiểm tra

`ai-opus/`: 16 bài Claude Opus (mức medium) viết ngày 15/11/2026 theo đề bài thường gặp, không bật skill. Tên người, công ty, số liệu trong bài đều do mô hình tự nghĩ ra. Đây là bộ đã dùng để chỉnh các kiểm của bản 2.7.0.

`nguoi-viet/`: 6 đoạn văn xuôi đã thuộc về công chúng, lấy từ Wikisource tiếng Việt: Nam Cao (*Chí Phèo*, *Một bữa no*), Thạch Lam (*Gió lạnh đầu mùa*, bài về cốm trong *Hà Nội băm sáu phố phường*), Vũ Trọng Phụng (*Lục sì*, *Bụng trẻ con*).

`tests/test_scan.py` giữ khoảng cách giữa hai bộ: bài mô hình viết phải có trung bình từ 12 điểm, ít nhất 9 bài từ 10 điểm trở lên, còn bài người viết thì không bài nào tới 10. Sửa bộ kiểm tra mà test này hỏng thì xem lại trước khi nới ngưỡng.

Thêm văn người viết vào đây thì chỉ lấy văn đăng trước 11/2022 và được phép chép. Văn đã thuộc về công chúng, hoặc văn bản hành chính của cơ quan nhà nước mà Điều 15 Luật Sở hữu trí tuệ không bảo hộ quyền tác giả. Văn dưới CC BY-SA (Wikipedia, Wikibooks) thì để thư mục riêng, ghi tác giả và giấy phép. Tin báo và bài trên các bộ dữ liệu như trong `references/sources.md` thì chỉ đo ở máy, không chép vào repo.
