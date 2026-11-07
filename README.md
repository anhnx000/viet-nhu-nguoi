# Vietnamese Humanizer

[![test](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/vietnamese-humanizer/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**English** · [Tiếng Việt](README.vi.md)

![Before: AI-written Vietnamese scores 72/100. After: a plain human rewrite scores 0/100.](assets/banner.png)

> **Tiếng Việt:** skill chống giọng văn AI, sửa bài ChatGPT/Claude/Gemini viết cho tự nhiên như người Việt viết. Bỏ văn dịch, sáo rỗng, giọng công văn, lời chatbot; giữ đúng số liệu và xưng hô. Đọc [bản tiếng Việt](README.vi.md).
>
> *Chong giong van AI, humanize tieng Viet, viet lai van AI tu nhien, bo giong ChatGPT, viet nhu nguoi that.*

A [Claude Code skill](https://code.claude.com/docs/en/skills) that makes AI-written Vietnamese read like a person wrote it. It removes the phrases Vietnamese readers spot right away: "Trong bối cảnh hiện nay" (*in today's context*), "không chỉ... mà còn..." (*not only... but also...*), "được phát triển bởi" (*was developed by*), "tiến hành thực hiện việc" (*proceed to carry out the act of*), "Hy vọng thông tin trên hữu ích!" (*Hope this helps!*).

English works too, based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [blader/humanizer](https://github.com/blader/humanizer). Most of the work went into Vietnamese, because generic humanizers miss what makes Vietnamese AI text sound off: it reads like it was written in English and translated.

## Before and after

AI draft:

> Trong bối cảnh hiện nay, việc ứng dụng AI không chỉ là xu hướng mà còn là yếu tố then chốt giúp doanh nghiệp nâng tầm hiệu suất. Điều này được chứng minh bởi nhiều nghiên cứu chỉ ra rằng năng suất có thể tăng một cách đáng kể.
>
> Bên cạnh đó, đội ngũ của chúng tôi đã tiến hành thực hiện việc triển khai hệ thống mới nhằm mục đích mang lại trải nghiệm liền mạch cho khách hàng. Nó giúp việc quản lý dự án trở nên dễ dàng hơn, nhanh chóng hơn và hiệu quả hơn.
>
> Hy vọng những thông tin trên sẽ hữu ích cho bạn!

*Roughly: "In today's context, applying AI is not only a trend but also a key factor that elevates business performance. This is proven by many studies showing productivity can increase significantly. In addition, our team proceeded to carry out the deployment of a new system for the purpose of delivering a seamless experience. It makes project management easier, faster and more efficient. Hope this helps!"*

After the skill:

> Đội mình đã đưa hệ thống quản lý dự án mới vào dùng. Khách hàng giờ tự xem được tiến độ.

*"Our team started using the new project management system. Customers can now check progress themselves."*

The skill does not invent facts. If the text needs detail, it asks you, then writes with only what you gave it:

> Từ tháng 3, đội mình chuyển việc theo dõi dự án sang hệ thống mới. Khách hàng tự xem tiến độ, không phải nhắn hỏi như trước, và mỗi tuần đội bớt được khoảng nửa ngày làm báo cáo.

*"Since March we track projects in the new system. Customers check progress themselves instead of messaging us, and the team saves about half a day of reporting each week."*

The bundled scanner scores the draft 72/100 ("dense") with 16 tells, and both rewrites 0/100:

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

## Install

As a plugin, inside Claude Code:

```text
/plugin marketplace add anhnx000/vietnamese-humanizer
/plugin install vietnamese-humanizer@vietnamese-humanizer
```

Or clone and run the script. It symlinks the skill into `~/.claude/skills/`, so `git pull` updates it:

```bash
git clone https://github.com/anhnx000/vietnamese-humanizer.git
cd vietnamese-humanizer
bash install.sh          # symlink
bash install.sh --copy   # or copy, if you want to review each update before installing
```

Start a new Claude Code session afterwards.

Other agents (Cursor, Codex, Gemini CLI, OpenCode and more) can install it with `npx skills add anhnx000/vietnamese-humanizer`. The skill is plain Markdown, so it runs on whatever model your editor uses.

## Use

- Turn it on for the session: `/vietnamese-humanizer`. Claude then follows the rules in every reply, short ones included.
- Rewrite a passage: `/vietnamese-humanizer <paste text>`, or ask "rewrite docs/intro.md so it sounds less like AI".
- It also triggers when you ask Claude to draft an email, message, post or PR that you will send under your name.
- For a closer match to your voice, include a sample you wrote yourself. The skill picks up your sentence length, connectives and pronouns of address.
- Pick a voice by name: *đời thường* (casual), *công việc* (work), *kỹ thuật* (technical), *ấm áp* (warm), *thẳng* (blunt). The voice changes style only, never pronouns of address or content.
- Audit without rewriting: ask it to "soi" or "audit" a text. You get each tell with its pattern number, the reason and a short fix, split into clear problems and judgment calls.
- Scan from the command line: `python3 -I skills/vietnamese-humanizer/scripts/scan.py file.md` prints a 0-100 score and every match. Add `--json` for machine output, or `--max 30` to exit 1 above a threshold in CI or a pre-commit hook.
- Check that a rewrite kept the facts: `python3 -I skills/vietnamese-humanizer/scripts/check_facts.py original.md rewrite.md` fails if a number, date, time, link or code span was lost or added, and warns about missing proper names.

Both scripts use only the Python standard library.

## What it catches

The full catalog has 38 patterns, each with a before/after example, in [references/patterns.md](skills/vietnamese-humanizer/references/patterns.md) (written in Vietnamese). Group G is Vietnamese-only:

| Pattern | Example | Becomes |
| --- | --- | --- |
| Calqued passive | được phát triển bởi Google (*was developed by Google*) | Google phát triển (*Google developed*) |
| "This" / "It" openers | Điều này cho phép... (*This allows...*) | name the thing, or drop the subject |
| Nominalisation | Việc áp dụng AI giúp việc quản lý trở nên dễ dàng | Dùng AI thì quản lý dễ hơn |
| Empty verbs | tiến hành thực hiện việc rà soát (*proceed to carry out a review*) | rà soát (*review*) |
| Literal marketing calques | mở khóa tiềm năng (*unlock potential*), trải nghiệm liền mạch (*seamless experience*) | say what it actually does |
| Chains of "của" (*of*) | sự nâng cao của năng suất của nhân viên | nhân viên làm được nhiều hơn |
| Redundant pairs | hiện nay đang trong quá trình (*currently now in the process of*) | đang (*is*) |
| Pronouns of address | "bạn" in an email to your boss; mixing "bạn" and "quý vị" | one pair that fits the relationship |
| English glosses in brackets | hiệu suất (performance) | hiệu suất |

The other groups apply to both languages: false contrasts, one-line punchlines, forced triplets, em dashes, inflated significance, vague authorities, decorative bold and emoji, chatbot filler, and re-explaining what the reader already knows.

It also knows when to leave text alone: regional dialect, colloquial speech, Sino-Vietnamese terms used correctly, passives in technical docs, and small words that carry meaning such as "vẫn" (*still*), "chưa" (*not yet*), "chỉ" (*only*), "có thể" (*may*). Text you wrote yourself only gets a light edit.

## Good to know

Nothing leaves your machine beyond what your agent already sends to its model. The skill is Markdown plus two Python scripts with no dependencies, no network calls, no telemetry and no account.

The score is a stand-in, not a verdict. It measures how many template habits a text has and how uniform its sentences are; it is not the probability that AI wrote it. Some people write in a uniform rhythm, and detectors are known to misfire on non-native writers. Treat a high score as a list of places to reread.

The skill makes text more natural and easier to read. It does not promise to beat AI detectors and does not use evasion tricks such as deliberate typos or hidden characters. Don't use it to submit someone else's coursework or to impersonate anyone. And don't use the pattern list to accuse people of using AI: humans guessing by feel do only a little better than chance.

## Layout

```text
skills/vietnamese-humanizer/
├── SKILL.md                 main rules, loaded when the skill is invoked
├── references/patterns.md   38 patterns with before/after examples
├── scripts/scan.py          scanner with a 0-100 score, no third-party packages
├── scripts/check_facts.py   checks a rewrite kept numbers, dates, links and code
└── LICENSE-humanizer        MIT license of blader/humanizer
assets/                      donation QR code
examples/                    before/after samples used in the README and tests
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Contributing

Found a Vietnamese AI phrasing the skill misses, or a natural sentence it wrongly rewrites? Open an issue with the sentence and the version you think is right. Pull requests that add a pattern should include a before/after example and a test in `tests/test_scan.py`, including a case that must not be flagged.

## Support

Vietnamese Humanizer is free and MIT licensed, and it will stay that way. I maintain it in my spare time. If it saves you editing time, a coffee helps me keep it current:

- update the pattern list when new models bring new habits, since each model generation shifts its favourite words;
- turn the sentences you report into test cases, and review issues and pull requests;
- keep improving the scanner and the fact checker.

<img src="assets/donate-vietqr.png" alt="VietQR code for donations via VPBank / Napas 247" width="220">

The QR code works with any Vietnamese banking app (VietQR / Napas 247). A transfer note such as "vietnamese-humanizer" tells me where it came from.

Outside Vietnam, or rather not give money? These help just as much: star the repo, share it with someone who writes Vietnamese with AI, or open an issue with a sentence the skill got wrong. Donations are a thank-you, not payment for support: every issue gets the same attention.

## Credits

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. The pattern catalog structure is based on it.
- Open-source Vietnamese humanize skills (MIT), used for cross-checking the catalog; the text here is written independently: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- Full list of articles at the end of [SKILL.md](skills/vietnamese-humanizer/SKILL.md).

MIT licensed.
