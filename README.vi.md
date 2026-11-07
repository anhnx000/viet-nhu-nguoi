# Vietnamese Humanizer

[![test](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Skill cho [Claude Code](https://code.claude.com/docs/en/skills) giúp văn tiếng Việt do AI viết đọc lên giống người viết. Nó bỏ những thứ khiến người đọc nhận ra ngay là "con AI viết": "Trong bối cảnh hiện nay", "không chỉ... mà còn...", "được phát triển bởi", "tiến hành thực hiện việc", "một cách hiệu quả", "Hy vọng thông tin trên hữu ích!".

Tiếng Anh vẫn dùng được, nhưng phần làm kỹ nhất là tiếng Việt: văn dịch từ tiếng Anh, danh hóa "việc/sự", giọng công văn, xưng hô sai vai.

[English](README.md) · **Tiếng Việt**

## Trước và sau

Bản AI viết:

> Trong bối cảnh hiện nay, việc ứng dụng AI không chỉ là xu hướng mà còn là yếu tố then chốt giúp doanh nghiệp nâng tầm hiệu suất. Điều này được chứng minh bởi nhiều nghiên cứu chỉ ra rằng năng suất có thể tăng một cách đáng kể.
>
> Bên cạnh đó, đội ngũ của chúng tôi đã tiến hành thực hiện việc triển khai hệ thống mới nhằm mục đích mang lại trải nghiệm liền mạch cho khách hàng. Nó giúp việc quản lý dự án trở nên dễ dàng hơn, nhanh chóng hơn và hiệu quả hơn.
>
> Hy vọng những thông tin trên sẽ hữu ích cho bạn!

Sau khi qua skill:

> Đội mình đã đưa hệ thống quản lý dự án mới vào dùng. Khách hàng giờ tự xem được tiến độ.

Skill không bịa số liệu. Nếu muốn bài có chi tiết, nó sẽ hỏi bạn, rồi viết với đúng những gì bạn đưa:

> Từ tháng 3, đội mình chuyển việc theo dõi dự án sang hệ thống mới. Khách hàng tự xem tiến độ, không phải nhắn hỏi như trước, và mỗi tuần đội bớt được khoảng nửa ngày làm báo cáo.

Máy quét đi kèm chấm bản đầu 72/100 (dày đặc) với 16 dấu hiệu, hai bản sau đều 0/100:

```text
$ python3 -I skills/vietnamese-humanizer/scripts/scan.py examples/truoc.md
Điểm 72/100 (dày đặc): 16 dấu hiệu trong 5 dòng.
[từ vựng AI (vi)] 3      nâng tầm, trong bối cảnh hiện nay, bên cạnh đó
[động từ rỗng (vi)] 3    tiến hành thực hiện, thực hiện việc, nhằm mục đích
[văn dịch (vi)] 2        được chứng minh bởi, trải nghiệm liền mạch
[danh hóa (vi)] 2        một cách đáng..., trở nên dễ...
["Điều này"/"Nó" mở câu] 2
[đối lập giả] 1          không chỉ là xu hướng mà còn
[thổi phồng] 1           yếu tố then chốt
[uy tín mơ hồ] 1         nhiều nghiên cứu chỉ ra
[lời chatbot] 1          hy vọng những thông tin trên
```

## Cài

Cài như plugin, trong Claude Code:

```text
/plugin marketplace add anhnx000/vietnamese-humanizer
/plugin install vietnamese-humanizer@vietnamese-humanizer
```

Hoặc clone rồi chạy script. Script tạo symlink vào `~/.claude/skills/`, sau này `git pull` là skill được cập nhật:

```bash
git clone https://github.com/anhnx000/vietnamese-humanizer.git
cd vietnamese-humanizer
bash install.sh          # symlink
bash install.sh --copy   # hoặc chép file, nếu muốn đọc lại từng bản cập nhật trước khi cài
```

Mở phiên Claude Code mới sau khi cài.

Agent khác (Cursor, Codex, Gemini CLI, OpenCode...) cài bằng `npx skills add anhnx000/vietnamese-humanizer`. Skill chỉ là Markdown nên chạy được với mô hình nào mà editor của bạn đang dùng.

## Dùng

- Bật cho cả phiên: gõ `/vietnamese-humanizer`. Từ đó Claude trả lời theo quy tắc của skill, kể cả tin nhắn ngắn.
- Sửa một đoạn: `/vietnamese-humanizer <dán văn bản>`, hoặc nói "viết lại file docs/gioi-thieu.md cho bớt giọng AI".
- Skill cũng tự bật khi bạn nhờ soạn email, tin nhắn, bài đăng, PR mà bạn sẽ gửi dưới tên mình.
- Muốn bài giống giọng bạn hơn thì đưa kèm một đoạn văn bạn tự viết. Skill đọc nhịp câu, từ nối, cách xưng hô trong đó rồi viết theo.
- Gọi giọng bằng tên: *đời thường*, *công việc*, *kỹ thuật*, *ấm áp*, *thẳng*. Tên giọng chỉ đổi văn phong, không đổi xưng hô hay nội dung.
- Chỉ soi, không sửa: nhờ "soi giúp đoạn này" hoặc "audit". Skill liệt kê từng chỗ kèm số mục, lý do và gợi ý sửa ngắn, tách chỗ chắc chắn nên sửa với chỗ tùy người viết.
- Quét bằng dòng lệnh: `python3 -I skills/vietnamese-humanizer/scripts/scan.py file.md` in điểm 0-100 và từng chỗ khớp. Thêm `--json` để lấy kết quả dạng máy đọc, hoặc `--max 30` để thoát mã 1 khi điểm vượt ngưỡng, dùng cho CI hay pre-commit.
- Kiểm bản sửa còn giữ đúng dữ kiện: `python3 -I skills/vietnamese-humanizer/scripts/check_facts.py goc.md moi.md` báo lỗi khi số liệu, ngày giờ, link hay code bị mất hoặc bị thêm, và nhắc khi thiếu tên riêng.

Hai script chỉ dùng thư viện chuẩn của Python.

## Skill bắt những gì

Danh mục đầy đủ có 38 dấu hiệu, mỗi dấu hiệu kèm ví dụ trước/sau, nằm trong [references/patterns.md](skills/vietnamese-humanizer/references/patterns.md). Nhóm G dành riêng cho tiếng Việt:

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

Các nhóm còn lại áp cho cả tiếng Việt lẫn tiếng Anh: đối lập giả, câu chốt một dòng, bộ ba ép buộc, gạch ngang dài, thổi phồng, mượn uy tín mơ hồ, in đậm và emoji trang trí, lời chatbot, giải thích lại điều người đọc đã biết.

Skill cũng biết khi nào không nên sửa: giọng vùng miền, khẩu ngữ, thuật ngữ Hán Việt đúng chỗ, câu bị động trong tài liệu kỹ thuật, và các từ nhỏ làm đổi nghĩa như "vẫn", "chưa", "chỉ", "có thể" đều được giữ. Bài bạn tự viết thì skill chỉ sửa nhẹ.

## Nên biết

Skill không gửi gì ra ngoài, ngoài những gì agent của bạn vốn gửi cho mô hình. Skill gồm Markdown và hai script Python không cần thư viện ngoài, không gọi mạng, không thu thập dữ liệu, không cần tài khoản.

Điểm số chỉ để tham khảo, không phải phán quyết: điểm đo văn bản có bao nhiêu thói quen viết theo khuôn và câu có đều nhau không, không phải xác suất văn bản do AI viết. Có người vốn viết câu đều nhịp, và máy dò AI hay báo nhầm với người viết không phải tiếng mẹ đẻ. Điểm cao thì coi đó là danh sách chỗ cần đọc lại.

Skill giúp văn bản tự nhiên và dễ đọc hơn, nhưng không cam kết qua được máy dò AI, và không dùng mẹo lừa máy dò như lỗi chính tả cố ý hay ký tự ẩn. Đừng dùng nó để nộp bài thay người học hay giả danh người khác. Cũng đừng dùng danh sách dấu hiệu để kết luận ai đó dùng AI: người đoán bằng cảm giác cũng chỉ đúng hơn may rủi một chút.

## Cấu trúc

```text
skills/vietnamese-humanizer/
├── SKILL.md                 quy tắc chính, Claude nạp khi skill được gọi
├── references/patterns.md   38 dấu hiệu, ví dụ trước/sau
├── scripts/scan.py          máy quét có điểm 0-100, không cần thư viện ngoài
├── scripts/check_facts.py   kiểm bản sửa giữ đúng số liệu, ngày giờ, link, code
└── LICENSE-humanizer        giấy phép MIT của blader/humanizer
assets/                      mã QR ủng hộ
examples/                    văn mẫu trước/sau dùng trong README và test
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Đóng góp

Gặp một kiểu câu AI tiếng Việt mà skill chưa bắt, hoặc thấy skill sửa sai một câu vốn tự nhiên? Mở issue và dán câu đó vào, kèm bản bạn thấy đúng. Pull request thêm dấu hiệu mới nên có ví dụ trước/sau và một test trong `tests/test_scan.py`, gồm cả trường hợp không được báo nhầm.

## Ủng hộ

Vietnamese Humanizer miễn phí, giấy phép MIT, và sẽ luôn như vậy. Mình làm skill này vào thời gian rảnh. Nếu nó giúp bạn bớt thời gian sửa văn, một ly cà phê giúp mình giữ skill luôn mới:

- cập nhật danh mục khi mô hình mới ra, vì mỗi đời mô hình lại có bộ từ ưa dùng riêng;
- biến những câu các bạn báo thành test, đọc và trả lời issue, pull request;
- làm tốt thêm máy quét và công cụ kiểm dữ kiện.

<img src="assets/donate-vietqr.png" alt="Mã VietQR ủng hộ qua VPBank / Napas 247" width="220">

Quét bằng app ngân hàng bất kỳ hỗ trợ VietQR / Napas 247. Ghi nội dung chuyển khoản là "vietnamese-humanizer" để mình biết khoản ủng hộ đến từ đâu.

Không tiện ủng hộ tiền thì những việc này giúp không kém: thả ⭐ cho repo, giới thiệu cho người hay dùng AI viết tiếng Việt, hoặc mở issue kèm một câu skill sửa chưa đúng. Ủng hộ là lời cảm ơn, không phải phí hỗ trợ: issue của ai cũng được xem như nhau.

## Nguồn

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. Khung danh mục dấu hiệu dựa trên skill này.
- Các skill humanize tiếng Việt mã nguồn mở (MIT), dùng để đối chiếu danh mục; nội dung ở đây viết lại theo cách riêng: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Nguồn bài viết đầy đủ nằm cuối [SKILL.md](skills/vietnamese-humanizer/SKILL.md).
