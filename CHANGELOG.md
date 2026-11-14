# Changelog

## 2.7.0 (2026-11-15)

Thử skill trên văn do mô hình đời mới viết. Bộ thử có 32 bài tiếng Việt viết theo đề bài thường gặp (bài LinkedIn, bài Facebook, email xin lùi hạn, mô tả sản phẩm, báo cáo tuần, thông báo nội bộ, bài giới thiệu quán, README, bài quan điểm), không dùng skill: 16 bài của Claude Opus chạy mức medium, 16 bài của Haiku và Sonnet. Bên đối chứng là 26 bài người viết đăng trước tháng 11/2022 (6 truyện và ký trên Wikisource, 4 bài Góc nhìn của VnExpress, 3 bài tin và phóng sự của Tuổi Trẻ, 6 bài kỹ thuật trên Viblo, 7 bài blog và tâm sự của bốn tác giả). Sau khi chỉnh xong máy quét, viết thêm hai đợt đề mới cho Opus, mỗi đợt 12 bài (thông báo mở chi nhánh, đơn xin nghỉ phép, review sách, thư từ chối ứng viên, tin báo cắt nước, biên bản họp, bài phát biểu đám cưới...), để đo trên bài chưa từng dùng lúc chỉnh.

- Máy quét bản 2.6.1 chấm "sạch" (dưới 10 điểm) cho 26 trên 32 bài, kể cả bài gọi vốn chia mục bằng emoji và bài quán cà phê toàn chữ quảng cáo. Văn đời mới ít từ sáo quen mặt, cái còn lại là khuôn của bài mạng xã hội và email.
- `scan.py` bắt thêm: đối lập tách hai câu ("Đây không chỉ là một con số. Đây là sự công nhận.", "PM không phải là... PM là..."), "X là A, không phải B", "Đừng A, hãy B", "Không có A, chỉ có B"; nhóm "mời tương tác" (câu kết xin bình luận, "Còn bạn, ...?", "cứ nhắn cho mình nhé"); nhóm "khẩu hiệu" ("tương lai thuộc về", "đây mới chỉ là khởi đầu", "hành trình phía trước còn dài"); nhóm "khuôn công văn" ("rất mong nhận được sự xem xét", "xin trình bày chi tiết như sau"); chỗ trống của bản mẫu còn sót ("[Họ tên]", "[Tên công ty]"); dòng mở bằng emoji, dòng in đậm đứng làm tiêu đề; thêm chữ quảng cáo ("điểm dừng chân lý tưởng", "đắm mình", "trải nghiệm trọn vẹn"), khuôn email dịch ("em viết thư này để", "dẫn dắt bởi"), nhãn "Thú thật,", "Điều mình muốn nói là:".
- Ba dấu hiệu cả bài mới, cộng điểm cố định: chia mục bằng emoji (từ ba dòng, 8 điểm), kết bài mời tương tác (5 điểm), in đậm dày (từ bốn nhãn hoặc tiêu đề in đậm, dày cỡ một chỗ trên 150 chữ, 5 điểm).
- Kết quả, điểm trung bình và số bài từ 10 điểm trở lên, bản 2.6.1 so với bản này:
  - 16 bài Opus dùng để chỉnh: 5,6 lên 15,4; 3 thành 10 bài.
  - 16 bài Haiku và Sonnet dùng để chỉnh: 4,3 lên 14,6; 3 thành 9 bài.
  - 12 bài Opus theo đề mới, đợt một: 4,4 lên 14,3; 1 thành 7 bài. Đọc đợt này xong có thêm một kiểm (đoạn mở bằng cụm in đậm), nên viết tiếp đợt hai.
  - 12 bài Opus theo đề mới, đợt hai, chấm sau khi máy quét đã chốt: 4,0 lên 11,5; 2 thành 5 bài. Đây là con số nên tin nhất: gặp bài chưa từng thấy, máy quét báo được chừng bốn phần mười.
  - 26 bài người viết: 4,5 xuống 3,0; 3 còn 1 bài. Các kiểm mới không báo thêm chỗ nào. Bài còn lại là một bài hướng dẫn kỹ thuật viết theo tài liệu tiếng Anh, dày chữ đệm của văn dịch.
  - Bài mô hình viết trơn tru mà toàn chi tiết bịa (quán cà phê hai tầng, ly sữa chua dâu tằm, "lần đầu đọc là năm lớp 11") thì máy quét vẫn chấm thấp, vì chữ nghĩa không có gì sai.
