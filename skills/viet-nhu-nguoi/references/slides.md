# Slide, lời thuyết trình và tài liệu dài

Đọc file này khi viết hoặc sửa slide, ghi chú thuyết trình, báo cáo hay đề xuất nhiều trang. Danh mục dấu hiệu nằm ở nhóm H (mục 39-44) trong `patterns.md`, còn file này nói cách làm.

Người xem nhận ra slide do AI làm từ trước khi đọc kỹ câu nào: nội dung gắn vào công ty nào cũng được, thứ tự trình bày theo khuôn có sẵn, các slide giống hệt nhau về bố cục. Vì vậy sửa từ ngữ thôi chưa đủ, phải sửa từ bước lấy dữ liệu.

## 1. Hỏi bối cảnh trước khi viết

Chưa biết ai xem, trong buổi nào, cần họ làm gì thì đừng dựng cả deck. Mỗi slide thêm vào là thêm một chỗ văn chung chung và một chỗ có thể sai. Hỏi trước, gộp thành một lượt:

1. Ai xem? Họ đã biết gì về chuyện này?
2. Xem xong, họ cần quyết gì hoặc làm gì?
3. Trình bày trực tiếp hay gửi cho người ta tự đọc?
4. Có mẫu slide, số liệu, tài liệu cũ, tin nhắn liên quan không?

Bảo người dùng cứ dán hết những gì đang có, chưa cần sắp xếp. Đọc xong thì hỏi thêm 5-10 câu đánh số về chỗ còn thiếu, và nói rõ họ trả lời tắt cũng được ("1: có, 2: xem file X, 3: chưa chốt"). Hỏi cho tới khi bàn được phương án và rủi ro mà không phải quay lại chuyện cơ bản thì thôi. Nếu có công cụ đọc Teams, email, SharePoint thì đề nghị đọc thẳng từ đó, nhưng hỏi trước khi đọc.

Thiếu bối cảnh mà người dùng vẫn cần gấp thì viết một trang tóm ý (kết luận, lý do, việc cần quyết) thay vì cả deck.

## 2. Dựng mạch bằng tiêu đề trước

- Viết danh sách tiêu đề trước khi viết nội dung. Mỗi tiêu đề là một câu kết luận, có chủ ngữ và vị ngữ: "Quý 3 trễ 2 tuần vì thiếu người test", không phải "Thực trạng".
- Đọc liền các tiêu đề từ trên xuống: phải thành một lập luận, không nhảy, không lặp ý. Chạy `python3 -I scripts/scan.py --titles <file>` để in riêng các tiêu đề.
- Tiêu đề nào đọc riêng cũng phải hiểu được: không "như trên", "điều này", "giải pháp đó". Không gắn nhãn trước dấu hai chấm ("Kỳ vọng: ...", "Hướng xử lý: ..."), viết thẳng câu kết luận.
- Không đếm số ý trong tiêu đề ("3 trụ cột"). Gọi tên các ý, còn nếu giữ con số thì nó phải khớp nội dung slide.
- Ba tiêu đề liền nhau không mở bằng cùng một khuôn.
- Slide có biểu đồ hoặc bảng: tiêu đề nói luôn người xem cần rút ra gì từ số liệu đó.
- Thứ tự slide đi theo việc người xem cần quyết. Không mặc định "Tổng quan → Thách thức → Giải pháp → Lợi ích → Kết luận". Số vấn đề và số giải pháp đúng bằng số có thật, không ép về ba.
- Tên khung lập luận dùng lúc dựng deck ("Situation", "Complication", "Resolution", "SCR") là để người làm slide dùng, không ghi lên slide.

## 3. Nội dung từng slide

- Một slide, một thông điệp. Nhiều ý quá thì tách slide, không thu nhỏ chữ để nhồi.
- Lượng chữ theo cách trình bày. Trình bày trực tiếp thì 1-3 ý mỗi slide, chữ to, phần còn lại để nói. Gửi cho người ta tự đọc thì 4-6 ý, slide nào đọc riêng cũng hiểu mà không cần người giảng.
- Gạch đầu dòng: mỗi gạch một ý, một dòng, không quá 15 chữ. Mỗi gạch một góc khác nhau (tiền, thời gian, người, rủi ro), không nói lại cùng một ý. Cùng cấp thì cùng kiểu câu. Có một ý thì viết thành câu thường.
- Không bịa để lấp chỗ trống. Thiếu số liệu thì ghi `[cần xác nhận: ...]` và báo người dùng. Slide quá mỏng thì gộp với slide bên cạnh, đừng thêm ý cho đầy.
- Trong cả deck, mỗi sự việc chỉ có một cách gọi và một con số. Viết tắt thì lần đầu ghi đầy đủ.
- Từ đánh giá ("đáng kể", "hạn chế", "đủ", "tối ưu") phải có căn cứ ngay trên slide đó. Không có thì thay bằng con số hoặc bỏ.
- Nêu rủi ro thì nêu kèm cách xử lý. Slide xin quyết định ghi rõ cần quyết gì, phương án đề xuất, hạn chót.
- Không hứa suông ("chi tiết sẽ trao đổi sau"). Viết luôn, hoặc ghi ai làm gì, khi nào.
- Báo cáo cho lãnh đạo: làm tròn số, thêm "khoảng", còn số chính xác để ở phụ lục.

## 4. Ghi chú thuyết trình

- Viết để nói: câu ngắn, mỗi câu một ý, nghe một lần là hiểu.
- Nói điều slide không ghi: vì sao, ví dụ, con số làm căn cứ. Không đọc lại chữ trên slide.
- Không ngoặc đơn, không "xem bảng ở trên", không mở bằng "Như chúng ta có thể thấy".
- Đọc thành tiếng một lần, chỗ nào vấp thì sửa.
- Xưng hô hợp với người nghe và giữ suốt bài.

## 5. Icon, màu và bố cục

Skill này lo phần chữ, nhưng có ai hỏi về hình thức thì nhắc mấy điểm sau:

- Emoji hoặc icon ở mọi tiêu đề, mọi gạch đầu dòng.
- Lưới thẻ icon lặp lại, nền trắng với gradient tím, ảnh minh họa chung chung không nói lên nội dung.
- Bảng tô ba màu đèn giao thông, nhiều chỗ tô màu trên một slide. Một slide chỉ nên có một chỗ nhấn màu, và màu nào cũng phải có nghĩa.
- Cùng một bố cục lặp lại ba slide liền dù nội dung khác nhau.
- In đậm tràn lan.

Nên thay bằng biểu đồ vẽ từ số liệu thật, ảnh chụp màn hình sản phẩm, ảnh thật của đội, mẫu slide của công ty.

Khi đã có file cần quét, dùng [cách soát file](slides-review.md).
