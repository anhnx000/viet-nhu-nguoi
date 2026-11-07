# Slide, lời thuyết trình và tài liệu dài

Đọc file này khi viết hoặc sửa slide, ghi chú thuyết trình, báo cáo hay đề xuất nhiều trang. Danh mục dấu hiệu nằm ở nhóm H (mục 39-44) trong `patterns.md`. Phần này nói cách làm.

Người xem nhận ra slide do AI làm từ trước khi đọc kỹ câu nào: nội dung đúng cho mọi công ty, mạch dựng sẵn, slide nào cũng giống slide nào. Vì vậy sửa từ ngữ thôi chưa đủ. Phải sửa từ bước lấy dữ liệu.

## 1. Trước khi viết: lấy đủ bối cảnh

Chưa biết ai xem, trong buổi nào, cần họ làm gì thì đừng dựng cả deck. Mỗi slide thêm vào là thêm một chỗ văn chung chung và một chỗ có thể sai. Hỏi trước, gộp thành một lượt:

1. Ai xem? Họ đã biết gì về chuyện này?
2. Xem xong, họ cần quyết gì hoặc làm gì?
3. Trình bày trực tiếp hay gửi cho người ta tự đọc?
4. Có mẫu slide, số liệu, tài liệu cũ, tin nhắn liên quan không?

Mời người dùng dán hết những gì họ có, chưa cần sắp xếp. Đọc xong thì hỏi thêm 5-10 câu đánh số về chỗ còn thiếu, và nói rõ họ trả lời tắt cũng được ("1: có, 2: xem file X, 3: chưa chốt"). Hỏi đủ khi đã có thể hỏi về các phương án và rủi ro mà không phải hỏi lại chuyện cơ bản. Nếu có công cụ đọc Teams, email, SharePoint thì đề nghị đọc thẳng từ đó, nhưng hỏi trước khi đọc.

Thiếu bối cảnh mà người dùng vẫn cần gấp: viết một trang tóm ý (kết luận, lý do, việc cần quyết) thay vì cả deck.

## 2. Viết mạch bằng tiêu đề trước

- Viết danh sách tiêu đề trước khi viết nội dung. Mỗi tiêu đề là một câu kết luận, có chủ ngữ và vị ngữ: "Quý 3 trễ 2 tuần vì thiếu người test", không phải "Thực trạng".
- Đọc liền các tiêu đề từ trên xuống: phải thành một lập luận, không nhảy, không lặp ý. Chạy `python3 -I scripts/scan.py --titles <file>` để in riêng các tiêu đề.
- Mỗi tiêu đề tự đứng được: không "như trên", "điều này", "giải pháp đó". Không gắn nhãn trước dấu hai chấm ("Kỳ vọng: ...", "Hướng xử lý: ..."); viết thẳng câu kết luận.
- Không đếm số ý trong tiêu đề ("3 trụ cột"). Gọi tên các ý. Nếu giữ con số thì nó phải khớp với nội dung slide.
- Ba tiêu đề liền nhau không mở bằng cùng một khuôn.
- Slide có biểu đồ hoặc bảng: tiêu đề nói số liệu đó có nghĩa gì với người xem.
- Thứ tự slide đi theo việc người xem cần quyết. Không mặc định "Tổng quan → Thách thức → Giải pháp → Lợi ích → Kết luận". Số vấn đề và số giải pháp đúng bằng số có thật, không ép về ba.
- Không in tên khung tư duy hay chữ của quy trình làm slide lên slide.

## 3. Nội dung từng slide

- Một slide, một thông điệp. Nhiều ý quá thì tách slide. Không thu nhỏ chữ để nhồi.
- Mật độ theo cách trình bày. Nói trực tiếp: 1-3 ý mỗi slide, chữ to, phần còn lại để trong lời nói. Gửi để đọc: 4-6 ý, mỗi slide tự hiểu được mà không cần người nói.
- Gạch đầu dòng: mỗi gạch một ý, một dòng, khoảng dưới 15 chữ. Mỗi gạch một góc khác nhau (tiền, thời gian, người, rủi ro), không nói lại cùng một ý. Cùng cấp thì cùng kiểu câu. Có một ý thì viết thành câu thường.
- Không bịa để lấp chỗ trống. Thiếu số liệu thì ghi `[cần xác nhận: ...]` và báo người dùng. Slide quá mỏng thì gộp với slide bên cạnh, đừng thêm ý cho đầy.
- Một sự việc, một cách gọi, một con số trong cả deck. Viết tắt thì lần đầu ghi đầy đủ.
- Từ đánh giá ("đáng kể", "hạn chế", "đủ", "tối ưu") phải có căn cứ ngay trên slide đó. Không có thì thay bằng con số hoặc bỏ.
- Nêu rủi ro thì nêu kèm cách xử lý. Slide xin quyết định ghi rõ cần quyết gì, phương án đề xuất, và hạn chót.
- Không hứa suông ("chi tiết sẽ trao đổi sau"). Viết luôn, hoặc ghi ai làm gì, khi nào.
- Báo cáo cho lãnh đạo: làm tròn số, thêm "khoảng"; giữ số chính xác ở phụ lục.

## 4. Ghi chú thuyết trình

- Viết để nói. Câu ngắn, mỗi câu một ý, người nghe hiểu ngay sau một lần nghe.
- Nói điều slide không ghi: vì sao, ví dụ, con số đằng sau. Không đọc lại chữ trên slide.
- Không ngoặc đơn, không "xem bảng ở trên", không mở bằng "Như chúng ta có thể thấy".
- Đọc thành tiếng một lần. Chỗ nào vấp thì sửa.
- Xưng hô hợp với người nghe và giữ suốt bài.