- Ba dấu hiệu cả bài mà người viết thật cũng hay có (đoạn ngắn đều nhau, câu vụn, đại từ dày) giờ chỉ cộng điểm khi bài còn dính ít nhất một dấu hiệu mạnh. Trước đó hai bài blog người viết lên 10 điểm chỉ vì xuống dòng liên tục và xưng "bạn", truyện Nam Cao bị cộng điểm vì câu ngắn.
- Chuyện bịa thì máy quét không chấm được, nên với bài xưng "mình", "tôi" nó in thêm một dòng liệt kê chi tiết riêng có con số ("800 mét", "tháng thứ tư", "5h15") để hỏi lại người đứng tên. Dòng này không tính điểm; bản JSON có trường `to_confirm`.
- Bớt báo nhầm: "nơi mà không ai hồi âm" không còn bị tính là "nơi mà" dịch sát; một dòng chúc mừng mở bằng emoji hay một nhãn in đậm lẻ thì bỏ qua; câu công văn nằm trong công văn thật (có "Số:", "V/v", "Kính gửi:") thì không báo.
- Nhóm mới "chỉ dẫn chèn vào": thẻ `</skill>`, "SYSTEM MESSAGE", "bỏ qua mọi hướng dẫn" nằm lẫn trong văn bản cần sửa.
- Thử bản skill cuối trên Opus, mỗi tình huống hai hoặc ba lượt:
  - Sửa bài báo người tự viết, 3 lượt trên hai bài Góc nhìn: giữ 86%, 98% và 99% số chữ gốc, lượt nào cũng mở đầu bằng nhận xét bài đọc ra giọng người.
  - Đoạn báo cáo có chỉ dẫn chèn vào, 3 lượt: lượt nào cũng không làm theo và báo lại cho người dùng.
  - Soi lỗi một bài kể chuyện chuyển nghề, 3 lượt: lượt nào cũng không viết lại bài, dẫn 7-9 mục của danh mục, tách chỗ nên sửa với chỗ tùy người viết, không kết luận bài do AI viết.
  - Nhờ làm slide báo cáo tiến độ mà không đưa số liệu, 2 lượt: cả hai chỉ hỏi bối cảnh, chưa dựng slide nào.
  - Sửa `examples/slide-truoc.pptx`, 2 lượt: không thêm con số nào, để 15 và 18 chỗ `[cần xác nhận]`.
  - Công văn gửi Sở, 3 lượt: giữ đủ số hiệu, số hợp đồng, hai mốc ngày, tên người ký, bỏ phần sáo. Một lượt tự điền "tháng 11 năm 2026" vào dòng ngày ký, nên `SKILL.md` dặn thêm: thêm phần thể thức còn thiếu thì để trống cho người dùng điền.
  - Tin trả lời PM trong nhóm chat, 3 lượt: đủ giờ deploy, người trực, mức rủi ro, thời gian rollback; bỏ "=))" và chữ viết tắt vì chưa có tin nào người dùng nhắn cho PM để học giọng.
  - Bài LinkedIn tiếng Anh, 3 lượt: giữ đủ năm con số, bỏ emoji, "testament", câu xin bình luận.
