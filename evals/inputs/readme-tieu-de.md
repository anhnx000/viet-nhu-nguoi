# so-chi

Ghi chi tiêu hằng ngày từ dòng lệnh, xuất ra CSV để mở bằng Excel.

## Công cụ này làm được gì?

Gõ một dòng là ghi xong một khoản chi. Cuối tháng chạy `so-chi xuat --thang 10` là có file CSV chia theo từng nhóm.

## Cài thế nào

```bash
pip install so-chi==1.4.0
so-chi khoi-tao
```

Dữ liệu nằm trong `~/.so-chi/so.db`.

## Dữ liệu đi đâu, cấu hình nói gì

So-chi không gửi gì lên mạng. File cấu hình ở `~/.so-chi/config.toml`, mặc định `tien_te = "VND"`.

## Lệnh, tùy chọn, mẹo, lỗi hay gặp

`so-chi them 45000 an-sang` ghi một khoản. Thêm `--ngay 2026-10-03` để ghi cho ngày khác. Bản 1.4.0 chưa đọc được file Excel, chỉ xuất CSV.

## Good to know

Mã nguồn MIT, góp ý gửi qua issue.
