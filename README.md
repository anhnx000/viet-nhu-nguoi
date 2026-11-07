# Vietnamese Humanizer

[![test](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Skill cho [Claude Code](https://code.claude.com/docs/en/skills) giúp văn tiếng Việt do AI viết đọc lên giống người viết. Nó bỏ những thứ khiến người đọc nhận ra ngay là "con AI viết": "Trong bối cảnh hiện nay", "không chỉ... mà còn...", "được phát triển bởi", "tiến hành thực hiện việc", "một cách hiệu quả", "Hy vọng thông tin trên hữu ích!".

Tiếng Anh vẫn dùng được, nhưng phần làm kỹ nhất là tiếng Việt: văn dịch từ tiếng Anh, danh hóa "việc/sự", giọng công văn, xưng hô sai vai.

[English below](#english)

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

Máy quét đi kèm tìm được 16 dấu hiệu ở bản đầu, bản sau thì không còn dấu hiệu nào:

```text
$ python3 -I skills/vietnamese-humanizer/scripts/scan.py examples/truoc.md
16 dấu hiệu trong 5 dòng:
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

## Dùng

- Bật cho cả phiên: gõ `/vietnamese-humanizer`. Từ đó Claude trả lời theo quy tắc của skill, kể cả tin nhắn ngắn.
- Sửa một đoạn: `/vietnamese-humanizer <dán văn bản>`, hoặc nói "viết lại file docs/gioi-thieu.md cho bớt giọng AI".
- Skill cũng tự bật khi bạn nhờ soạn email, tin nhắn, bài đăng, PR mà bạn sẽ gửi dưới tên mình.
- Muốn bài giống giọng bạn hơn thì đưa kèm một đoạn văn bạn tự viết. Skill đọc nhịp câu, từ nối, cách xưng hô trong đó rồi viết theo.
- Chỉ quét, không sửa: `python3 -I skills/vietnamese-humanizer/scripts/scan.py file.md`. Script chỉ dùng thư viện chuẩn của Python.

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

## Không dùng để làm gì

Skill giúp văn bản tự nhiên và dễ đọc hơn, nhưng không cam kết qua được máy dò AI, và không dùng mẹo lừa máy dò như lỗi chính tả cố ý hay ký tự ẩn. Đừng dùng nó để nộp bài thay người học hay giả danh người khác. Cũng đừng dùng danh sách dấu hiệu để kết luận ai đó dùng AI: người đoán bằng cảm giác cũng chỉ đúng hơn may rủi một chút.

## Cấu trúc

```text
skills/vietnamese-humanizer/
├── SKILL.md                 quy tắc chính, Claude nạp khi skill được gọi
├── references/patterns.md   38 dấu hiệu, ví dụ trước/sau
├── scripts/scan.py          máy quét, không cần thư viện ngoài
└── LICENSE-humanizer        giấy phép MIT của blader/humanizer
examples/                    văn mẫu trước/sau dùng trong README và test
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Đóng góp

Gặp một kiểu câu AI tiếng Việt mà skill chưa bắt, hoặc thấy skill sửa sai một câu vốn tự nhiên? Mở issue và dán câu đó vào, kèm bản bạn thấy đúng. Pull request thêm dấu hiệu mới nên có ví dụ trước/sau và một test trong `tests/test_scan.py`, gồm cả trường hợp không được báo nhầm.

## Nguồn

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. Khung danh mục dấu hiệu dựa trên skill này.
- Các skill humanize tiếng Việt mã nguồn mở (MIT), dùng để đối chiếu danh mục; nội dung ở đây viết lại theo cách riêng: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Nguồn bài viết đầy đủ nằm cuối [SKILL.md](skills/vietnamese-humanizer/SKILL.md).

---

## English

A [Claude Code skill](https://code.claude.com/docs/en/skills) that makes AI-written Vietnamese read like a person wrote it. It also handles English, based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [blader/humanizer](https://github.com/blader/humanizer).

The Vietnamese-specific part targets what generic humanizers miss: calqued English passives ("được ... bởi"), "This/It" sentence openers translated literally, nominalisation with "việc/sự/một cách", empty bureaucratic verbs ("tiến hành thực hiện"), chains of "của", redundant pairs, and wrong or inconsistent pronouns of address, which in Vietnamese encode the relationship between writer and reader.

Install:

```text
/plugin marketplace add anhnx000/vietnamese-humanizer
/plugin install vietnamese-humanizer@vietnamese-humanizer
```

Then run `/vietnamese-humanizer` to turn it on for the session, or `/vietnamese-humanizer <text>` to rewrite a passage. The scanner (`skills/vietnamese-humanizer/scripts/scan.py`) uses only the Python standard library.

It does not promise to beat AI detectors and does not use detector-evasion tricks. MIT licensed.
