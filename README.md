# Viết như người · Vietnamese Humanizer

Chống giọng văn AI cho tiếng Việt: nhờ AI viết mà đọc lên vẫn ra giọng mình.

[![test](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Tiếng Việt** · [English](README.en.md)

![Trước: văn AI được 84/100. Sau: bản viết lại giọng người được 0/100.](assets/banner.png)

> **English:** a Claude skill that makes AI-drafted Vietnamese (and English) read like a person wrote it, without changing the facts. Read the [English README](README.en.md).
>
> *Viet nhu nguoi, chong giong van AI, human voice, Vietnamese humanizer, humanize tieng Viet, viet lai van AI tu nhien, bo giong ChatGPT.*

Nhờ AI làm slide, viết email, báo cáo thì nhanh, có điều ai đọc cũng nhận ra. Slide nào cũng "Tổng quan", "Thách thức", email mở bằng "Trong bối cảnh hiện nay" rồi kết bằng "Hy vọng thông tin trên hữu ích!". Gửi sếp hay gửi khách thì lại phải ngồi sửa tay.

Viết như người là một skill (bộ hướng dẫn cài thêm) cho Claude Code, Codex, Cursor và các trợ lý AI khác. Cài vào rồi thì tiêu đề slide nói thẳng kết luận, email xưng hô đúng vai, câu gọn, số liệu đưa sao để vậy. Miễn phí, mã nguồn mở.

Mục lục: [Cài đặt](#cài-không-cần-biết-lập-trình) · [Cách dùng](#cách-dùng) · [Trước và sau](#trước-và-sau) · [Skill sửa những gì](#skill-sửa-những-gì) · [Dòng lệnh](#chạy-bằng-dòng-lệnh)

## Dùng vào việc gì

- Slide báo cáo, đề xuất: tiêu đề nào cũng là một câu kết luận, sếp lướt qua là biết cần quyết gì. Chỗ thiếu số liệu thì ghi `[cần xác nhận]` để bạn điền.
- Email gửi sếp, gửi khách: nói việc trước, giữ đúng cặp xưng hô (anh/chị/em, quý khách), không tự đổi thành "bạn".
- Tài liệu dịch từ tiếng Anh: bỏ các kiểu câu "được... bởi", "Điều này cho phép", "thông qua việc".
- Bài Facebook, LinkedIn, blog: AI viết nháp mà vẫn ra giọng bạn, mỗi bài kể một chuyện.
- Trả lời tin nhắn theo giọng bạn: xưng hô, viết tắt, kiểu cười học từ những tin bạn từng gửi đúng người đó. Trong cùng một nhóm, với bạn thân thì suồng sã, với sếp hay người lớn tuổi thì lễ phép.
- Soi bài trước khi gửi: chỉ ra chỗ nghe giống AI, sửa hay không do bạn.

## Cài, không cần biết lập trình

Không phải gõ lệnh, cứ nhờ trợ lý AI cài hộ như nhờ bạn IT ngồi cạnh.

1. Mở trợ lý AI chạy trên máy tính: Claude Code (có bản dùng chuột như phần mềm thường), Codex, Cursor, Gemini CLI hay OpenCode đều được. Claude hay ChatGPT mở trên trình duyệt thì không cài được gì vào máy.
2. Dán câu này vào ô chat:

   > Cài giúp tôi skill viet-nhu-nguoi từ https://github.com/anhnx000/viet-nhu-nguoi

3. Trợ lý xin phép tải và cài thì bấm đồng ý, thường chưa tới một phút là xong.
4. Mở cuộc trò chuyện mới rồi thử:

   > Viết như người: soạn giúp tôi email xin sếp lùi hạn nộp báo cáo 3 ngày, xưng em

Email trả về ngắn, vào việc ngay, xưng "em" từ đầu tới cuối là được.

Kiểm tra, cập nhật hay gỡ cũng nói với trợ lý như vậy: "Máy tôi có skill viet-nhu-nguoi chưa?", "Cập nhật skill viet-nhu-nguoi lên bản mới nhất", "Gỡ skill viet-nhu-nguoi khỏi máy". Cài bị lỗi thì chụp màn hình rồi [mở issue](https://github.com/anhnx000/viet-nhu-nguoi/issues), mình xem giúp.

<details>
<summary>Dành cho trợ lý AI được nhờ cài skill này</summary>

Người nhờ cài không rành kỹ thuật, nên hãy tự làm hết, chỉ xin phép lúc cần chạy lệnh. Thử lần lượt, cách nào chạy được thì dừng ở đó:

1. Máy có `npx`: chạy `npx skills add anhnx000/viet-nhu-nguoi -g -y`.
2. Máy có `git` và `bash` (macOS, Linux, WSL): `git clone https://github.com/anhnx000/viet-nhu-nguoi.git ~/viet-nhu-nguoi && bash ~/viet-nhu-nguoi/install.sh --copy`.
3. Windows không có bash, hoặc không có git: tải `https://github.com/anhnx000/viet-nhu-nguoi/archive/refs/heads/main.zip`, giải nén, rồi chép thư mục `skills/viet-nhu-nguoi` vào thư mục skill cấp người dùng của agent (Claude Code: `~/.claude/skills/viet-nhu-nguoi`, trên Windows là `%USERPROFILE%\.claude\skills\viet-nhu-nguoi`).

Cài xong thì kiểm tra file `SKILL.md` đã nằm đúng thư mục đích chưa, rồi báo đường dẫn cho người dùng. Skill chưa hiện thì nhắc họ mở cuộc trò chuyện mới.

Cập nhật thì cài cách nào làm lại cách đó. Cách 2: chạy `git -C ~/viet-nhu-nguoi pull` rồi `bash ~/viet-nhu-nguoi/install.sh --copy --update`. Cách 3: xóa thư mục cũ rồi mới chép bản mới. Gỡ thì xóa thư mục `viet-nhu-nguoi` trong thư mục skill.

</details>

<details>
<summary>Dành cho người quen dòng lệnh</summary>

Trong Claude Code thì cài như plugin:

```text
/plugin marketplace add anhnx000/viet-nhu-nguoi
/plugin install viet-nhu-nguoi@viet-nhu-nguoi
```

Hoặc clone về rồi chạy script. Mặc định script tạo symlink vào `~/.claude/skills/`, về sau `git pull` là có bản mới:

```bash
git clone https://github.com/anhnx000/viet-nhu-nguoi.git
cd viet-nhu-nguoi
bash install.sh                   # symlink
bash install.sh --copy            # chép file, muốn đọc từng bản cập nhật trước khi cài
bash install.sh --copy --update   # thay bản đã chép bằng bản mới
```

Agent khác (Cursor, Codex, Gemini CLI, OpenCode...) thì dùng công cụ [skills](https://github.com/vercel-labs/skills):

```bash
npx skills add anhnx000/viet-nhu-nguoi      # chỉ cho dự án hiện tại
npx skills add anhnx000/viet-nhu-nguoi -g   # cho mọi dự án
```

Thêm `-a claude-code` (hoặc `-a '*'`) và `-y` để lệnh khỏi hỏi cài cho agent nào. Skill chỉ có file Markdown nên editor chạy mô hình nào cũng dùng được.

</details>

## Cách dùng

Cứ nói như nhờ đồng nghiệp, không có cú pháp gì phải nhớ.

| Gõ thế này | Skill làm gì |
| --- | --- |
| "Làm slide báo cáo tiến độ dự án tuần này để sếp duyệt" | Hỏi ai xem, cần họ quyết gì, trình bày trực tiếp hay gửi đọc, rồi mới dựng slide |
| "Sửa file bao-cao-q3.pptx cho bớt giọng AI" | Đọc chữ và ghi chú từng slide, sửa tiêu đề, gạch đầu dòng, lời thuyết trình |
| "Viết email xin sếp lùi deadline 3 ngày, xưng em" | Viết email ngắn, nói việc trước, giữ "em"/"anh" từ đầu tới cuối |
| "Viết bài Facebook kể về dự án của mình, khoảng 300 chữ" | Hỏi một hai chuyện có thật rồi kể đúng một chuyện, không chia mục |
| "Soi giúp đoạn này chỗ nào giọng AI" | Chỉ ra từng chỗ kèm lý do và gợi ý sửa, không tự sửa |
| "Rep giúp mình tin anh Tuấn trong nhóm này" kèm đoạn chat | Nhắn theo đúng giọng bạn vẫn dùng với anh Tuấn, dù trong nhóm bạn hay đùa với người khác |

Muốn bài sát ý hơn thì nói rõ ai đọc và bạn với họ vai vế thế nào, vì "gửi chị trưởng phòng, xưng em" ra email khác hẳn "gửi khách hàng, xưng chúng tôi". Có sẵn đoạn tự viết cùng loại thì dán kèm để skill học nhịp câu và chữ bạn hay dùng. Số liệu, tên, ngày tháng thì đưa đúng bản thật, thiếu chỗ nào skill hỏi lại. Câu nào không giống mình thì bảo "mình không nói thế", skill sửa theo tới hết cuộc trò chuyện.

Gõ `/viet-nhu-nguoi` để bật cho cả cuộc trò chuyện, kể cả câu trả lời ngắn. Nhờ soạn email, tin nhắn hay bài đăng đứng tên bạn thì skill tự bật. Bài bạn tự viết thì chỉ sửa nhẹ. Bộ slide quan trọng còn có thêm một trợ lý chưa biết gì về bối cảnh đọc thử và chấm theo 7 tiêu chí, nhận góp ý nào là do bạn.

## Trước và sau

Điểm dưới đây do máy quét kèm theo skill chấm, thang 0-100, bài càng viết theo khuôn càng nhiều điểm.

### Slide

![Tiêu đề slide. Bộ AI làm, 48/100: Chuyển đổi số: Hành trình kiến tạo giá trị; Tổng quan; Thách thức; 3 trụ cột giải pháp; Lợi ích; Kết luận; Cảm ơn. Bộ làm theo skill, 0/100: Đề xuất thuê thêm 1 QA cho quý 1/2027; Hai bản phát hành quý 3 đều trễ vì thiếu người test; Thuê 1 QA tốn ít hơn tiền phạt mỗi lần trễ hạn; Cần anh duyệt trước 30/11 để kịp tuyển người.](assets/vi-du-slide.png)

Bộ AI làm có bảy tiêu đề toàn nhãn. Bộ làm theo skill chỉ cần đọc bốn tiêu đề là hiểu cả đề xuất. Hai file `.pptx` nằm trong [`examples/`](examples).

### Email, báo cáo

![Email, báo cáo. Bản AI viết, 84/100, mở bằng "Trong bối cảnh hiện nay" và kết bằng "Hy vọng những thông tin trên sẽ hữu ích cho bạn!". Qua skill, 0/100: Đội mình đã chuyển sang hệ thống quản lý dự án mới, nên giờ theo dõi dự án nhanh và đỡ vất vả hơn, khách hàng làm việc với đội cũng thuận tiện hơn trước. Có thêm chi tiết bạn đưa, 0/100: Từ tháng 3, đội mình chuyển việc theo dõi dự án sang hệ thống mới.](assets/vi-du-email.png)

Máy quét bắt 17 cụm trong bài AI viết, chính là những chỗ tô đỏ. Bài gốc không có số liệu nào nên bản qua skill cũng ngắn, skill không tự thêm. Có chi tiết bạn đưa thì ra đoạn thứ ba. Ba đoạn này nằm ở [`examples/truoc.md`](examples/truoc.md), [`sau.md`](examples/sau.md) và [`sau-co-chi-tiet.md`](examples/sau-co-chi-tiet.md).

### Bài đăng dài

![Bài đăng dài. Bài gốc, 55/100: 1.740 chữ, mười câu kiểu "không phải X mà là Y", sáu câu mở bằng nhãn, 19 trên 88 câu có dấu hai chấm. Bản viết lại, 0/100: 373 chữ, chỉ rủ người vào làm cùng.](assets/vi-du-bai-dang.png)

[Bài gốc](examples/bai-dang-truoc.md) gần như không còn từ AI quen mặt mà ai đọc vẫn nhận ra, vì vài kiểu câu cứ lặp đi lặp lại từ đầu tới cuối. Máy quét đếm các kiểu câu đó nên chấm 55/100. [Bản viết lại](examples/bai-dang-sau.md) còn 373 chữ, chỉ giữ việc rủ người vào làm cùng, không thêm dữ kiện nào. Phần định nghĩa hệ điều hành, lịch sử microkernel, thống kê bảo mật để dành viết riêng.

## Skill sửa những gì

Danh mục của skill có 65 dấu hiệu văn AI, mỗi dấu hiệu kèm ví dụ trước và sau ([xem đủ](skills/viet-nhu-nguoi/references/patterns.md)). Mấy dấu hiệu riêng của tiếng Việt:

| Dấu hiệu | Ví dụ | Sửa thành |
| --- | --- | --- |
| Bị động kiểu dịch | được phát triển bởi Google | Google phát triển |
| "Điều này", "Nó" mở câu | Điều này cho phép người dùng... | gọi tên sự vật, hoặc lược chủ ngữ |
| Danh hóa | Việc áp dụng AI giúp việc quản lý trở nên dễ dàng | Dùng AI thì quản lý dễ hơn |
| Động từ rỗng | tiến hành thực hiện việc rà soát | rà soát |
| Cụm marketing dịch sát | mở khóa tiềm năng, trải nghiệm liền mạch | nói cụ thể làm được gì |
| Thừa nghĩa | hiện nay đang trong quá trình | đang |
| Xưng hô | cả bài "bạn" gửi sếp, trộn "bạn"/"quý vị" | một cặp xưng hô đúng vai |
| Chêm tiếng Anh | hiệu suất (performance) | hiệu suất |

Khó thấy hơn là văn dịch từng chữ: từng chữ đều là tiếng Việt mà câu vẫn theo khuôn tiếng Anh. Kiểu này hay mở câu bằng "Bạn", "Với...", "Để..., bạn cần...", gắn "của bạn" sau danh từ, rải "một", "các", "đã", "sẽ" khắp bài. Gặp văn như vậy, skill viết lại từ ý chứ không thay từng cụm.

Có dấu hiệu phải đếm trên cả bài mới thấy, dù từng câu đều ổn:

- kiểu "không phải X mà là Y" lặp lại
- câu mở đầu bằng nhãn ("nói gọn", "nói cho thật:")
- đoạn nào cũng khép lại bằng một câu nghe như châm ngôn
- dấu hai chấm dày đặc, hoặc dấu chấm chặt một ý thành nhiều câu vụn
- bài chia mục bằng emoji, cuối bài mời bình luận

Slide có nhóm riêng: tiêu đề chỉ là nhãn, tiêu đề đếm số ý ("3 trụ cột"), slide nào cũng đúng ba ý, ghi chú thuyết trình viết như công văn. Hướng dẫn ở [slides.md](skills/viet-nhu-nguoi/references/slides.md).

Tin nhắn thì icon, kiểu cười, viết tắt lấy từ tối đa 30 lượt trò chuyện gần nhất, và giọng đổi theo từng người nhận. Trợ từ như "à", "nhé", "ạ" phải giữ đúng ý hỏi, nhờ hay hứa của người nói. Bản nháp dồn ba bốn chữ lóng vào một tin hay trộn "rứa", "nghen", "giời ơi" trong một câu thì máy quét báo. Hướng dẫn ở [chat.md](skills/viet-nhu-nguoi/references/chat.md) và [spoken.md](skills/viet-nhu-nguoi/references/spoken.md).

Skill không đụng tới giọng vùng miền, khẩu ngữ, thuật ngữ Hán Việt dùng đúng chỗ, câu bị động trong tài liệu kỹ thuật, và mấy chữ bỏ đi là đổi nghĩa như "vẫn", "chưa", "chỉ", "có thể".

## Chạy bằng dòng lệnh

Hai script chạy tay được, chỉ dùng thư viện chuẩn của Python.

`scan.py` chấm file `.md`, `.txt` hoặc `.pptx`, in điểm 0-100 và từng chỗ dính:

```bash
python3 -I skills/viet-nhu-nguoi/scripts/scan.py file.md
```

| Tùy chọn | Tác dụng |
| --- | --- |
| `--json` | in kết quả cho máy đọc |
| `--max 30` | thoát mã 1 nếu điểm quá 30, dùng trong CI hay pre-commit |
| `--meta` | bỏ qua phần trích dẫn (dòng `>`, bảng, chữ trong ngoặc kép), dùng cho văn bản bàn về chính các dấu hiệu |
| `--titles` | chỉ in tiêu đề theo thứ tự |
| `--chat` | văn bản là tin nhắn trả lời: báo thêm gạch đầu dòng, in đậm, câu khách sáo, tin quá dài |
| `--text` | in hết chữ và ghi chú từng slide trong file `.pptx` |

Chuyện bịa thì máy quét không chấm được. Với bài xưng "mình", "tôi", máy quét in thêm một dòng liệt kê chi tiết riêng có con số ("tháng thứ tư", "5h15") và lời người khác nói trong ngoặc kép, vì AI viết hộ hay tự thêm đúng loại chi tiết này. Dòng đó không tính điểm.

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
```

`check_facts.py` so bản gốc với bản sửa (hai file `.pptx` cũng được). Số liệu, ngày giờ, link hay code bị mất hoặc tự thêm thì báo lỗi. Số so theo giá trị nên "1.250" với "1250", "3 khách" với "ba khách" coi là một. Tên riêng, số viết bằng chữ, thứ trong tuần và các chữ "chưa", "vẫn", "chỉ", "có thể" bị rơi thì script nhắc xem lại.

```bash
python3 -I skills/viet-nhu-nguoi/scripts/check_facts.py goc.md moi.md
```

Bài AI viết mới thì so với lời dặn: lưu ghi chú hay tin nhắn bạn đã đưa cho AI vào một file rồi thêm `--brief`. Script liệt kê số liệu, ngày giờ, tên riêng, lời thoại có trong bài mà bạn chưa hề đưa, để soát trước khi đăng dưới tên mình.

```bash
python3 -I skills/viet-nhu-nguoi/scripts/check_facts.py --brief loi-dan.txt bai.md
```

## Lưu ý

Skill không gửi văn bản đi đâu ngoài mô hình AI mà trợ lý vốn đang dùng. Trong skill chỉ có file Markdown và vài script Python, script không kết nối mạng, không thu thập dữ liệu, không cần tài khoản.

Điểm số chỉ cho biết bài viết theo khuôn nhiều hay ít. Bài có phải AI viết không thì điểm không trả lời được, vì có người vốn viết câu đều nhịp. Bài bị điểm cao thì đọc lại mấy chỗ máy quét báo.

Skill không hứa bài lọt máy dò AI, cũng không chơi mẹo lừa máy dò như cố ý sai chính tả hay chèn ký tự ẩn. Xin đừng dùng skill để làm bài hộ người học hay giả danh người khác, và đừng cầm danh sách dấu hiệu đi kết luận ai đó dùng AI.

## Trong repo có gì

```text
skills/viet-nhu-nguoi/
├── SKILL.md                 quy tắc chính, trợ lý đọc mỗi lần dùng skill
├── references/patterns.md   65 dấu hiệu, ví dụ trước/sau
├── references/slides.md     slide, lời thuyết trình, nhờ người đọc thử
├── references/chat.md       tin nhắn theo giọng người dùng, theo từng người nhận
├── references/spoken.md     trợ từ, lời nhờ, lời hứa, bản chép lời
├── references/sources.md    nguồn tham khảo
├── scripts/scan.py          máy quét, điểm 0-100
├── scripts/check_facts.py   so số liệu, ngày giờ, link, code giữa hai bản
├── scripts/slides.py        đọc chữ và ghi chú trong file .pptx
└── LICENSE-humanizer        giấy phép MIT của blader/humanizer
assets/                      banner, ảnh ví dụ, script vẽ lại ảnh (make_images.py)
examples/                    văn mẫu và deck .pptx trước/sau
evals/                       bộ đề thử hành vi của skill, xem evals/README.md
tests/                       python3 -m unittest discover -s tests
```

## Góp ý, báo lỗi

Gặp kiểu câu AI tiếng Việt nào skill chưa bắt, hay thấy skill sửa hỏng một câu vốn tự nhiên, thì mở issue, dán câu đó kèm bản bạn thấy đúng. Pull request thêm dấu hiệu mới cần ví dụ trước/sau và một test trong `tests/test_scan.py`, test có cả câu máy quét không được báo nhầm.

## Nguồn tham khảo

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. Khung danh mục dấu hiệu dựa theo skill này.
- Các skill humanize tiếng Việt mã nguồn mở (MIT), dùng để đối chiếu danh mục, nội dung ở đây viết lại theo cách riêng: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Phần slide học ý tưởng từ [carnot-tech/jinba-consulting-pptx-skill](https://github.com/carnot-tech/jinba-consulting-pptx-skill) (MIT), [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) (MIT) và skill `doc-coauthoring` trong [anthropics/skills](https://github.com/anthropics/skills) (Apache 2.0), rồi viết lại bằng lời riêng.
- [references/sources.md](skills/viet-nhu-nguoi/references/sources.md) liệt kê đủ nguồn: sách và nghiên cứu về tiếng Việt, nghiên cứu về độ tin cậy của máy dò, hướng dẫn giọng văn, skill khác.