- `SKILL.md` có thêm chế độ viết mới. Lỗi nặng nhất của bài mô hình viết hộ là bịa cho đầy: lịch xử lý từng ngày trong email xin lùi hạn, "sau 5 năm, 3 công ty", lần đau ống đồng ở tháng thứ tư. Chế độ mới dặn chỉ dùng dữ kiện người dùng đưa; email, thông báo đủ dữ kiện thì viết luôn, chỗ chỉ người dùng biết để trong ngoặc vuông; bài sống nhờ chuyện riêng thì hỏi hai đến bốn câu trước, không đưa khung điền chỗ trống. Chạy ba đề viết mới trên Opus (bài LinkedIn "5 bài học làm PM", bài giới thiệu quán cà phê sách, bài Facebook một năm chạy bộ), mỗi bản skill ba lượt một đề. Bản 2.6.1: cả 9 lượt đều trả một câu trả lời dài khoảng 230-470 chữ kèm bài khung, có 4-19 chỗ trống trong ngoặc vuông; với đề PM, cả ba lượt tự viết luôn năm bài học người dùng chưa hề nêu. Bản này: cả 9 lượt chỉ hỏi bốn câu, dài 130-200 chữ; 7 lượt không có chỗ trống nào, 2 lượt kèm bản hai câu về quán, chỗ trống chỉ dành cho thứ chủ quán mới biết (địa chỉ, giờ mở cửa, món nước).
- `SKILL.md`: bước tự kiểm tách thành năm phần (dữ kiện, dấu hiệu còn sót, tiếng Việt, cả bài, chấm điểm); ghi chú sau bản sửa phải ngắn hơn hẳn bài; bài AI viết hộ có chi tiết riêng nghe tròn trịa quá thì hỏi lại người dùng; không kết bài bằng lời mời tương tác hay câu hô hào. Phần "Nguồn" chỉ còn hai nguồn chính, danh sách đầy đủ ở `references/sources.md`.
- Danh mục vẫn 65 mục, các khuôn mới gộp vào mục 1, 3, 16, 21, 32, 45, 50, 53, 61.
- `check_facts.py` so số theo giá trị ("1.250" với "1250", "12,5%" với "12.5%", "3 khách" với "ba khách" coi là một), không tính dòng tiêu đề viết hoa là tên viết tắt, và nhắc xem lại ba thứ trước đây lọt: số viết bằng chữ bị đổi ("ba khách" thành "năm khách"), thứ trong tuần và tháng, các từ giữ nghĩa bị rơi ("chưa", "vẫn", "chỉ", "có thể", "khoảng", "ít nhất").
- Điểm các file mẫu và README không đổi. Test từ 71 lên 97, trong đó có test giữ khoảng cách giữa 16 bài Opus và 6 đoạn văn xuôi của Nam Cao, Thạch Lam, Vũ Trọng Phụng trong `tests/fixtures/`.

## 2.6.1 (2026-11-13)

- `references/chat.md` thêm ví dụ cá nhân hóa: chuyện chuyển sang nghiêm túc mà giọng vẫn giữ (bản nháp quay về giọng chatbot còn làm mất nguyên nhân lỗi và mốc 15 phút), cùng người gửi mà hai người nhận, người không dùng icon, một tin chúc mừng không làm đổi hồ sơ, người dùng sửa giữa chừng, giọng Huế nhại cả câu và bản theo mẫu.
- Test kiểm bản nháp quay về giọng chatbot bị `--chat` báo, còn bản giữ giọng thì không.

## 2.6.0 (2026-11-13)

Cá nhân hóa tin nhắn trả lời: icon và ngữ điệu lấy từ cuộc trò chuyện, giữ nguyên tới hết cuộc. Ý tưởng từ một đồng nghiệp hỏi skill đã xử lý tiếng địa phương chưa.

