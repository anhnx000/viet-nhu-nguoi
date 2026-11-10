# Viết như người · Vietnamese Humanizer

**Chống giọng văn AI cho tiếng Việt. Nhờ AI viết, đọc lên vẫn là bạn.**

[![test](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Tiếng Việt** · [English](README.en.md)

![Trước: văn AI được 72/100. Sau: bản viết lại giọng người được 0/100.](assets/banner.png)

> **English:** a Claude skill that makes AI-drafted Vietnamese (and English) read like a person wrote it, without changing the facts. Read the [English README](README.en.md).
>
> *Viet nhu nguoi, chong giong van AI, human voice, Vietnamese humanizer, humanize tieng Viet, viet lai van AI tu nhien, bo giong ChatGPT.*

Nhờ AI làm slide, viết email hay báo cáo thì nhanh, nhưng người đọc nhận ra ngay. Tiêu đề slide lúc nào cũng là "Tổng quan", "Thách thức". Email thì mở bằng "Trong bối cảnh hiện nay" và kết bằng "Hy vọng thông tin trên hữu ích!". Gửi trong nhóm thì không sao, còn gửi lãnh đạo hay khách hàng thì bạn lại phải ngồi sửa.

Viết như người là một skill, tức một gói hướng dẫn cài thêm cho Claude và các trợ lý AI khác. Cài xong, AI viết tiếng Việt giống người đi làm viết hơn: tiêu đề slide nói thẳng kết luận, email xưng hô đúng vai, câu không rườm, số liệu bạn đưa được giữ nguyên. Skill miễn phí và có mã nguồn mở.

**Mục lục:** [Cài, không cần biết code](#cài-trong-vài-phút-không-cần-biết-code) · [Dùng hằng ngày](#dùng-hằng-ngày) · [Trước và sau](#trước-và-sau) · [Skill sửa những lỗi nào](#skill-sửa-những-lỗi-nào) · [Dòng lệnh](#cho-người-dùng-dòng-lệnh)

## Dùng vào việc gì

- Làm slide báo cáo, đề xuất. Mỗi tiêu đề là một câu kết luận, nên sếp đọc lướt các tiêu đề là biết cần quyết gì. Chỗ nào thiếu số liệu thì skill ghi `[cần xác nhận]`, không bịa cho đầy.
- Viết email cho sếp, cho khách hàng. Email nói việc trước và xưng hô đúng vai (anh/chị/em, quý khách), không tự đổi sang "bạn".
- Sửa báo cáo, tài liệu dịch từ tiếng Anh để bỏ những kiểu câu dịch như "được... bởi", "Điều này cho phép", "thông qua việc".
- Viết bài Facebook, LinkedIn, blog. AI viết nháp nhưng giọng vẫn là của bạn, và mỗi bài chỉ kể một chuyện.
- Soi lại bài trước khi gửi. Skill chỉ ra chỗ nào nghe giống AI, còn sửa hay không là bạn quyết.

## Cài trong vài phút, không cần biết code

Bạn không phải gõ lệnh nào, chỉ cần nhờ trợ lý AI cài hộ như nhờ bạn IT ngồi cạnh.

**Bước 1. Mở một trợ lý AI chạy trên máy tính.** Ví dụ ứng dụng Claude Code cho máy tính, dùng bằng chuột như mọi phần mềm khác. Codex, Cursor, Gemini CLI hay OpenCode cũng được, riêng Claude hay ChatGPT mở trên trình duyệt thì không cài được gì vào máy.

**Bước 2. Dán câu này vào ô chat:**

> Cài giúp tôi skill viet-nhu-nguoi từ https://github.com/anhnx000/viet-nhu-nguoi

**Bước 3. Bấm đồng ý** khi trợ lý xin phép tải và cài, thường chưa tới một phút là xong.

**Bước 4. Mở một cuộc trò chuyện mới và thử:**

> Viết như người: soạn giúp tôi email xin sếp lùi hạn nộp báo cáo 3 ngày, xưng em

Nếu email trả về ngắn, vào việc ngay và xưng "em" từ đầu đến cuối thì skill đã chạy.

Sau này cần gì bạn cũng chỉ việc nói với trợ lý.

| Bạn muốn | Bạn gõ |
| --- | --- |
| Kiểm tra đã cài chưa | "Máy tôi có skill viet-nhu-nguoi chưa?" |
| Lấy bản mới | "Cập nhật skill viet-nhu-nguoi lên bản mới nhất" |
| Gỡ ra | "Gỡ skill viet-nhu-nguoi khỏi máy" |

Nếu trợ lý báo lỗi khi cài, bạn chụp màn hình rồi [mở issue](https://github.com/anhnx000/viet-nhu-nguoi/issues) (trang báo lỗi của dự án), mình sẽ xem giúp.

<details>
<summary>Dành cho trợ lý AI được nhờ cài skill này</summary>

Người dùng không rành kỹ thuật, nên hãy tự làm hết và chỉ xin phép khi cần chạy lệnh. Thử lần lượt, dừng ở cách đầu tiên chạy được:

1. Có `npx`: chạy `npx skills add anhnx000/viet-nhu-nguoi -g -y`.
2. Có `git` và `bash` (macOS, Linux, WSL): `git clone https://github.com/anhnx000/viet-nhu-nguoi.git ~/viet-nhu-nguoi && bash ~/viet-nhu-nguoi/install.sh --copy`.
3. Windows không có bash, hoặc không có git: tải `https://github.com/anhnx000/viet-nhu-nguoi/archive/refs/heads/main.zip`, giải nén, rồi chép thư mục `skills/viet-nhu-nguoi` vào thư mục skill cấp người dùng của agent (Claude Code: `~/.claude/skills/viet-nhu-nguoi`, trên Windows là `%USERPROFILE%\.claude\skills\viet-nhu-nguoi`).

Cài xong, kiểm tra file `SKILL.md` nằm đúng trong thư mục đích và báo cho người dùng đường dẫn đã cài. Nếu skill chưa hiện thì nhắc họ mở cuộc trò chuyện mới.

Cập nhật thì dùng lại đúng cách đã cài. Với cách 2, chạy `git -C ~/viet-nhu-nguoi pull` rồi `bash ~/viet-nhu-nguoi/install.sh --copy --update`. Với cách 3, xóa thư mục cũ trước khi chép bản mới. Gỡ thì xóa thư mục `viet-nhu-nguoi` trong thư mục skill.

</details>

<details>
<summary>Dành cho người quen dòng lệnh: tự gõ lệnh cài</summary>

Trong Claude Code, cài như plugin:

```text
/plugin marketplace add anhnx000/viet-nhu-nguoi
/plugin install viet-nhu-nguoi@viet-nhu-nguoi
```

Hoặc clone rồi chạy script. Script tạo symlink vào `~/.claude/skills/`, nên sau này chỉ cần `git pull` là skill được cập nhật:

```bash
git clone https://github.com/anhnx000/viet-nhu-nguoi.git
cd viet-nhu-nguoi
bash install.sh                   # symlink
bash install.sh --copy            # hoặc chép file, nếu muốn đọc lại từng bản cập nhật trước khi cài
bash install.sh --copy --update   # thay bản đã chép bằng bản mới
```

Agent khác (Cursor, Codex, Gemini CLI, OpenCode...) cài bằng công cụ [skills](https://github.com/vercel-labs/skills):

```bash
npx skills add anhnx000/viet-nhu-nguoi      # chỉ cho dự án hiện tại
npx skills add anhnx000/viet-nhu-nguoi -g   # cho mọi dự án (cấp người dùng)
```

Lệnh sẽ hỏi cài cho agent nào. Muốn bỏ qua các câu hỏi thì thêm `-a claude-code` (hoặc `-a '*'`) và `-y`. Skill chỉ gồm file Markdown nên editor của bạn dùng mô hình nào cũng chạy được.

</details>

## Dùng hằng ngày

Bạn cứ nói như nhờ đồng nghiệp, không có cú pháp nào phải nhớ.

| Bạn gõ | Skill làm gì |
| --- | --- |
| "Làm slide báo cáo tiến độ dự án tuần này để sếp duyệt" | Hỏi trước ai xem, cần họ quyết gì, trình bày trực tiếp hay gửi đọc, rồi mới dựng slide |
| "Sửa file bao-cao-q3.pptx cho bớt giọng AI" | Đọc chữ và ghi chú từng slide, sửa tiêu đề, gạch đầu dòng, lời thuyết trình |
| "Viết email xin sếp lùi deadline 3 ngày, xưng em" | Viết email ngắn, nói việc trước, giữ đúng "em"/"anh" từ đầu đến cuối |
| "Viết bài Facebook kể về dự án của mình, khoảng 300 chữ" | Hỏi bạn một hai chuyện thật đã xảy ra rồi kể đúng một chuyện, không chia mục, không giảng lại kiến thức nền |
| "Soi giúp đoạn này chỗ nào giọng AI" | Chỉ ra từng chỗ kèm lý do và gợi ý sửa, không tự sửa |
| Dán kèm một email bạn tự viết | Học nhịp câu, từ nối, cách xưng hô của bạn rồi viết theo |

Muốn kết quả tốt hơn thì:

1. Nói rõ ai đọc và bạn là ai với họ. "Gửi chị trưởng phòng, xưng em" cho ra email khác hẳn "gửi khách hàng, xưng chúng tôi".
2. Dán một đoạn bạn tự viết, cùng loại với bài sắp viết, để skill bắt chước độ dài câu và từ bạn hay dùng.
3. Đưa số liệu, tên, ngày thật. Chỗ nào thiếu thì skill hỏi lại hoặc để trống, không tự nghĩ ra.
4. Thấy chỗ nào lạ thì nói "mình không nói thế". Skill sẽ đổi theo và nhớ cho phần còn lại của cuộc trò chuyện.

Vài cách dùng khác:

- Gõ `/viet-nhu-nguoi` để bật cho cả cuộc trò chuyện. Từ đó mọi câu trả lời đều theo quy tắc của skill, kể cả tin nhắn ngắn.
- Skill tự bật khi bạn nhờ soạn email, tin nhắn, bài đăng mà bạn sẽ gửi dưới tên mình.
- Bạn có thể gọi giọng bằng tên: *đời thường*, *công việc*, *kỹ thuật*, *ấm áp*, *thẳng*. Tên giọng chỉ đổi văn phong, còn xưng hô và nội dung giữ nguyên.
- Bài bạn tự viết thì skill chỉ sửa nhẹ.
- Với bộ slide quan trọng, skill có thể nhờ một trợ lý AI khác chưa biết gì về bối cảnh đọc thử và chấm 7 tiêu chí trên thang 70 điểm. Sau đó skill lập bảng góp ý để bạn chọn nhận hay bỏ từng mục.

## Trước và sau

Các điểm số bên dưới do máy quét đi kèm skill chấm trên thang 0-100. Điểm càng cao thì bài càng nhiều thói quen viết theo khuôn.

### Slide

Thư mục [`examples/`](examples) có hai bộ slide mẫu. Đây là tiêu đề của bộ AI làm:

```text
1. Chuyển đổi số: Hành trình kiến tạo giá trị
2. Tổng quan
3. Thách thức
4. 3 trụ cột giải pháp
5. Lợi ích
6. Kết luận
7. Cảm ơn
```

Còn đây là bộ làm theo skill:

```text
1. Đề xuất thuê thêm 1 QA cho quý 1/2027
2. Quý 3 trễ 2 tuần, cả 2 lần đều do thiếu người test
3. Thuê 1 QA rẻ hơn tiếp tục trễ
4. Cần anh duyệt trước 30/11 để kịp tuyển
```

Bộ thứ hai chỉ cần đọc bốn tiêu đề là hiểu cả đề xuất. Máy quét chấm bộ này 0/100, còn bộ đầu 48/100.

### Email, báo cáo

Bản AI viết:

> Trong bối cảnh hiện nay, việc ứng dụng AI không chỉ là xu hướng mà còn là yếu tố then chốt giúp doanh nghiệp nâng tầm hiệu suất. Điều này được chứng minh bởi nhiều nghiên cứu chỉ ra rằng năng suất có thể tăng một cách đáng kể.
>
> Bên cạnh đó, đội ngũ của chúng tôi đã tiến hành thực hiện việc triển khai hệ thống mới nhằm mục đích mang lại trải nghiệm liền mạch cho khách hàng. Nó giúp việc quản lý dự án trở nên dễ dàng hơn, nhanh chóng hơn và hiệu quả hơn.
>
> Hy vọng những thông tin trên sẽ hữu ích cho bạn!

Sau khi qua skill:

> Đội mình đã đưa hệ thống quản lý dự án mới vào dùng. Khách hàng giờ tự xem được tiến độ.

Bản này ngắn vì skill không bịa số liệu. Muốn có chi tiết thì skill hỏi bạn rồi viết theo đúng những gì bạn đưa:

> Từ tháng 3, đội mình chuyển việc theo dõi dự án sang hệ thống mới. Khách hàng tự xem tiến độ, không phải nhắn hỏi như trước, và mỗi tuần đội bớt được khoảng nửa ngày làm báo cáo.

Bản AI viết được 72/100 với 16 dấu hiệu, hai bản sau đều 0/100.

### Bài đăng dài

Bản 2.2 của skill ra đời từ một bài đăng thật. [Bài gốc](examples/bai-dang-truoc.md) dài 1.740 chữ, chia chín mục viết hoa. Những từ AI quen thuộc đã được bỏ gần hết nên máy quét bản cũ chấm 3/100, vậy mà người đọc vẫn nhận ra ngay vì cả bài lặp đi lặp lại vài kiểu câu:

> Nói cho thật: tiến độ không dễ. [...] Khó nhất không phải là code, mà là chọn việc gì để làm. [...] Mình không cần bạn giỏi kernel. Mình cần bạn kiên nhẫn đọc log.

Từ bản 2.2, máy quét đếm trên cả bài và chấm bài này 55/100. Bài có mười câu kiểu "không phải X mà là Y" và sáu câu mở bằng nhãn như "nói gọn", "nói cho thật". Trong 88 câu thì 19 câu có dấu hai chấm.

[Bản viết lại](examples/bai-dang-sau.md) còn 376 chữ và chỉ làm một việc là rủ người vào làm cùng. Máy quét chấm bản này 0/100, và nó không thêm dữ kiện nào ngoài bài gốc. Phần định nghĩa hệ điều hành, lịch sử microkernel và thống kê bảo mật để dành cho bài khác.

## Skill sửa những lỗi nào

Skill có danh mục 55 dấu hiệu của văn AI, mỗi dấu hiệu kèm ví dụ trước và sau ([xem đầy đủ](skills/viet-nhu-nguoi/references/patterns.md)). Bảng dưới là nhóm riêng cho tiếng Việt.

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

Có những dấu hiệu chỉ lộ ra khi đọc cả bài, dù từng câu đã ổn:

- câu mở bằng nhãn ("nói gọn", "nói cho thật:");
- kiểu "không phải X mà là Y" lặp từ ba lần;
- đoạn nào cũng kết bằng một câu nghe như châm ngôn;
- dấu hai chấm dày đặc;
- dấu chấm chặt một ý thành nhiều câu vụn, hoặc ngược lại là một câu gộp quá nhiều vế;
- bài đăng dài ôm đủ mọi chủ đề.

Slide và tài liệu nhiều trang có nhóm riêng. Ở nhóm này skill bắt tiêu đề chỉ là nhãn ("Tổng quan", "Kết luận"), tiêu đề đếm số ý ("3 trụ cột"), slide nào cũng đúng ba ý, lời hứa suông ("chi tiết sẽ trao đổi sau") và ghi chú thuyết trình viết như công văn. Hướng dẫn viết slide nằm ở [references/slides.md](skills/viet-nhu-nguoi/references/slides.md).

Các nhóm còn lại dùng cho cả tiếng Việt lẫn tiếng Anh: đối lập giả, câu chốt một dòng, liệt kê ép cho đủ ba, gạch ngang dài, thổi phồng, mượn uy tín mơ hồ, in đậm và emoji trang trí, lời chatbot, giải thích lại điều người đọc đã biết.

Skill cũng biết giữ nguyên những thứ không nên sửa: giọng vùng miền, khẩu ngữ, thuật ngữ Hán Việt đúng chỗ, câu bị động trong tài liệu kỹ thuật, và các từ nhỏ làm đổi nghĩa như "vẫn", "chưa", "chỉ", "có thể".

## Cho người dùng dòng lệnh

Repo có hai script chạy tay được, cả hai chỉ dùng thư viện chuẩn của Python.

`scan.py` chấm điểm một file `.md`, `.txt` hoặc `.pptx`, in điểm 0-100 và từng chỗ khớp:

```bash
python3 -I skills/viet-nhu-nguoi/scripts/scan.py file.md
```

| Tùy chọn | Tác dụng |
| --- | --- |
| `--json` | in kết quả dạng máy đọc |
| `--max 30` | thoát mã 1 khi điểm vượt 30, dùng cho CI hay pre-commit |
| `--meta` | bỏ qua phần trích dẫn (dòng `>`, bảng, chữ trong ngoặc kép), dùng cho văn bản bàn về chính các dấu hiệu |
| `--titles` | chỉ in các tiêu đề theo thứ tự |
| `--text` | in toàn bộ chữ và ghi chú từng slide của file `.pptx` |

`check_facts.py` so bản gốc với bản sửa, hai file `.pptx` cũng so được. Script báo lỗi khi số liệu, ngày giờ, link hay code bị mất hoặc bị thêm, và nhắc khi thiếu tên riêng:

```bash
python3 -I skills/viet-nhu-nguoi/scripts/check_facts.py goc.md moi.md
```

Kết quả quét hai file mẫu:

```text
$ python3 -I skills/viet-nhu-nguoi/scripts/scan.py examples/truoc.md
Điểm 72/100 (dày đặc): 16 dấu hiệu trong 5 dòng, 110 chữ.
[từ vựng AI (vi)] 3      nâng tầm, trong bối cảnh hiện nay, bên cạnh đó
[động từ rỗng (vi)] 3    tiến hành thực hiện, thực hiện việc, nhằm mục đích
[văn dịch (vi)] 2        được chứng minh bởi, trải nghiệm liền mạch
[danh hóa (vi)] 2        một cách đáng..., trở nên dễ...
["Điều này"/"Nó" mở câu] 2
[đối lập giả] 1          không chỉ là xu hướng mà còn
[thổi phồng] 1           yếu tố then chốt
[uy tín mơ hồ] 1         nhiều nghiên cứu chỉ ra
[lời chatbot] 1          hy vọng những thông tin trên

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

## Vài điều nên biết

Skill không gửi văn bản của bạn đi đâu thêm, văn bản chỉ tới mô hình AI mà trợ lý của bạn vốn đang dùng. Bản thân skill gồm các file Markdown và mấy script Python chỉ dùng thư viện chuẩn, không gọi mạng, không thu thập dữ liệu, không cần tài khoản.

Điểm số chỉ để tham khảo. Điểm cho biết bài có bao nhiêu thói quen viết theo khuôn và câu có đều nhau quá không, chứ chưa nói được bài có do AI viết hay không. Có người vốn viết câu đều nhịp, và các máy dò AI hay báo nhầm người viết bằng ngôn ngữ không phải tiếng mẹ đẻ. Bài được điểm cao thì bạn coi kết quả như danh sách những chỗ nên đọc lại.

Skill giúp văn bản tự nhiên và dễ đọc hơn, nhưng không cam kết bài qua được máy dò AI. Skill cũng không dùng mẹo lừa máy dò như cố ý sai chính tả hay chèn ký tự ẩn. Xin đừng dùng skill để nộp bài thay người học hay giả danh người khác. Cũng đừng lấy danh sách dấu hiệu ra để kết luận ai đó dùng AI, vì người đoán văn AI bằng cảm giác chỉ đúng hơn may rủi một chút.

## Trong repo có gì

```text
skills/viet-nhu-nguoi/
├── SKILL.md                 quy tắc chính, Claude nạp khi skill được gọi
├── references/patterns.md   55 dấu hiệu, ví dụ trước/sau
├── references/slides.md     cách viết slide, lời thuyết trình, nhờ người đọc thử
├── references/sources.md    nguồn tham khảo: bài viết, nghiên cứu, hướng dẫn giọng văn, skill khác
├── scripts/scan.py          máy quét có điểm 0-100, không cần thư viện ngoài
├── scripts/check_facts.py   kiểm bản sửa giữ đúng số liệu, ngày giờ, link, code
├── scripts/slides.py        đọc chữ và ghi chú trong file .pptx, chỉ dùng thư viện chuẩn
└── LICENSE-humanizer        giấy phép MIT của blader/humanizer
assets/                      banner
examples/                    văn mẫu và deck .pptx trước/sau dùng trong README và test
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Đóng góp

Nếu bạn gặp một kiểu câu AI tiếng Việt mà skill chưa bắt, hoặc thấy skill sửa hỏng một câu vốn tự nhiên, bạn mở issue và dán câu đó vào, kèm bản bạn thấy đúng. Pull request thêm dấu hiệu mới cần có ví dụ trước/sau và một test trong `tests/test_scan.py`, gồm cả trường hợp không được báo nhầm.

## Nguồn

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. Khung danh mục dấu hiệu dựa trên skill này.
- Các skill humanize tiếng Việt mã nguồn mở (MIT), dùng để đối chiếu danh mục, còn nội dung ở đây viết lại theo cách riêng: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Phần slide học ý tưởng (viết lại bằng lời riêng) từ [carnot-tech/jinba-consulting-pptx-skill](https://github.com/carnot-tech/jinba-consulting-pptx-skill) (MIT), [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) (MIT) và skill `doc-coauthoring` trong [anthropics/skills](https://github.com/anthropics/skills) (Apache 2.0).
- [references/sources.md](skills/viet-nhu-nguoi/references/sources.md) liệt kê đủ các nguồn: bài viết, sách và nghiên cứu về tiếng Việt, nghiên cứu về độ tin cậy của máy dò, hướng dẫn giọng văn và các skill khác. File này có ghi rõ skill dựa trực tiếp vào nguồn nào.
