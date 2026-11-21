````markdown
---
title: Cài đặt kho-cli
version: 0.9.2
---

# Cài đặt

**kho-cli** là công cụ dòng lệnh giúp đội vận hành quản lý tồn kho.

Chạy hai lệnh sau để cài đặt và tạo cơ sở dữ liệu:

```bash
pip install kho-cli==0.9.2
kho init --db sqlite:///kho.db
```

Cài xong, cấu hình được lưu ở `~/.kho/config.toml`. Muốn đổi thiết lập thì sửa file này, ví dụ `max_rows = 500`.

Lưu ý: bản 0.9.2 chưa hỗ trợ PostgreSQL, chỉ chạy với SQLite và MySQL 8. Chi tiết xem tại https://example.com/kho-cli/docs.
````

Thay đổi chính: mình bỏ câu mở đầu về "bối cảnh hiện nay" và câu chúc ở cuối. Câu "không chỉ là… mà còn là người bạn đồng hành" giờ là một câu nói rõ công cụ làm gì. Các cụm như "thực hiện việc chạy", "được hoàn tất", "một cách linh hoạt" cũng đã gọn lại. Lệnh, đường dẫn, số phiên bản, danh sách cơ sở dữ liệu và link vẫn giữ nguyên.