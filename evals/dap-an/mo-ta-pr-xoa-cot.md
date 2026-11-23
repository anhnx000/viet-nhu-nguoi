Gộp hai cột `first_name` và `last_name` của bảng `customers` thành `full_name`.

- Migration 0042 chép dữ liệu sang `full_name` rồi xóa hai cột cũ.
- Trước khi sửa, 3 test trong `tests/test_customer.py` đỏ. Giờ cả bộ 128 test đều xanh.

Lưu ý khi merge:
- Migration này không lùi lại được: revert code không lấy lại hai cột đã xóa, muốn quay về phải khôi phục từ backup.
- API v1 vẫn trả `first_name` nên sẽ lỗi. Mình đã báo nhóm mobile.