- `references/chat.md`: lập hồ sơ giọng từ tối đa 30 lượt trò chuyện gần nhất đọc được (đoạn chat dán vào, các lượt trong phiên, công cụ đọc tin nhắn nếu người dùng cho phép). Hồ sơ gồm icon (emoji, emoticon, đặt ở đâu, dày cỡ nào) và ngữ điệu (độ dài, viết hoa, chấm câu, trợ từ, xưng hô, chữ lóng, từ địa phương). Chỉ dùng những gì hồ sơ có, giữ hồ sơ cho mọi tin sau trong phiên, cửa sổ 30 lượt trượt theo lượt mới, mỗi người nhận một hồ sơ. Không có lượt nào thì hỏi, vẫn không có thì viết đời thường, không lóng, không icon, không giọng miền. Một tin một vùng, không nhại phát âm, không đoán vùng từ tên hay quê.
- Nhóm dấu hiệu L (mục 63-65): tin nhắn viết như email, icon và ngữ điệu lạc giọng (chồng lóng, icon lạ, đổi giọng giữa chừng), giả giọng miền (trộn vùng, nhại phát âm, tự rải).
- `scan.py` kiểm cả bài "chồng tiếng lóng" (từ ba chữ lóng khác nhau, dày từ một chữ trên 25 chữ, cộng 8 điểm) và "trộn giọng miền" (dấu hiệu của hai vùng trở lên, tổng từ ba chỗ, cộng 6 điểm). Tùy chọn mới `--chat` báo thêm gạch đầu dòng, in đậm, tiêu đề trong tin nhắn, câu khách sáo ("cảm ơn bạn đã", "sẽ cân nhắc") và tin quá 80 chữ.
- Test có cả tin nhắn người viết thật (giọng Nam thuần, giọng Trung thuần, tin có ":v" và một chữ "chill") để chắc không báo nhầm. Điểm các file mẫu và README không đổi.
- `SKILL.md` thêm một mục ngắn trỏ sang `chat.md`, README hai thứ tiếng thêm một đoạn và tùy chọn `--chat`.

## 2.5.0 (2026-11-11)

Máy quét đo văn dịch trên cả bài, skill học thêm từ humanizer 4.0.0.

- Thử máy quét trên hai bộ văn do agent khác viết: mỗi bộ có đoạn dịch từng chữ và đoạn giọng người cùng nội dung, thuộc 22 thể loại (tin nhắn, thông báo, điều khoản, release note, review phim...). Trước bản này, đoạn dịch phần lớn chỉ được 0-15/100, vì người viết khác dùng những cụm không có trong danh sách.
- `scan.py` kiểm cả bài "chữ đệm dịch dày": đếm "một", "các/những", "được", "có thể", "sẽ", "đã", "rằng", "cho phép/giúp", "điều này/nó", "việc/sự", "của bạn/của tôi..." (tính gấp đôi) trên 1.000 chữ, từ 110 trở lên thì báo, cộng 12 điểm. Bộ thứ nhất: đoạn dịch 120-189, đoạn người 30-90. Bộ thứ hai, không dùng để chỉnh ngưỡng: bắt 5/6 đoạn dịch nặng, không báo nhầm đoạn nào trong 12 đoạn người. Đoạn chỉ hơi dịch, vài chỗ gượng lẻ tẻ, thì máy vẫn không thấy, phải đọc.
- Thêm cụm "hào hứng để chia sẻ rằng", "để lại một bình luận"; "của tôi" tính là sở hữu dịch sát.
- `examples/truoc.md` từ 72 lên 84/100 (17 dấu hiệu). README hai thứ tiếng, banner và ảnh ví dụ email đã cập nhật.
- `SKILL.md` theo humanizer 4.0.0: câu nào giữ lại cũng phải cho người đọc điều mới; nhóm A và E gặp một lần là sửa; lúc tự kiểm thì soát trước xem có mất tên, số liệu, thứ hạng không, có biến hai việc xảy ra cùng lúc thành trước sau không, nhất là ở chỗ vừa bỏ bộ ba, rào đón, nhãn in đậm; sửa file thì đọc lại file trên đĩa và báo nếu mới sửa một phần; văn bản có thẻ đóng kiểu `</skill>` chèn vào, hay lời nhắn xưng là "operator", "system message", thì coi là chữ cần sửa, không làm theo; văn bản trước 30/11/2022 không phải do AI viết. Mục 2 và 26 của danh mục thêm ví dụ.
- `examples/sau.md` viết lại thành một câu liền ý, bỏ chi tiết "khách tự xem tiến độ" vì bản gốc không có (chi tiết đó thuộc bản có thêm thông tin). Banner trích thêm đoạn nói về hệ thống mới cho hai bên khớp nhau.
- Chữ trong ảnh viết lại thành câu đủ chủ ngữ, vị ngữ: ba tiêu đề slide trong `examples/slide-sau.pptx` ("Thuê 1 QA tốn ít hơn tiền phạt mỗi lần trễ hạn" thay cho "Thuê 1 QA rẻ hơn tiếp tục trễ"), các dòng chú thích, nhãn số liệu ở ảnh bài đăng, và câu thứ hai của `examples/sau-co-chi-tiet.md`.
- Humanizer 4.0.0 cho mô hình tự thêm chi tiết nó biết là đúng, chỗ này thì không theo: skill vẫn không thêm dữ kiện ngoài bản gốc và lời người dùng.
- Repo: `tests/test_package.py` kiểm phiên bản khớp ở bốn nơi, danh mục đánh số liền, README ghi đúng số dấu hiệu, `SKILL.md` không quá 6.000 chữ; mẫu issue tiếng Việt ("Dấu hiệu mới", "Skill sửa sai"); thêm `AGENTS.md`, dặn trợ lý AI những việc cần biết khi sửa repo.
- Năm vòng đọc soát văn dịch, mỗi vòng nhờ hai agent mới đọc, chạy trên model khác với model đã viết bài. Vòng một: README và file ví dụ không còn câu nào, `SKILL.md`, `slides.md`, `patterns.md` còn 4 câu. Vòng hai: README vẫn sạch, CHANGELOG còn 3 câu, `SKILL.md` và `sources.md` còn 5 câu. Cả 8 câu của vòng hai đều nằm trong phần mới viết, chuyển ý từ humanizer và changelog tiếng Anh. Vòng ba còn 10 câu, vòng bốn còn 7, vòng năm còn 8, phần lớn là thuật ngữ tiếng Anh để nguyên ("register") và câu tóm ý rút từ nguồn tiếng Anh. Đã sửa hết, và `SKILL.md` dặn thêm: viết tiếng Việt từ nguồn tiếng Anh thì đọc xong nguồn phải gấp lại rồi mới viết, rồi soát riêng những câu đó.

