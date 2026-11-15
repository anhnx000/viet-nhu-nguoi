---
title: Cài đặt kho-cli
version: 0.9.2
---

# Cài đặt

Trong bối cảnh hiện nay, việc quản lý tồn kho một cách hiệu quả đóng vai trò then chốt đối với mọi doanh nghiệp. **kho-cli** không chỉ là một công cụ dòng lệnh, mà còn là người bạn đồng hành đáng tin cậy của đội vận hành.

Để tiến hành cài đặt, bạn cần thực hiện việc chạy lệnh sau đây:

```bash
pip install kho-cli==0.9.2
kho init --db sqlite:///kho.db
```

Sau khi việc cài đặt được hoàn tất, cấu hình sẽ được lưu tại `~/.kho/config.toml`. Điều này cho phép bạn có thể tùy chỉnh các thiết lập một cách linh hoạt — chẳng hạn như `max_rows = 500`.

Lưu ý: bản 0.9.2 chưa hỗ trợ PostgreSQL, chỉ chạy với SQLite và MySQL 8. Chi tiết xem tại https://example.com/kho-cli/docs.

Hy vọng hướng dẫn này hữu ích với bạn!
