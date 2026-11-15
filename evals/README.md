# Bộ đề thử skill

Ba mươi tư tình huống thường gặp, dùng để xem một bản `SKILL.md` mới có làm hỏng hành vi cũ không. Bộ đề này rút từ các lượt thử của bản 2.7.0, kết quả từng lượt ghi trong `CHANGELOG.md`.

## Chạy một đề

Mỗi đề là một mục trong `scenarios.json`: `tin_nhan` là lời người dùng, `tep` (nếu có) là file đầu vào, `mong_doi` là điều một người đọc cần thấy trong câu trả lời, `kiem` là phần script đếm được.

1. Mở một phiên trợ lý mới, chưa biết gì về repo, và bật skill (hoặc dặn nó đọc `skills/viet-nhu-nguoi/SKILL.md` rồi làm theo).
2. Gửi đúng `tin_nhan` của đề, thay `{tep}` bằng đường dẫn tới file đầu vào.
3. Lưu nguyên văn câu trả lời vào `<thư mục kết quả>/<id>.md`.

Chạy đủ các đề rồi chấm:

```bash
python3 -I evals/check.py <thư mục kết quả>
```

Script báo từng đề qua hay trượt phần tự động. Sau đó đọc tay từng câu trả lời theo `mong_doi`, vì có những thứ script không đếm được: giọng có tự nhiên không, ghi chú có ngắn không, có chi tiết nào bịa không.

## Đọc kết quả

Mô hình trả lời mỗi lần một khác, nên một đề trượt một lượt thì đọc câu trả lời trước, rồi chạy lại vài lượt nếu cần. Lượt chạy đủ đầu tiên của bản 2.7.0 trên Claude Opus mức medium có 13 đề qua, ba đề còn lại trượt vì điều kiện chấm đặt quá chặt chứ câu trả lời thì đúng: viết "9h tối" thay cho "21h", dẫn số mục kiểu "(45, 3)" không kèm chữ "mục", để `[Họ tên]` chờ người dùng điền. Điều kiện đã nới theo ba chỗ đó, chấm lại thì cả 16 đề qua. Đề thứ mười bảy (một ý gửi ba người nhận) thêm sau, rút từ lần thử phần cá nhân hóa trên tin nhắn thật. Bản 2.7.1 gọt hai chỗ trùng lặp trong `SKILL.md` rồi chạy lại đủ 17 đề, cả 17 qua phần tự động và phần đọc tay. Chín đề cuối thêm ở bản 2.7.1 cho những phần chưa có đề nào thử: mẫu giọng có gạch ngang dài, giọng gọi tên, tài liệu kỹ thuật có code, tin viết từ nguồn tiếng Anh, daily report, mô tả PR, bài dài quá mức của kênh, yêu cầu qua máy dò AI, bài nộp cho trường. Lượt đầu cả chín đều qua, chạy thêm lượt hai (bốn đề cần phán đoán chạy cả lượt ba) cũng vậy. Riêng đề mẫu giọng, đọc tay thấy trợ lý hay tự thêm một câu cảm nghĩ, bản 2.7.2 đã sửa. Một tình huống thử tay mà không đưa vào bộ đề vì `check.py` chỉ đọc câu trả lời: nhờ sửa thẳng vào file có front matter và khối lệnh (file sửa xong còn nguyên code, link, phiên bản). Ba đề viết mới thiếu chuyện riêng là chỗ bản 2.6.1 trượt (trả bài khung có 4-19 chỗ trống thay vì hỏi lại).

Thêm đề mới thì thêm một mục vào `scenarios.json`. Điều kiện trong `kiem` nên lỏng vừa đủ: câu trả lời đúng mà viết khác đi một chút thì vẫn phải qua. Đừng đặt `must_not` cho cụm mà trợ lý có thể trích lại trong ghi chú ("mình đã bỏ câu ...").

Năm đề `chat-giong-*` thử phần cá nhân hóa trên năm giọng khác nhau (miền Tây, Nghệ An, sinh viên viết tắt, cô giáo viết trang trọng, dân văn phòng chêm tiếng Anh). Năm đoạn chat đó do một mô hình không bật skill viết, lời dặn thì cố ý xưng "tôi" và viết trang trọng để xem tin trả lời theo giọng mẫu hay theo giọng lời dặn. Lượt đầu cả năm đúng giọng mẫu.

Ba đề `luot-hai-*` thử lượt hai của chế độ viết mới: người dùng đã trả lời các câu skill hỏi, giờ skill phải viết bài từ đúng những gì họ kể. Phần đọc tay ở ba đề này là chỗ quan trọng nhất: bài có thêm cảnh, lời thoại hay cảm nghĩ nào người dùng chưa kể không.

File đầu vào trong `inputs/` là văn viết ra để thử, tên người và số liệu đều bịa.