## 5. Hình thức cũng có "mùi AI"

Skill này lo phần chữ, nhưng khi được hỏi về hình thức thì nhắc các điểm sau:

- Emoji hoặc icon ở mọi tiêu đề, mọi gạch đầu dòng.
- Lưới thẻ icon lặp lại, nền gradient tím trên trắng, ảnh minh họa chung chung không nói lên nội dung.
- Bảng tô ba màu đèn giao thông, nhiều chỗ tô màu trên một slide. Một slide chỉ nên có một chỗ nhấn màu, và màu phải mang nghĩa.
- Cùng một bố cục lặp lại ba slide liền dù nội dung khác nhau.
- In đậm tràn lan.

Nên thay bằng biểu đồ vẽ từ số liệu thật, ảnh chụp màn hình sản phẩm, ảnh thật của đội, và mẫu slide của công ty.

## 6. Soát trước khi gửi

0. `python3 -I scripts/scan.py --text <file.pptx>`: in chữ từng slide kèm số slide, để đọc trước khi soi hay sửa.
1. `python3 -I scripts/scan.py <file.pptx>`: quét chữ trên slide, bảng và ghi chú. Kết quả ghi theo vị trí, ví dụ "slide 3, ghi chú". Ngoài các dấu hiệu chung, máy quét bắt thêm: tiêu đề dạng nhãn, tiêu đề có tiền tố nhãn, tiêu đề đếm số ý, gạch đầu dòng dài, slide nhiều chữ, slide nào cũng đúng 3-4 ý, ba tiêu đề cùng khuôn, tên khung lộ ra slide, câu ghi chú quá dài để nói, ngoặc trong lời nói.
2. `python3 -I scripts/scan.py --titles <file>`: đọc liền các tiêu đề.
3. Sửa xong một file `.pptx` có sẵn thì chạy `python3 -I scripts/check_facts.py goc.pptx moi.pptx` để chắc không mất hay tự thêm con số, ngày tháng, tên viết tắt.
4. Với deck hoặc tài liệu quan trọng, nhờ một người đọc mới đọc thử (mục 7).

Muốn sửa thẳng file `.pptx` thì dùng skill `pptx` nếu có. Nếu không có, trả bản sửa theo từng slide (tiêu đề, nội dung, ghi chú) để người dùng dán vào.

## 7. Nhờ người đọc mới đọc thử

Người viết không thấy được chỗ mình viết khó hiểu, vì trong đầu đã có sẵn bối cảnh. Nếu có công cụ gọi subagent, giao file cho một agent mới. Chỉ đưa đường dẫn file và lời dặn dưới đây, không kể deck được làm thế nào, dùng skill gì, hay chỗ nào mình đã cân nhắc kỹ:

> Bạn là người xem bộ slide (hoặc tài liệu) này lần đầu, không biết gì về cách nó được làm. Đọc hết file `<đường dẫn>`, không đọc file nào khác.
> 1. Viết tự do 3-10 điều khiến bạn khó hiểu, không tin, hoặc sẽ trả lại nếu bạn là người duyệt.
> 2. Chỉ đọc các tiêu đề từ trên xuống: chỗ nào nhảy ý, lặp ý, hoặc kết luận xuất hiện mà không có căn cứ?
> 3. Liệt kê kèm số slide và câu trích: con số mâu thuẫn giữa các slide; tiêu đề nói một đằng, nội dung hoặc biểu đồ nói một nẻo; từ đánh giá không có căn cứ ("đáng kể", "hạn chế", "đủ"); slide sau lặp lại slide trước; mục lục không khớp nội dung; câu tiếng Việt nghe lạ hoặc giống văn dịch.
> 4. Đoán 5 câu người xem sẽ hỏi, và trả lời từng câu chỉ bằng nội dung trong file. Câu nào không trả lời được thì ghi rõ.
> 5. Chấm 7 tiêu chí, mỗi tiêu chí 1-10, kèm một câu lý do: **mạch** (đọc liền tiêu đề có thành một lập luận không), **một thông điệp** (mỗi slide nói rõ một ý, không nhồi, không quá mỏng), **cấu trúc** (so sánh, nhân quả, số liệu có được trình bày bằng bảng, sơ đồ, biểu đồ hợp lý không), **dễ nhìn** (vài giây đầu có biết nhìn vào đâu không), **dùng được** (người xem có đủ căn cứ để quyết hay làm không), **nhất quán** (từ ngữ, con số, cách trình bày có khớp giữa các slide không), **trung thực** (số liệu có nguồn, có nói rõ giới hạn, có gây hiểu nhầm không). Ghi tổng điểm trên 70.
> 6. Kết bằng 5 việc nên sửa trước, xếp theo mức quan trọng, mỗi việc nói rõ sửa thế nào.
> Nêu ít nhất 3 điểm yếu. Không khen chung chung.

Điểm 70 chỉ để so bản trước với bản sau của cùng một deck, không dùng để so hai deck khác nhau. Không sửa theo mọi góp ý. Lập bảng nhận/không nhận và cho người dùng xem:

| # | Slide | Góp ý | Loại (câu chữ / lập luận / số liệu / hình thức) | Nhận? | Sửa thế nào / vì sao không sửa |
| --- | --- | --- | --- | --- | --- |

Góp ý làm đổi nghĩa hoặc đổi thứ tự lập luận thì để người dùng quyết. Sửa xong thì quét lại một lần.

Với tài liệu dài không phải slide (đề xuất, spec, báo cáo), dùng cùng cách: đoán câu hỏi của người đọc, đưa tài liệu cho agent mới trả lời, rồi xem nó hiểu sai ở đâu.