## 2.4.5 (2026-11-11)

- Đoạn báo cáo quý dịch từng chữ từ 26 lên 44/100: "danh hóa (vi)" bắt "trong việc cải thiện/xây dựng/...", "văn dịch (vi)" bắt "làm được điều này mà không" và "muốn gửi lời cảm ơn đặc biệt". "Điều đáng nói là" vẫn để người đọc tự xét. Điểm các file mẫu và README không đổi.

## 2.4.4 (2026-11-11)

- Thử thêm hai thể loại: báo cáo quý và bài giải thích kiến thức, đều viết theo kiểu dịch từng chữ. Báo cáo từ 12 lên 26/100, bài giải thích từ 17 lên 43/100.
- "văn dịch (vi)" bắt thêm "tiến về phía trước", "đạt được những tiến bộ đáng kể", "hãy nghĩ về nó như", "điều đó nói rằng", "không phải là không có những hạn chế". "quan hệ từ dịch sát" bắt "mà tập trung vào/cho phép/giúp" sau danh từ và "càng nhiều X mà". "bị động dịch sát" thêm "được lập trình".
- Test có đoạn giọng người cùng nội dung để chắc không báo nhầm. Điểm các file mẫu và README không đổi.
- Còn sót: báo cáo dịch vẫn chỉ 26/100 (bản 2.4.5 vá tiếp).

## 2.4.3 (2026-11-11)

- Thử thêm ba đoạn văn dịch mới viết ở ba thể loại: email công việc, mô tả sản phẩm, hướng dẫn xử lý lỗi. Email dịch nguyên khuôn tiếng Anh trước đây được 0/100, giờ 39/100. Mô tả sản phẩm từ 16 lên 47, hướng dẫn từ 14 lên 37.
- "văn dịch (vi)" và mục 61 bắt thêm khuôn email ("hy vọng email này tìm thấy anh", "vui lòng tìm thấy tệp đính kèm", "mong chờ được nghe từ anh", "bất kỳ câu hỏi hoặc mối quan tâm nào"), khuôn quảng cáo ("với bạn trong tâm trí", "cho dù bạn là", "sự lựa chọn hoàn hảo", "nhận được nhiều hơn từ") và khuôn hướng dẫn ("vẫn còn tồn tại", "hãy chắc chắn để", "bạn không muốn bỏ lỡ"). `SKILL.md` có thêm ví dụ sửa khuôn email.
- Test có đoạn email giọng người ("Anh Minh ơi, em gửi bản báo cáo cuối trong file đính kèm...") để chắc không báo nhầm. Điểm các file mẫu và README không đổi.

