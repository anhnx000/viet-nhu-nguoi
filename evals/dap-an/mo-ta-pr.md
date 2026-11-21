Khi gọi API thanh toán bị timeout, client giờ sẽ thử lại tối đa 3 lần, mỗi lần cách nhau 2 giây. Trước đây chỉ cần timeout một lần là báo lỗi ngay cho người dùng.

- Sửa logic gọi API trong `payment/client.py`
- Thêm 4 test vào `tests/test_client.py`

Chưa làm: trường hợp cổng thanh toán trả về lỗi 5xx vẫn chưa được xử lý, sẽ làm ở PR sau.