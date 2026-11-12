# Viết như người · Vietnamese Humanizer

**Chống giọng văn AI cho tiếng Việt. Nhờ AI viết mà đọc lên vẫn ra giọng mình.**

[![test](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Tiếng Việt** · [English](README.en.md)

![Trước: văn AI được 84/100. Sau: bản viết lại giọng người được 0/100.](assets/banner.png)

> **English:** a Claude skill that makes AI-drafted Vietnamese (and English) read like a person wrote it, without changing the facts. Read the [English README](README.en.md).
>
> *Viet nhu nguoi, chong giong van AI, human voice, Vietnamese humanizer, humanize tieng Viet, viet lai van AI tu nhien, bo giong ChatGPT.*

Nhờ AI làm slide, viết email, viết báo cáo thì nhanh thật, có điều ai đọc cũng nhận ra ngay. Slide nào cũng có tiêu đề "Tổng quan", "Thách thức". Email thì mở bằng "Trong bối cảnh hiện nay", kết bằng "Hy vọng thông tin trên hữu ích!". Gửi trong nhóm thì không sao, chứ gửi sếp hay gửi khách thì lại phải ngồi sửa.

Viết như người là một skill, tức là gói hướng dẫn cài thêm cho Claude và các trợ lý AI khác. Cài rồi thì AI viết tiếng Việt giống người đi làm hơn: tiêu đề slide nói thẳng kết luận, email xưng hô đúng vai, câu không rườm, số liệu đưa sao để vậy. Skill miễn phí, mã nguồn mở.

**Mục lục:** [Cài, không cần biết lập trình](#cài-mất-vài-phút-không-cần-biết-lập-trình) · [Cách dùng hằng ngày](#cách-dùng-hằng-ngày) · [Văn AI và bản đã sửa](#văn-ai-và-bản-đã-sửa) · [Skill sửa những lỗi nào](#skill-sửa-những-lỗi-nào) · [Dòng lệnh](#chạy-bằng-dòng-lệnh)

## Dùng vào việc gì

- Làm slide báo cáo, đề xuất. Tiêu đề nào cũng là câu kết luận, sếp lướt qua tiêu đề là biết cần quyết gì. Chỗ nào thiếu số liệu thì skill ghi `[cần xác nhận]`, không bịa cho đầy.
- Viết email gửi sếp, gửi khách. Email vào việc trước, xưng hô đúng vai (anh/chị/em, quý khách), không tự đổi thành "bạn".
- Sửa báo cáo, tài liệu dịch từ tiếng Anh, bỏ mấy kiểu câu dịch như "được... bởi", "Điều này cho phép", "thông qua việc".
- Viết bài Facebook, LinkedIn, blog. AI viết nháp nhưng vẫn ra giọng bạn, mỗi bài kể một chuyện thôi.
- Soi lại bài trước khi gửi. Skill chỉ ra chỗ nào nghe giống AI, còn sửa hay không là tùy bạn.

## Cài mất vài phút, không cần biết lập trình

Không phải gõ lệnh gì cả, cứ nhờ trợ lý AI cài hộ, như nhờ bạn IT ngồi cạnh.

**Bước 1. Mở trợ lý AI chạy trên máy tính.** Chẳng hạn ứng dụng Claude Code bản cho máy tính, dùng chuột như phần mềm bình thường. Codex, Cursor, Gemini CLI, OpenCode cũng được, còn Claude hay ChatGPT mở trên trình duyệt thì không cài được gì vào máy.

**Bước 2. Dán câu này vào ô chat:**

> Cài giúp tôi skill viet-nhu-nguoi từ https://github.com/anhnx000/viet-nhu-nguoi

**Bước 3. Bấm đồng ý** khi trợ lý xin phép tải và cài. Thường chưa tới một phút là xong.

**Bước 4. Mở cuộc trò chuyện mới rồi thử:**

> Viết như người: soạn giúp tôi email xin sếp lùi hạn nộp báo cáo 3 ngày, xưng em

Email trả về mà ngắn, vào việc ngay, xưng "em" từ đầu tới cuối là skill chạy rồi.

Về sau cần gì cũng cứ nói với trợ lý.

| Muốn | Gõ |
| --- | --- |
| Kiểm tra đã cài chưa | "Máy tôi có skill viet-nhu-nguoi chưa?" |
| Lấy bản mới | "Cập nhật skill viet-nhu-nguoi lên bản mới nhất" |
| Gỡ ra | "Gỡ skill viet-nhu-nguoi khỏi máy" |

Lúc cài mà trợ lý báo lỗi thì chụp màn hình rồi [mở issue](https://github.com/anhnx000/viet-nhu-nguoi/issues) (trang báo lỗi của dự án), mình xem giúp.

<details>
<summary>Dành cho trợ lý AI được nhờ cài skill này</summary>

Người nhờ cài không rành kỹ thuật, nên hãy tự làm hết, chỉ xin phép lúc cần chạy lệnh. Thử lần lượt, cách nào chạy được thì dừng ở đó:

1. Máy có `npx`: chạy `npx skills add anhnx000/viet-nhu-nguoi -g -y`.
2. Máy có `git` và `bash` (macOS, Linux, WSL): `git clone https://github.com/anhnx000/viet-nhu-nguoi.git ~/viet-nhu-nguoi && bash ~/viet-nhu-nguoi/install.sh --copy`.
3. Windows không có bash, hoặc không có git: tải `https://github.com/anhnx000/viet-nhu-nguoi/archive/refs/heads/main.zip`, giải nén, rồi chép thư mục `skills/viet-nhu-nguoi` vào thư mục skill cấp người dùng của agent (Claude Code: `~/.claude/skills/viet-nhu-nguoi`, trên Windows là `%USERPROFILE%\.claude\skills\viet-nhu-nguoi`).

Cài xong thì kiểm tra xem file `SKILL.md` đã nằm đúng thư mục đích chưa, rồi báo đường dẫn cho người dùng. Skill chưa hiện thì nhắc họ mở cuộc trò chuyện mới.

Cập nhật thì cài cách nào làm lại cách đó. Cách 2: chạy `git -C ~/viet-nhu-nguoi pull` rồi `bash ~/viet-nhu-nguoi/install.sh --copy --update`. Cách 3: xóa thư mục cũ rồi mới chép bản mới. Gỡ thì xóa thư mục `viet-nhu-nguoi` trong thư mục skill.

</details>

<details>
<summary>Dành cho người quen dòng lệnh: tự gõ lệnh cài</summary>

Trong Claude Code thì cài như plugin:

```text
/plugin marketplace add anhnx000/viet-nhu-nguoi
/plugin install viet-nhu-nguoi@viet-nhu-nguoi
```

Hoặc clone về rồi chạy script. Script tạo symlink vào `~/.claude/skills/`, về sau `git pull` là có bản mới:

```bash
git clone https://github.com/anhnx000/viet-nhu-nguoi.git
cd viet-nhu-nguoi
bash install.sh                   # symlink
bash install.sh --copy            # hoặc chép file, nếu muốn đọc lại từng bản cập nhật trước khi cài
bash install.sh --copy --update   # thay bản đã chép bằng bản mới
```

Agent khác (Cursor, Codex, Gemini CLI, OpenCode...) thì cài bằng công cụ [skills](https://github.com/vercel-labs/skills):

```bash
npx skills add anhnx000/viet-nhu-nguoi      # chỉ cho dự án hiện tại
npx skills add anhnx000/viet-nhu-nguoi -g   # cho mọi dự án (cấp người dùng)
```

Lệnh hỏi cài cho agent nào, muốn khỏi hỏi thì thêm `-a claude-code` (hoặc `-a '*'`) và `-y`. Skill chỉ gồm file Markdown nên editor đang dùng mô hình nào cũng chạy được.

</details>

## Cách dùng hằng ngày

Cứ nói như nhờ đồng nghiệp, không có cú pháp gì phải nhớ.

| Gõ thế này | Skill làm gì |
| --- | --- |
| "Làm slide báo cáo tiến độ dự án tuần này để sếp duyệt" | Hỏi trước ai xem, cần họ quyết gì, trình bày trực tiếp hay gửi đọc, hỏi xong mới dựng slide |
| "Sửa file bao-cao-q3.pptx cho bớt giọng AI" | Đọc chữ và ghi chú từng slide, sửa tiêu đề, gạch đầu dòng, lời thuyết trình |
| "Viết email xin sếp lùi deadline 3 ngày, xưng em" | Viết email ngắn, nói việc trước, giữ đúng "em"/"anh" từ đầu tới cuối |
| "Viết bài Facebook kể về dự án của mình, khoảng 300 chữ" | Hỏi một hai chuyện có thật rồi kể đúng một chuyện, không chia mục, không giảng lại kiến thức nền |
| "Soi giúp đoạn này chỗ nào giọng AI" | Chỉ ra từng chỗ kèm lý do và gợi ý sửa, không tự sửa |
| Dán kèm một email tự viết | Học nhịp câu, từ nối, cách xưng hô trong đó rồi viết theo |

Muốn skill viết sát ý hơn thì:

1. Nói rõ ai đọc, bạn với họ vai vế thế nào. "Gửi chị trưởng phòng, xưng em" ra email khác hẳn "gửi khách hàng, xưng chúng tôi".
2. Dán một đoạn tự viết, cùng loại với bài sắp viết, để skill bắt chước độ dài câu và chữ hay dùng.
3. Số liệu, tên, ngày tháng thì đưa số thật, tên thật. Thiếu chỗ nào skill hỏi lại hoặc để trống, không tự nghĩ ra.
4. Thấy chỗ nào lạ thì bảo "mình không nói thế". Skill đổi theo và nhớ tới hết cuộc trò chuyện.

Còn vài cách dùng nữa:

- Gõ `/viet-nhu-nguoi` để bật cho cả cuộc trò chuyện. Từ đó câu trả lời nào cũng theo quy tắc của skill, kể cả tin nhắn ngắn.
- Nhờ soạn email, tin nhắn, bài đăng mà bạn đứng tên gửi thì skill tự bật.
- Muốn giọng nào thì gọi tên giọng đó: *đời thường*, *công việc*, *kỹ thuật*, *ấm áp*, *thẳng*. Đổi giọng thì chỉ văn phong đổi, còn xưng hô và nội dung vẫn giữ nguyên.
- Bài tự viết thì skill chỉ sửa nhẹ.
- Bộ slide nào quan trọng thì skill nhờ thêm một trợ lý AI khác, chưa biết gì về bối cảnh, đọc thử rồi chấm 7 tiêu chí trên thang 70 điểm. Skill xếp góp ý thành bảng, nhận mục nào bỏ mục nào tùy bạn.

## Văn AI và bản đã sửa

Điểm ở dưới là do máy quét kèm theo skill chấm, thang 0-100, bài càng viết theo khuôn thì điểm càng cao.

### Slide

Thư mục [`examples/`](examples) có hai bộ slide mẫu, một bộ AI làm và một bộ làm theo skill. Đây là tiêu đề của hai bộ:

![Tiêu đề slide. Bộ AI làm, 48/100: Chuyển đổi số: Hành trình kiến tạo giá trị; Tổng quan; Thách thức; 3 trụ cột giải pháp; Lợi ích; Kết luận; Cảm ơn. Bộ làm theo skill, 0/100: Đề xuất thuê thêm 1 QA cho quý 1/2027; Hai bản phát hành quý 3 đều trễ vì thiếu người test; Thuê 1 QA tốn ít hơn tiền phạt mỗi lần trễ hạn; Cần anh duyệt trước 30/11 để kịp tuyển người.](assets/vi-du-slide.png)

Bộ sau chỉ đọc bốn tiêu đề là hiểu cả đề xuất. Máy quét chấm bộ này 0/100, bộ đầu 48/100.

### Email, báo cáo

![Email, báo cáo. Bản AI viết, 84/100, mở bằng "Trong bối cảnh hiện nay" và kết bằng "Hy vọng những thông tin trên sẽ hữu ích cho bạn!". Qua skill, 0/100: Đội mình đã chuyển sang hệ thống quản lý dự án mới, nên giờ theo dõi dự án nhanh và đỡ vất vả hơn, khách hàng làm việc với đội cũng thuận tiện hơn trước. Có thêm chi tiết, 0/100: Từ tháng 3, đội mình chuyển việc theo dõi dự án sang hệ thống mới.](assets/vi-du-email.png)

Bản AI viết bị chấm 84/100, dính 17 dấu hiệu, là những chỗ tô đỏ trong ảnh. Bản qua skill ngắn vì skill không bịa số liệu. Cần thêm chi tiết thì skill hỏi lại, bạn đưa gì skill viết nấy, như bản thứ ba. Hai bản sau đều được 0/100. Ba đoạn văn này nằm ở [`examples/truoc.md`](examples/truoc.md), [`examples/sau.md`](examples/sau.md) và [`examples/sau-co-chi-tiet.md`](examples/sau-co-chi-tiet.md).

### Bài đăng dài

Bản 2.2 của skill ra đời từ một bài đăng thật. [Bài gốc](examples/bai-dang-truoc.md) dài 1.740 chữ, chia thành chín mục có tiêu đề viết hoa. Bài gần như không còn từ AI quen mặt nên máy quét ở bản trước chỉ chấm 3/100. Vậy mà ai đọc cũng nhận ra, vì cả bài cứ lặp đi lặp lại vài kiểu câu.

![Bài đăng dài. Bài gốc, 55/100: 1.740 chữ, mười câu kiểu "không phải X mà là Y", sáu câu mở bằng nhãn, 19 trên 88 câu có dấu hai chấm. Bản viết lại, 0/100: 373 chữ, chỉ làm một việc là rủ người vào làm cùng.](assets/vi-du-bai-dang.png)

Từ bản 2.2 máy quét đếm trên cả bài nên bài này lên 55/100. Trong bài có mười câu kiểu "không phải X mà là Y", sáu câu mở bằng nhãn như "nói gọn", "nói cho thật", và 19 trên 88 câu có dấu hai chấm.

[Bản viết lại](examples/bai-dang-sau.md) còn 373 chữ, chỉ làm một việc là rủ người vào làm cùng. Máy quét chấm 0/100, không thêm dữ kiện nào ngoài bài gốc. Phần định nghĩa hệ điều hành, lịch sử microkernel, thống kê bảo mật thì để dành cho bài khác.

## Skill sửa những lỗi nào

Danh mục của skill có 65 dấu hiệu văn AI, dấu hiệu nào cũng kèm ví dụ trước và sau khi sửa ([xem đầy đủ](skills/viet-nhu-nguoi/references/patterns.md)). Nhóm riêng cho tiếng Việt có mấy dấu hiệu dễ thấy như bảng dưới:

| Dấu hiệu | Ví dụ | Sửa thành |
| --- | --- | --- |
| Bị động kiểu dịch | được phát triển bởi Google | Google phát triển |
| "Điều này", "Nó" mở câu | Điều này cho phép người dùng... | gọi tên sự vật, hoặc lược chủ ngữ |
| Danh hóa | Việc áp dụng AI giúp việc quản lý trở nên dễ dàng | Dùng AI thì quản lý dễ hơn |
| Động từ rỗng | tiến hành thực hiện việc rà soát | rà soát |
| Cụm marketing dịch sát | mở khóa tiềm năng, trải nghiệm liền mạch | nói cụ thể làm được gì |
| Chuỗi "của" | sự nâng cao của năng suất của nhân viên | nhân viên làm được nhiều hơn |
| Thừa nghĩa | hiện nay đang trong quá trình | đang |
| Xưng hô | cả bài "bạn" gửi sếp, trộn "bạn"/"quý vị" | một cặp xưng hô đúng vai |
| Chêm tiếng Anh | hiệu suất (performance) | hiệu suất |

Khó thấy hơn là văn dịch từng chữ: chữ nào cũng là tiếng Việt mà câu vẫn theo khuôn tiếng Anh. Kiểu này hay lộ ở mấy chỗ:

- câu nào cũng mở bằng "Bạn", danh từ nào cũng kèm "của bạn";
- "một", "các", "những" đứng trước mọi danh từ;
- bị động không nói ai làm ("số liệu được giữ nguyên"), đồ vật làm chủ ngữ ("Bảng này cho thấy");
- "đã", "đang", "sẽ", "có thể" rải khắp bài;
- "Với...", "Để..., bạn cần..." mở câu, "và" nối mọi vế;
- thành ngữ và tiêu đề dịch thẳng ("tin tốt là", "Bắt đầu nhanh").

Gặp văn như vậy, skill không thay từng cụm mà viết lại từ ý, như người Việt vẫn nói.

Có dấu hiệu phải đọc cả bài mới thấy, dù từng câu đã ổn:

- câu mở bằng nhãn ("nói gọn", "nói cho thật:");
- kiểu "không phải X mà là Y" lặp từ ba lần;
- đoạn nào cũng kết bằng một câu nghe như châm ngôn;
- dấu hai chấm dày đặc;
- cả bài dày những chữ đệm của văn dịch như "một", "các", "được", "sẽ", "của bạn";
- dấu chấm chặt một ý thành nhiều câu vụn, hoặc ngược lại, một câu gộp quá nhiều vế;
- bài đăng dài ôm đủ mọi chủ đề.

Slide và tài liệu nhiều trang có nhóm riêng: tiêu đề chỉ là nhãn ("Tổng quan", "Kết luận"), tiêu đề đếm số ý ("3 trụ cột"), slide nào cũng đúng ba ý, hứa suông ("chi tiết sẽ trao đổi sau"), ghi chú thuyết trình viết như công văn. Cách viết slide có hướng dẫn riêng ở [references/slides.md](skills/viet-nhu-nguoi/references/slides.md).

Tin nhắn trả lời thì skill cá nhân hóa icon và ngữ điệu. Skill đọc tối đa 30 lượt trò chuyện gần nhất mà nó truy cập được, học cách bạn viết hoa, chấm câu, cười (":v", ")))"), dùng emoji, trợ từ, xưng hô, rồi giữ đúng giọng đó cho mọi tin sau trong cuộc trò chuyện. Tiếng lóng hay giọng miền chỉ dùng khi các lượt đó có, hoặc khi bạn nói rõ muốn giọng vùng nào. Bản nháp nào dồn ba bốn chữ lóng vào một tin ("u là trời", "đỉnh nóc kịch trần", "slay") hay trộn "rứa", "nghen", "giời ơi" trong cùng một câu thì máy quét báo. Hướng dẫn ở [references/chat.md](skills/viet-nhu-nguoi/references/chat.md).

Các nhóm còn lại thì tiếng Việt hay tiếng Anh đều gặp: đối lập giả, câu chốt một dòng, liệt kê ép cho đủ ba, gạch ngang dài, thổi phồng, mượn uy tín mơ hồ, in đậm và emoji trang trí, lời chatbot, giải thích lại điều người đọc biết rồi.

Cũng có thứ skill không đụng tới: giọng vùng miền, khẩu ngữ, thuật ngữ Hán Việt dùng đúng chỗ, câu bị động trong tài liệu kỹ thuật, và mấy chữ nhỏ mà bỏ đi là đổi nghĩa như "vẫn", "chưa", "chỉ", "có thể".

## Chạy bằng dòng lệnh

Repo có hai script chạy tay được, đều chỉ dùng thư viện chuẩn của Python.

`scan.py` chấm điểm file `.md`, `.txt` hoặc `.pptx`, in ra điểm 0-100 và từng chỗ dính:

```bash
python3 -I skills/viet-nhu-nguoi/scripts/scan.py file.md
```

| Tùy chọn | Tác dụng |
| --- | --- |
| `--json` | in kết quả cho máy đọc |
| `--max 30` | thoát mã 1 nếu điểm quá 30, dùng trong CI hay pre-commit |
| `--meta` | bỏ qua phần trích dẫn (dòng `>`, bảng, chữ trong ngoặc kép), dùng khi văn bản bàn về chính các dấu hiệu |
| `--titles` | chỉ in tiêu đề theo thứ tự |
| `--chat` | văn bản là tin nhắn trả lời: báo thêm gạch đầu dòng, in đậm, câu khách sáo, tin quá dài |
| `--text` | in hết chữ và ghi chú từng slide trong file `.pptx` |

`check_facts.py` so bản gốc với bản sửa, so hai file `.pptx` cũng được. Số liệu, ngày giờ, link hay code bị mất hoặc tự thêm vào thì script báo lỗi, thiếu tên riêng thì nhắc:

```bash
python3 -I skills/viet-nhu-nguoi/scripts/check_facts.py goc.md moi.md
```

Kết quả quét hai file mẫu:

```text
$ python3 -I skills/viet-nhu-nguoi/scripts/scan.py examples/truoc.md
Điểm 84/100 (dày đặc): 17 dấu hiệu trong 5 dòng, 110 chữ.
[từ vựng AI (vi)] 3      nâng tầm, trong bối cảnh hiện nay, bên cạnh đó
[động từ rỗng (vi)] 3    tiến hành thực hiện, thực hiện việc, nhằm mục đích
[văn dịch (vi)] 2        được chứng minh bởi, trải nghiệm liền mạch
[danh hóa (vi)] 2        một cách đáng..., trở nên dễ...
["Điều này"/"Nó" mở câu] 2
[đối lập giả] 1          không chỉ là xu hướng mà còn
[thổi phồng] 1           yếu tố then chốt
[uy tín mơ hồ] 1         nhiều nghiên cứu chỉ ra
[lời chatbot] 1          hy vọng những thông tin trên
[chữ đệm dịch dày] 1     145 chữ đệm trên 1.000 chữ

$ python3 -I skills/viet-nhu-nguoi/scripts/scan.py examples/slide-truoc.pptx
Điểm 48/100 (nhiều dấu hiệu): 21 dấu hiệu trong 7 slide, 176 chữ.
[từ vựng AI (vi)] 7
[tiêu đề dạng nhãn] 4        slide 2: Tổng quan, slide 3: Thách thức, slide 5: Lợi ích, slide 6: Kết luận
[hứa suông] 1                slide 5, ghi chú: chi tiết sẽ được trao đổi sau
[tiêu đề đếm số ý] 1         slide 4: 3 trụ cột giải pháp
[câu khó nói (ghi chú)] 1    slide 2, ghi chú: Như chúng ta có thể thấy, ...
[số gạch đầu dòng đều] 1     5/5 slide có đúng 3 ý
...
```

## Lưu ý

Skill không gửi văn bản đi đâu cả, ngoài mô hình AI mà trợ lý vốn đang dùng. Skill chỉ gồm file Markdown và vài script Python dùng thư viện chuẩn, không kết nối mạng, không thu thập dữ liệu, không cần tài khoản.

Điểm số chỉ để tham khảo. Nhìn điểm thì biết bài viết theo khuôn nhiều hay ít, câu có đều quá không, còn bài có phải AI viết hay không thì không biết được. Có người vốn viết câu đều nhịp. Máy dò AI cũng hay bắt nhầm người viết bằng ngoại ngữ. Bài bị điểm cao thì cứ đọc lại mấy chỗ máy quét báo.

Dùng skill thì văn tự nhiên, dễ đọc hơn, nhưng không dám hứa bài sẽ lọt máy dò AI. Skill cũng không chơi mẹo lừa máy dò như cố ý sai chính tả hay chèn ký tự ẩn. Xin đừng dùng skill để làm bài hộ người học hay giả danh người khác. Cũng đừng cầm danh sách dấu hiệu đi kết luận ai đó dùng AI, vì đoán bằng cảm giác thì cũng chỉ nhỉnh hơn đoán mò một chút.

## Trong repo có gì

```text
skills/viet-nhu-nguoi/
├── SKILL.md                 quy tắc chính, Claude nạp khi skill được gọi
├── references/patterns.md   65 dấu hiệu, ví dụ trước/sau
├── references/slides.md     cách viết slide, lời thuyết trình, nhờ người đọc thử
├── references/chat.md       cá nhân hóa icon, ngữ điệu khi trả lời tin nhắn
├── references/sources.md    nguồn tham khảo: bài viết, nghiên cứu, hướng dẫn giọng văn, skill khác
├── scripts/scan.py          máy quét có điểm 0-100, không cần thư viện ngoài
├── scripts/check_facts.py   kiểm bản sửa giữ đúng số liệu, ngày giờ, link, code
├── scripts/slides.py        đọc chữ và ghi chú trong file .pptx, chỉ dùng thư viện chuẩn
└── LICENSE-humanizer        giấy phép MIT của blader/humanizer
assets/                      banner, ảnh ví dụ và script vẽ lại ảnh (make_images.py)
examples/                    văn mẫu và deck .pptx trước/sau dùng trong README và test
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Góp ý, báo lỗi

Gặp kiểu câu AI tiếng Việt nào skill chưa bắt, hay thấy skill sửa hỏng một câu vốn tự nhiên, thì mở issue, dán câu đó vào, kèm bản bạn thấy đúng. Pull request thêm dấu hiệu mới cần có ví dụ trước/sau và một test trong `tests/test_scan.py`, test phải có cả câu mà máy quét không được báo nhầm.

## Nguồn tham khảo

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. Khung danh mục dấu hiệu dựa theo skill này.
- Các skill humanize tiếng Việt mã nguồn mở (MIT), dùng để đối chiếu danh mục, còn nội dung ở đây thì viết lại theo cách riêng: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Phần slide học ý tưởng từ [carnot-tech/jinba-consulting-pptx-skill](https://github.com/carnot-tech/jinba-consulting-pptx-skill) (MIT), [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) (MIT) và skill `doc-coauthoring` trong [anthropics/skills](https://github.com/anthropics/skills) (Apache 2.0), rồi viết lại bằng lời riêng.
- [references/sources.md](skills/viet-nhu-nguoi/references/sources.md) liệt kê đủ nguồn: bài viết, sách và nghiên cứu về tiếng Việt, nghiên cứu về độ tin cậy của máy dò, hướng dẫn giọng văn, skill khác. Nguồn nào skill dựa vào trực tiếp thì trong file có ghi rõ.