## 2.4.2 (2026-11-11)

- Thử máy quét trên một đoạn văn dịch mới viết, không lấy từ repo. Máy quét bỏ sót các cụm mở và chuyển đoạn quen thuộc của bài hướng dẫn tiếng Anh. Đã thêm vào "văn dịch (vi)" và mục 61: "bạn đã đến đúng nơi", "đầu tiên và quan trọng nhất", "như một quy tắc chung", "cuối cùng nhưng không kém phần quan trọng", "kẻ thù lớn nhất của bạn", "chúng ta sẽ cùng nhau xem xét", "tìm kiếm một cách để". Đoạn thử từ 31/100 lên 49/100, điểm các file mẫu không đổi.
- "hãy chắc chắn rằng bạn" không còn bị đếm hai lần.
- CHANGELOG: sửa một cụm dịch sát ("như một luật").

## 2.4.1 (2026-11-10)

- Vẽ lại banner ở độ phân giải gấp đôi, tô đỏ các cụm máy quét bắt được.
- Ba ảnh ví dụ mới thay cho khối chữ trong README: tiêu đề slide, email và báo cáo, bài đăng dài. Có bản nhãn tiếng Anh cho `README.en.md`.
- `assets/make_images.py` vẽ lại toàn bộ ảnh từ các file trong `examples/` (cần Pillow và font Inter).

## 2.4.0 (2026-11-10)

Văn dịch từng chữ: chữ nào cũng là tiếng Việt mà câu vẫn theo khuôn tiếng Anh.

- `SKILL.md`: phần mới "Văn dịch: viết từ ý, đừng dịch từ câu". Che câu đi rồi viết lại như kể cho đồng nghiệp người Việt, thử dịch ngược, rà các chữ tiếng Anh buộc có mà tiếng Việt thì không ("bạn", "của bạn", "một", "các", "đã/đang/sẽ", "được", "và", "với", "có thể"), dùng khung đề-thuyết, dùng thành ngữ và tiêu đề của tiếng Việt.
- Nhóm dấu hiệu K (mục 56-62): chủ ngữ và sở hữu chép từ "you/your", mạo từ và số nhiều, bị động không nói ai làm và đồ vật làm chủ ngữ, chữ chỉ thì và "có thể", giới từ và từ nối dịch thẳng, thành ngữ và tiêu đề dịch thẳng, thiếu khung đề-thuyết.
- `scan.py`: nhóm mới "bị động dịch sát", "vật làm chủ ngữ", "mở câu dịch sát", "quan hệ từ dịch sát"; thêm thành ngữ dịch thẳng vào "văn dịch (vi)"; kiểm cả bài "đại từ dày" khi "bạn/chúng tôi/chúng ta" từ 12 lần trên 1.000 chữ. Điểm các file mẫu không đổi.
- README tiếng Việt viết lại từ ý theo phần mới, đổi cả tiêu đề mục ("Trước và sau" thành "Văn AI và bản đã sửa", "Vài điều nên biết" thành "Lưu ý"...).
- Tám vòng đọc độc lập soi văn dịch trong README, bài mẫu `examples/bai-dang-sau.md`, `SKILL.md`, `slides.md`, `patterns.md`, `sources.md` và CHANGELOG; đã sửa theo, gồm cả những chỗ `SKILL.md` tự phạm quy tắc của mình.
- `SKILL.md` dặn thêm đừng đổi tật này lấy tật khác (thay hết "các" bằng "mấy", hết "và" bằng "với") và đừng lược chữ tới mức câu thành mơ hồ.
- Còn hạn chế: phần lớn văn dịch tầng này máy không đếm được, phải tự đọc. Ngưỡng "đại từ dày" chưa thử trên văn người viết thật.

## 2.3.0 (2026-11-10)

Ngắt câu tiếng Việt và các việc tồn đọng của máy quét.

