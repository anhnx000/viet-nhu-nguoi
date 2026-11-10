# Viết như người · Vietnamese Humanizer

**Human voice for Vietnamese (chống giọng văn AI). Let AI draft it, and still sound like you.**

[![test](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml/badge.svg)](https://github.com/anhnx000/viet-nhu-nguoi/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Tiếng Việt](README.md) · **English**

![Before: AI-written Vietnamese scores 72/100. After: a plain human rewrite scores 0/100.](assets/banner.png)

AI drafts slides, emails and reports quickly, and Vietnamese readers spot the result just as quickly. The slide titles say "Tổng quan" (*Overview*) and "Thách thức" (*Challenges*). The email opens with "Trong bối cảnh hiện nay" (*in today's context*) and closes with "Hy vọng thông tin trên hữu ích!" (*Hope this helps!*). Fine for a team chat. For your boss or a customer, you end up rewriting it by hand.

Viết như người ("write like a person") is a skill, a small add-on, for Claude and other AI assistants. Once installed, the assistant writes Vietnamese the way a working person does: slide titles that state the conclusion, emails with the right pronouns of address, short sentences, and your numbers left exactly as you gave them. Free and open source.

English works too, based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [blader/humanizer](https://github.com/blader/humanizer). Most of the work went into Vietnamese, because generic humanizers miss what makes Vietnamese AI text sound off: it reads like it was written in English and translated.

**Jump to:** [Install, no coding needed](#install-in-a-few-minutes-no-coding-needed) · [Everyday use](#everyday-use) · [Before and after](#before-and-after) · [What it catches](#what-it-catches) · [Command line](#for-command-line-users) · [Buy me a coffee](#buy-me-a-coffee)

## What people use it for

- Report and proposal decks: every title is a conclusion, so reading the titles alone tells your manager what to decide. Missing numbers are marked `[cần xác nhận]` (*to confirm*), never made up.
- Emails to a boss or a customer: the right pronouns of address (anh/chị/em, quý khách) instead of a default "bạn", and the request comes first.
- Reports and documents translated from English: no more calqued sentences such as "được... bởi" (*was ... by*) or "Điều này cho phép" (*This allows*).
- Facebook, LinkedIn and blog posts: AI drafts, the voice stays yours, and the post tells one story instead of covering everything.
- A check before you send: it points at the places that sound like AI, and you decide what to change.

## Install in a few minutes, no coding needed

You don't type any commands. You ask your AI assistant to install it, the way you would ask a colleague from IT.

**Step 1. Open an AI assistant that runs on your computer.** For example the Claude Code desktop app (point and click, no terminal window), or Codex, Cursor, Gemini CLI, OpenCode. The web chat versions of Claude and ChatGPT cannot install anything on your machine, so you need one of these.

**Step 2. Paste this into the chat box:**

> Install the viet-nhu-nguoi skill for me from https://github.com/anhnx000/viet-nhu-nguoi

**Step 3. Click approve** when the assistant asks permission to download and install. It usually takes under a minute.

**Step 4. Start a new conversation and try it:**

> Viết như người: soạn giúp tôi email xin sếp lùi hạn nộp báo cáo 3 ngày, xưng em

(*"Write like a person: draft an email asking my boss for three more days on the report; I address myself as em."*) If the email comes back short, leads with the request and keeps "em" all the way through, the skill is working.

A few things you may want later. Again, just say them to the assistant:

| You want to | You type |
| --- | --- |
| Check it is installed | "Do I have the viet-nhu-nguoi skill installed?" |
| Get the latest version | "Update the viet-nhu-nguoi skill to the latest version" |
| Remove it | "Uninstall the viet-nhu-nguoi skill" |

Did the assistant hit an error? Take a screenshot and [open an issue](https://github.com/anhnx000/viet-nhu-nguoi/issues). I'll take a look.

<details>
<summary>For an AI assistant that was asked to install this skill</summary>

The user is not technical, so do all of it yourself and only ask for permission to run commands. Try these in order and stop at the first that works:

1. `npx` is available: run `npx skills add anhnx000/viet-nhu-nguoi -g -y`.
2. `git` and `bash` are available (macOS, Linux, WSL): `git clone https://github.com/anhnx000/viet-nhu-nguoi.git ~/viet-nhu-nguoi && bash ~/viet-nhu-nguoi/install.sh --copy`.
3. Windows without bash, or no git: download `https://github.com/anhnx000/viet-nhu-nguoi/archive/refs/heads/main.zip`, unzip it, and copy the `skills/viet-nhu-nguoi` folder into the agent's user-level skills folder (Claude Code: `~/.claude/skills/viet-nhu-nguoi`, which on Windows is `%USERPROFILE%\.claude\skills\viet-nhu-nguoi`).

Afterwards, check that `SKILL.md` sits in the target folder, tell the user where it was installed, and suggest a new conversation if the skill does not show up. To update, repeat the method you used; for methods 2 and 3, delete the old folder first. To uninstall, delete the `viet-nhu-nguoi` folder from the skills folder.

</details>

<details>
<summary>For people comfortable with a terminal: install by hand</summary>

As a plugin, inside Claude Code:

```text
/plugin marketplace add anhnx000/viet-nhu-nguoi
/plugin install viet-nhu-nguoi@viet-nhu-nguoi
```

Or clone and run the script. It symlinks the skill into `~/.claude/skills/`, so `git pull` updates it:

```bash
git clone https://github.com/anhnx000/viet-nhu-nguoi.git
cd viet-nhu-nguoi
bash install.sh          # symlink
bash install.sh --copy   # or copy, if you want to review each update before installing
```

Start a new Claude Code session afterwards.

Other agents (Cursor, Codex, Gemini CLI, OpenCode and more) can use the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add anhnx000/viet-nhu-nguoi      # current project only
npx skills add anhnx000/viet-nhu-nguoi -g   # every project (user level)
```

It asks which agents to install for; pass `-a claude-code` (or `-a '*'`) and `-y` to skip the prompts. The skill is plain Markdown, so it runs on whatever model your editor uses.

</details>

## Everyday use

Talk to it the way you would brief a colleague. There is no syntax to remember, and you can ask in Vietnamese or English.

| You type | What the skill does |
| --- | --- |
| "Làm slide báo cáo tiến độ dự án tuần này để sếp duyệt" (*make this week's progress deck for my boss to approve*) | Asks first: who is watching, what they must decide, presented live or sent to read. Then builds the deck |
| "Sửa file bao-cao-q3.pptx cho bớt giọng AI" (*make this deck sound less like AI*) | Reads the text and speaker notes on every slide, fixes titles, bullets and notes |
| "Viết email xin sếp lùi deadline 3 ngày, xưng em" (*email my boss for a three-day extension*) | Writes a short email, request first, with "em"/"anh" kept consistent throughout |
| "Viết bài Facebook kể về dự án của mình, khoảng 300 chữ" (*a 300-word Facebook post about my project*) | Asks you for one or two things that really happened, then tells one story. No section headings, no background lecture |
| "Soi giúp đoạn này chỗ nào giọng AI" (*where does this sound like AI?*) | Lists each spot with the reason and a short fix, and rewrites nothing |
| Paste an email you wrote yourself | Picks up your sentence length, connectives and pronouns, then writes to match |

Four habits that make the output much better:

1. Say who will read it and who you are to them. "To my department head, I'm em" produces a different email from "to a customer, we are chúng tôi".
2. Paste a passage you wrote yourself, the same kind of text as the one you need. The skill copies your sentence length and the words you favour.
3. Give it the real numbers, names and dates. If something is missing it asks or leaves a blank; it does not make things up.
4. When a phrase feels off, say "mình không nói thế" (*I don't talk like that*). It adjusts and remembers for the rest of the conversation.

More ways to call it:

- Type `/viet-nhu-nguoi` to turn it on for the session. Every reply then follows the rules, short ones included.
- It also triggers by itself when you ask for an email, message or post that you will send under your name.
- Pick a voice by name: *đời thường* (casual), *công việc* (work), *kỹ thuật* (technical), *ấm áp* (warm), *thẳng* (blunt). The voice changes style only; pronouns of address and content stay put.
- Text you wrote yourself only gets a light edit.

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
```

### A long post

This example is why version 2.2 exists. [The original post](examples/bai-dang-truoc.md) runs 1,740 Vietnamese words under nine all-caps headings. It had already dropped the familiar AI vocabulary, so the old scanner scored it 3/100. Readers still spotted it at once, because it repeats the same few moves all the way down:

> Nói cho thật: tiến độ không dễ. [...] Khó nhất không phải là code, mà là chọn việc gì để làm. [...] Mình không cần bạn giỏi kernel. Mình cần bạn kiên nhẫn đọc log.

*"To be honest: progress isn't easy. [...] The hardest part isn't the code, it's choosing what to work on. [...] I don't need you to be good at kernels. I need you to be patient with logs."*

Version 2.2 counts across the whole text and scores it 55/100: ten "not X but Y" frames, six voice labels such as "nói gọn" (*put briefly*) and "nói cho thật" (*to be honest*), and a colon in 20 of 88 sentences. [The rewrite](examples/bai-dang-sau.md) is 376 words, does one job (inviting people to join the project) and scores 0/100. It adds no fact that the original lacks. The operating-system primer, the microkernel history and the security statistics are left for other posts.

## What it catches

The full catalog has 53 patterns, each with a before/after example, in [references/patterns.md](skills/viet-nhu-nguoi/references/patterns.md) (written in Vietnamese). Group I covers what only shows across a whole post after each sentence is clean: voice labels ("nói gọn", "nói cho thật:"), the same contrast frame used three times or more, a punchline closing every paragraph, colons everywhere, a post that covers everything. Group G is Vietnamese-only:

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

Group H covers slides and long documents (see below). The other groups apply to both languages: false contrasts, one-line punchlines, forced triplets, em dashes, inflated significance, vague authorities, decorative bold and emoji, chatbot filler, and re-explaining what the reader already knows.

It also knows when to leave text alone: regional dialect, colloquial speech, Sino-Vietnamese terms used correctly, passives in technical docs, and small words that carry meaning such as "vẫn" (*still*), "chưa" (*not yet*), "chỉ" (*only*), "có thể" (*may*). Text you wrote yourself only gets a light edit.

## Slides and talks

AI-made slides give themselves away before anyone reads a sentence: titles like "Tổng quan" (*Overview*) and "Thách thức" (*Challenges*), exactly three bullets on every slide, speaker notes that read like a memo. The skill has a separate guide for this ([references/slides.md](skills/viet-nhu-nguoi/references/slides.md), in Vietnamese):

- Gather context before building a deck: who watches, what they must decide, presented live or sent to read.
- Write the storyline as titles first. Each title is a conclusion, and the titles read top to bottom form one argument.
- One message per slide. Missing numbers are marked `[cần xác nhận]` (*to confirm*), never invented.
- Speaker notes are written to be spoken: short sentences, no brackets, saying what the slide doesn't.
- A fresh agent with no context reads the deck and scores it on seven criteria (out of 70); its feedback goes into an accept/reject table for you to decide.

The scanner reads `.pptx` files directly (slide text, tables and speaker notes) and reports by slide:

```text
$ python3 -I skills/viet-nhu-nguoi/scripts/scan.py examples/slide-truoc.pptx
Điểm 48/100 (nhiều dấu hiệu): 21 dấu hiệu trong 7 slide, 176 chữ.
[từ vựng AI (vi)] 7
[tiêu đề dạng nhãn] 4        slide 2: Tổng quan, slide 3: Thách thức, slide 5: Lợi ích, slide 6: Kết luận
[hứa suông] 1                slide 5, ghi chú: chi tiết sẽ được trao đổi sau
[tiêu đề đếm số ý] 1         slide 4: 3 trụ cột giải pháp
[câu khó nói (ghi chú)] 1    slide 2, ghi chú: Như chúng ta có thể thấy, ...
[số gạch đầu dòng đều] 1     5/5 slide có đúng 3 ý
...

$ python3 -I skills/viet-nhu-nguoi/scripts/scan.py --titles examples/slide-sau.pptx
 1. Đề xuất thuê thêm 1 QA cho quý 1/2027
 2. Quý 3 trễ 2 tuần, cả 2 lần đều do thiếu người test
 3. Thuê 1 QA rẻ hơn tiếp tục trễ
 4. Cần anh duyệt trước 30/11 để kịp tuyển
```

The rewrite scores 0/100, and the four titles alone tell the whole proposal (*hire one QA for Q1 2027; Q3 slipped two weeks, both times for lack of testers; one QA costs less than more delays; please approve by 30/11 so hiring finishes in time*).

## For command-line users

Both scripts use only the Python standard library.

- Score a file: `python3 -I skills/viet-nhu-nguoi/scripts/scan.py file.md` (or `file.pptx`) prints a 0-100 score and every match. Add `--json` for machine output, or `--max 30` to exit 1 above a threshold in CI or a pre-commit hook. Add `--titles` to print only the headings or slide titles, in order, or `--text` to dump every slide's text and notes from a `.pptx`.
- Check that a rewrite kept the facts: `python3 -I skills/viet-nhu-nguoi/scripts/check_facts.py original.md rewrite.md` (also reads `.pptx`) fails if a number, date, time, link or code span was lost or added, and warns about missing proper names.

## Good to know

Nothing leaves your machine beyond what your agent already sends to its model. The skill is Markdown plus two Python scripts with no dependencies, no network calls, no telemetry and no account.

The score is a stand-in, not a verdict. It measures how many template habits a text has and how uniform its sentences are; it is not the probability that AI wrote it. Some people write in a uniform rhythm, and detectors are known to misfire on non-native writers. Treat a high score as a list of places to reread.

The skill makes text more natural and easier to read. It does not promise to beat AI detectors and does not use evasion tricks such as deliberate typos or hidden characters. Don't use it to submit someone else's coursework or to impersonate anyone. And don't use the pattern list to accuse people of using AI: humans guessing by feel do only a little better than chance.

## Layout

```text
skills/viet-nhu-nguoi/
├── SKILL.md                 main rules, loaded when the skill is invoked
├── references/patterns.md   53 patterns with before/after examples
├── references/slides.md     slides, speaker notes, fresh-reader test
├── references/sources.md    references: articles, research, style guides, other skills
├── scripts/scan.py          scanner with a 0-100 score, no third-party packages
├── scripts/check_facts.py   checks a rewrite kept numbers, dates, links and code
├── scripts/slides.py        reads slide text and notes from .pptx, standard library only
└── LICENSE-humanizer        MIT license of blader/humanizer
assets/                      banner and the coffee QR code
examples/                    before/after text and .pptx decks used in the README and tests
tests/test_scan.py           python3 -m unittest discover -s tests
```

## Contributing

Found a Vietnamese AI phrasing the skill misses, or a natural sentence it wrongly rewrites? Open an issue with the sentence and the version you think is right. Pull requests that add a pattern should include a before/after example and a test in `tests/test_scan.py`, including a case that must not be flagged.

<a id="support"></a>

## Buy me a coffee

Viết như người is free and MIT licensed, and it will stay that way. I maintain it in my spare time. If it saves you an evening of rewriting, you can buy me a cà phê sữa đá, Vietnamese iced coffee with condensed milk.

<table>
  <tr>
    <td width="250" align="center">
      <img src="assets/donate-vietqr.png" alt="VietQR code to buy the author a coffee via VPBank / Napas 247" width="220">
    </td>
    <td>
      <b>Scan with any Vietnamese banking app</b> (VietQR / Napas 247).<br><br>
      Any amount is welcome. One coffee makes my day.<br><br>
      Put <code>viet-nhu-nguoi</code> in the transfer note so I know where the coffee came from.
    </td>
  </tr>
</table>

Coffee money turns into time for three things:

- updating the pattern list when new models bring new habits, since each model generation shifts its favourite words;
- turning the sentences you report into test cases, and reviewing issues and pull requests;
- improving the scanner and the fact checker.

Outside Vietnam, or the QR code is no use to you? These are worth just as much: star the repo, share it with someone who writes Vietnamese with AI, or open an issue with a sentence the skill got wrong. Coffee or no coffee, every issue gets the same attention.

## Credits

- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [blader/humanizer](https://github.com/blader/humanizer), MIT, Copyright (c) 2025 Siqi Chen. The pattern catalog structure is based on it.
- Open-source Vietnamese humanize skills (MIT), used for cross-checking the catalog; the text here is written independently: [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer), [andyluu98/vn-humanize](https://github.com/andyluu98/vn-humanize), [cuongducle/viet-humanize](https://github.com/cuongducle/viet-humanize), [pdh372/humanize-vietnamese](https://github.com/pdh372/humanize-vietnamese).
- The slide guidance borrows ideas, rewritten in our own words, from [carnot-tech/jinba-consulting-pptx-skill](https://github.com/carnot-tech/jinba-consulting-pptx-skill) (MIT), [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) (MIT) and the `doc-coauthoring` skill in [anthropics/skills](https://github.com/anthropics/skills) (Apache 2.0).
- Full reference list (in Vietnamese), covering articles, Vietnamese linguistics, research on detector reliability, style guides and other skills, and marking which ones the skill builds on directly: [references/sources.md](skills/viet-nhu-nguoi/references/sources.md).

MIT licensed.
