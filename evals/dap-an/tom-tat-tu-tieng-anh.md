Mọi người ơi, ngày 2/12 mình phát hành bản 3.4.0. Có một việc cần lưu ý trước: API v1 cũ sẽ bị deprecate vào 31/3/2027, nên ai đang dùng v1 thì chuyển sang v2 trước ngày đó nhé.

Có gì mới:
- Export nhanh hơn tới 40% với workspace có trên 10.000 bản ghi.
- Thêm tính năng "Scheduled reports" (đang beta): admin đặt được lịch gửi báo cáo qua email theo tuần hoặc theo tháng, mỗi workspace tối đa 5 lịch. Workspace dùng gói Free thì chưa có tính năng này.

Lỗi đã sửa:
- Import file CSV trên 50 cột bị lỗi nhưng không báo gì.
- Audit log hiển thị sai múi giờ (lúc nào cũng hiện giờ UTC).