# Bộ đề thử skill

Bốn mươi lăm tình huống thường gặp, dùng để xem một bản `SKILL.md` mới có làm hỏng hành vi cũ không. Bộ đề này rút từ các lượt thử của bản 2.7.0, kết quả từng lượt ghi trong `CHANGELOG.md`.

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

Tám đề `spoken-*` thử sắc thái lời nói: trợ từ, phạm vi phủ định, mức chắc chắn, lời nhờ, bản chép lời, câu vốn tự nhiên không được sửa.

Bốn đề nhóm chat thử việc đổi giọng theo người nhận. `chat-cung-nhom-khac-vai` đưa sẵn mẫu cho bạn thân, trưởng nhóm lớn tuổi và cả nhóm. `chat-nhom-tra-loi-sep` và `chat-nhom-tra-loi-hai-nguoi` dùng một đoạn chat năm người, trong đó phần lớn tin của người dùng là giọng suồng sã với bạn, chỉ vài tin lễ phép với sếp và chị lớn tuổi hơn. Đọc tay ở các đề này là xem tin gửi người trên có lẫn "tui", "ông", ":v" của giọng bạn bè không.

## Kết quả bản 2.7.6

Bản này chưa có lượt nào chạy đủ 45 đề trên cùng một bản `SKILL.md`. Các đề chạy theo từng đợt trong lúc sửa, bằng hai mô hình (Claude và Codex), nên không gộp thành một tỉ lệ qua.

- Tám đề `spoken-*` chạy trên cả ba bản 2.7.1, 2.7.2, 2.7.3 và bản mới. Bản cũ đã giữ đúng ý ở cả tám đề, nên chưa có căn cứ nói bản mới hơn ở nhóm này.
- Đề giới thiệu quán chỉ có tên và địa điểm: cả ba bản cũ dựng bài có nhiều ô trống. Sau khi sửa, bốn đề thiếu dữ kiện (bài PM, chạy bộ, quán, studio) đều hỏi thêm, không dựng bài, mỗi đề một lượt.
- Nhóm chat: năm lượt Opus mức medium trên ba đề (`chat-nhom-tra-loi-sep` hai lượt, `chat-nhom-tra-loi-hai-nguoi` hai lượt, `chat-tra-loi-pm` một lượt) đều qua phần đếm và đúng vai khi đọc tay. Tin gửi sếp và chị lớn tuổi dùng "Dạ", "em", "ạ", phần gửi bạn giữ "ông". Hai lượt Codex về đổi người nhận giữa chừng và chưa rõ gửi cho ai cũng đúng.
- Lỗi còn thấy: mẫu giọng có gạch ngang thì lượt giữ lượt bỏ, tin chat có lúc chuẩn hóa dấu câu hơn mẫu, bài kể dài có lượt tự thêm một câu diễn giải ở đoạn kết dù đủ số liệu. Bài kể trải nghiệm vẫn cần người đứng tên đọc lại từng chi tiết.

`check.py` đổi hai chỗ: `min_questions` nhận cả câu hỏi không đánh số, `min_refs` nhận "Mục" viết hoa và danh sách số sau từ đó. `max_questions` vẫn chỉ đếm mục đánh số, vì dấu hỏi trong email soạn hộ có thể là lời nhờ người nhận.

Câu trả lời thô của các lượt chạy để ở máy người chạy (`evals/results/`, đã nằm trong `.gitignore`) vì log của công cụ có lẫn cấu hình máy.