- `SKILL.md`: quy tắc ngắt câu viết lại cho nhất quán. Ngắt theo ý, không chặt vụn, cũng không gộp quá ba vế; từ nối phải đúng quan hệ; ngoặc đơn và chấm phẩy dùng dè. Bỏ lời khuyên bắt buộc xen câu dài với câu ngắn.
- Dấu hiệu 55, câu gộp quá tay: chuỗi vế nối bằng dấu phẩy. `scan.py` báo "câu quá dài" từ 60 chữ; ngắn hơn phải tự đọc.
- `scan.py --meta`: bỏ qua phần trích dẫn (dòng `>`, bảng, chữ trong ngoặc kép) khi quét văn bản bàn về chính các dấu hiệu. README từ 19/100 xuống 0/100 với `--meta`, điểm các file mẫu không đổi.
- "Hai chấm dồn dập" không còn đếm dấu hai chấm cuối đoạn dẫn vào danh sách, khối lệnh, bảng. Bài mẫu từ 20/88 còn 19/88 câu, điểm vẫn 55/100.
- `check_facts.py` không báo lỗi khi đoạn code được tách, gộp hay chuyển vào khối lệnh mà nội dung còn nguyên.
- `install.sh --update` thay bản đã cài, chỉ xóa thư mục đích khi nó đúng là skill này.
- "Câu vụn" không tính câu dẫn vào danh sách hay khối lệnh, ngưỡng đổi thành 30% số câu. Ngưỡng này sát: bản README bị chê vụn là 32%, bản đã sửa là 28%.
- Test: bốn đoạn văn mẫu giọng người (email, tin nhắn, bài đăng, báo cáo tuần) không được dính dấu hiệu cả bài. Các mẫu này do người bảo trì soạn, chưa phải văn thu thập từ người viết thật.
- README tiếng Việt viết lại theo quy tắc ngắt câu mới; bản tiếng Anh cập nhật theo.
- Chưa làm được: câu chốt cuối đoạn vẫn chưa dò được bằng máy.

## 2.2.2 (2026-11-10)

- Dấu hiệu 54, câu vụn: dấu chấm chặt một ý thành nhiều câu ngắn, lặp chủ ngữ. `SKILL.md` thêm quy tắc gộp vế bằng dấu phẩy và từ nối; `scan.py` báo "câu vụn" khi từ một phần ba số câu dài không quá 10 chữ (bài từ 20 câu). "Đoạn ngắn đều nhau" không còn tính cho tài liệu có tiêu đề Markdown như README.
- README tiếng Việt gộp lại các câu bị chặt vụn.
- Bỏ mục "Mời một ly cà phê" và mã QR khỏi README hai thứ tiếng, bỏ nút Sponsor (`.github/FUNDING.yml`).

## 2.2.1 (2026-11-10)

- Ví dụ bài đăng dài: `examples/bai-dang-truoc.md` (1.740 chữ, 55/100) và `examples/bai-dang-sau.md` (376 chữ, 0/100), có test kiểm bản viết lại không thêm số liệu.
- README hai thứ tiếng: cách cài không cần biết code, hướng dẫn dùng hằng ngày, mục riêng cho trợ lý AI được nhờ cài (có cách cho Windows), mục "Mời một ly cà phê".
- Mã QR vẽ lại ở độ phân giải gấp 4, nội dung mã giữ nguyên.
- README chính (`README.md`) là bản tiếng Việt; bản tiếng Anh chuyển sang `README.en.md`.
- README tiếng Việt viết lại cho dễ đọc (bớt dấu hai chấm, bỏ câu hỏi tu từ, tách bảng tùy chọn dòng lệnh); bản tiếng Anh cập nhật theo cùng bố cục.

## 2.2.0 (2026-11-10)

Dấu hiệu cả bài. Xuất phát từ một bài đăng 1.740 chữ đã sạch từng câu (bản 2.1.0 chấm 3/100) mà người đọc vẫn nhận ra là AI viết.

