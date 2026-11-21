# Soát file trình chiếu

Chạy từ thư mục skill với file người dùng đưa.

| Cần xem gì | Lệnh |
|---|---|
| Chữ và ghi chú theo số slide | `python3 -I scripts/scan.py --text deck.pptx` |
| Mạch lập luận qua các tiêu đề | `python3 -I scripts/scan.py --titles deck.pptx` |
| Dấu hiệu trên từng slide, bảng, ghi chú | `python3 -I scripts/scan.py deck.pptx` |
| Dữ kiện mất hoặc tự thêm sau khi sửa | `python3 -I scripts/check_facts.py goc.pptx moi.pptx` |

Khi sửa thẳng PPTX, dùng công cụ biên tập trình chiếu nếu có. Nếu chỉ sửa được chữ, trả tiêu đề, nội dung và ghi chú theo từng slide để người dùng dán vào. Với deck hay đề xuất quan trọng cần người xem lần đầu, dùng [đề bài đọc thử](slides-reader.md).