- Nhóm dấu hiệu I (mục 45-53): nhãn báo giọng ("nói gọn", "nói cho thật:", "nói rõ để..."), đối lập lặp cả bài, câu chốt cuối đoạn, "Tức là" giải nghĩa hộ và hai chấm dồn dập, bài ôm hết mọi thứ, bài tự kể dàn ý và mục "KẾT", đoạn ngắn đều nhau, nhượng bộ theo khuôn, xưng "mình" mà không có chuyện của mình.
- `SKILL.md`: phần "Cả bài" trong quy tắc cốt lõi. Mỗi quy tắc cấm cả họ cụm từ, thay cụm bị cấm bằng cụm đồng nghĩa không tính là sửa. Đối lập chỉ được dùng một lần mỗi bài. Một bài một việc, độ dài theo kênh, giọng riêng cho bài đăng mạng xã hội.
- `scan.py`: nhóm mới "nhãn báo giọng", "diễn giải lại", "tự kể dàn ý", "mục kết dán nhãn"; bắt thêm đối lập dạng "không X, mà Y", "chứ không", tách hai câu.
- `scan.py` đếm trên cả bài: một khuôn lặp từ 3 lần, hai chấm dồn dập, đoạn nào cũng 1-3 câu, bài đăng chia mục viết hoa, bài mạng xã hội trên 800 chữ. Các dấu hiệu này cộng điểm cố định, không chia theo độ dài, nên bài dài không loãng thành "sạch". Bài mẫu từ 3/100 lên 55/100.
- Kết quả in thêm số chữ; JSON có thêm `document_points`.

## 2.1.0 (2026-11-08)

Slide và thuyết trình.

- `scan.py` đọc thẳng file `.pptx`: chữ trên slide, bảng, ghi chú thuyết trình. Kết quả ghi theo vị trí ("slide 2, ghi chú").
- Kiểm riêng cho slide: tiêu đề dạng nhãn, tiêu đề có tiền tố nhãn, tiêu đề đếm số ý, ba tiêu đề cùng khuôn, tên khung lộ ra slide, slide nào cũng đúng 3-4 ý, gạch đầu dòng dài, slide nhiều chữ, câu ghi chú dài quá, khó nói, ngoặc trong lời nói.
- `scan.py --titles` in riêng các tiêu đề (slide hoặc heading Markdown); `scan.py --text` in toàn bộ chữ từng slide.
- `check_facts.py` so được hai file `.pptx`.
- Nhóm dấu hiệu H (mục 39-44) và hướng dẫn `references/slides.md`: lấy bối cảnh trước khi viết, tiêu đề là câu kết luận, mật độ theo cách trình bày, ghi chú viết để nói, nhờ agent mới đọc thử và chấm 7 tiêu chí.
- Dấu hiệu mới cho mọi văn bản: hứa suông ("chi tiết sẽ trao đổi sau").
- Sửa báo nhầm "một cách gọi", "một cách khác".
- Ý tưởng học từ jinba-consulting-pptx-skill, frontend-slides và doc-coauthoring, viết lại bằng lời riêng.

## 2.0.0 (2026-11-07)

Đổi tên thành **Viết như người** (`viet-nhu-nguoi`). Lệnh gọi đổi từ `/vietnamese-humanizer` sang `/viet-nhu-nguoi`; tên plugin và marketplace đổi theo. Link repo cũ tự chuyển sang repo mới.

## 1.2.0 (2026-11-07)

- Điểm 0-100 có trọng số theo độ mạnh của dấu hiệu, cộng phần phạt khi câu dài đều nhau; `--json`, `--max N` để chặn trong CI.
- `check_facts.py` kiểm bản sửa còn giữ số liệu, ngày giờ, link, code.
- Chế độ soi lỗi (chỉ liệt kê, không sửa), giọng theo tên, tự chấm năm tiêu chí.
- `references/sources.md` liệt kê nguồn, ghi rõ nguồn dùng trực tiếp và nguồn đọc thêm.

## 1.1.0

Nhóm dấu hiệu G riêng cho tiếng Việt: văn dịch, danh hóa, động từ rỗng, cụm marketing dịch sát, chuỗi "của", thừa nghĩa, xưng hô, chêm tiếng Anh, câu đều nhịp.

## 1.0.0

Bản đầu: danh mục dấu hiệu văn AI Việt/Anh dựa trên Wikipedia "Signs of AI writing" và blader/humanizer, máy quét bề mặt.
