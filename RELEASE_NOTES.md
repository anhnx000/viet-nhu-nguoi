# Release notes

English notes for each GitHub release. The release workflow publishes the section that matches the version in `SKILL.md`. The full development log, in Vietnamese, is in [CHANGELOG.md](CHANGELOG.md).

## 2.19.0

A search for more signs of AI writing in Vietnamese: one new rule, seven regression cases.

- Opus and GPT each wrote 24 everyday pieces without the skill (school essays, wedding toasts, shop captions, restaurant reviews, leave requests, cover letters, short stories). All 48 were read, alongside new Vietnamese articles and research. Every candidate sign got a case that ran on the current skill first.
- Letters to one person now pick "anh" or "chị" and use it throughout, with one line outside the letter telling the user to switch if needed. English only has "you", so models scattered "anh/chị" through the letter, four times in a leave request to a boss. New case `viet-email-nghi-phep`: 0/3 before, 3/3 after; seven other drafting cases still pass.
- Seven other signs were already handled, so they stay as regression cases with no new rule: stock memories any team shares, stories that mix southern names with northern food and scenery, "anh/chị" left in a ready-made email, customer replies built on translated English templates, therapy-speak in apologies, greetings that mention a card or gift the sender doesn't have, and recruitment clichés. The suite now has 78 cases.

## 2.18.0

A new sign drawn from how Turnitin checks for AI writing.

- Turnitin publishes no list of signs: its FAQ (November 2026) says a trained model scores each sentence and is not hand-coded for perplexity or burstiness. It does not check Vietnamese, and its paraphraser and humanizer detection covers English only. Paraphrased text tends to swap familiar words for odd synonyms, a sign Wikipedia also lists. The skill copies none of Turnitin's scoring and adds no tricks for getting past it.
- New pattern 67 (group M): one thing called by several names, and common phrases swapped for rare synonyms. Edit only when the new word is clearer; keep deliberate variation such as a full name followed by a short name.
- Two new cases were written and run on 2.17.0 first. The edit case passed 3/3 before and after. In the review case the old release found the problem but said all three times that the catalog had no item for it; the new release cites pattern 67 every time (0/3 to 3/3 on that check). The suite now has 70 cases.
- `evals/check.py` now counts pattern references written as "#45".

## 2.17.0

More lessons from mattpocock/skills, kept only where they measurably helped.

- PR descriptions now state when a change cannot be undone by a revert, such as a migration that drops columns or rewrites stored data (from the `pr` skill). New case `mo-ta-pr-xoa-cot`: 0/3 before, 3/3 after; the existing PR case stays 3/3 with no added warning.
- Two other ideas were tested first and needed no rule: reviewing a draft against its brief separately from its voice (`code-review`), and one question per line in emails that ask for answers (`to-questionnaire`). Release 2.16.0 already passed both new cases 3/3, so they stay as regression cases. The suite now has 68 cases.
- `AGENTS.md` adopts the `writing-for-agents` habit: write the case first, add a rule only if the current skill fails it, and phrase rules as what to do.

## 2.16.0

Back to MIT, with the credit link in the copyright line.

- `LICENSE` is MIT again. Its copyright line reads `Copyright (c) 2026 anhnx000 - https://github.com/anhnx000/viet-nhu-nguoi`, and MIT requires every copy to keep it, so forks carry a link to the original without the `NOTICE` and change-marking duties of Apache 2.0.
- `NOTICE` is removed. `LICENSE` still ships inside `skills/viet-nhu-nguoi/`.
- Release 2.15.0 remains available under Apache 2.0.

## 2.15.0

License change: MIT to Apache License 2.0, with attribution required.

- The repo is now under the Apache License 2.0 with a `NOTICE` file. Redistributions and derivative works (forks, translations, modified copies, products that include the skill, its catalog, checker or eval suite) must keep `NOTICE`, which credits the original project at https://github.com/anhnx000/viet-nhu-nguoi, and state which files were changed.
- `LICENSE` and `NOTICE` are also shipped inside `skills/viet-nhu-nguoi/`, since some installs copy only that folder.
- Releases up to 2.14.0 remain available under MIT. The parts adapted from blader/humanizer keep their MIT license in `LICENSE-humanizer`.
- Dependabot is no longer configured.

## 2.14.0

Teams chat replies: abbreviations the way Vietnamese office workers type, and no repeated requests.

- Before writing a chat reply, the skill rereads the sender's last three messages, including ones it drafted itself, and does not reuse a request, thank-you, sign-off or status line from them, even with a word or two changed. The bug came from a real Teams thread where four drafted messages in a row ended in "anh duyệt giúp em nha" (*please approve it for me*).
- On Teams, about half of the words that have a common short form get abbreviated (ko, đc, r, a, e...), at random spots. Names, numbers, links, MR numbers and technical terms stay as they are; messages to customers, partners or the whole company are not abbreviated.
- New catalog item 66, and three new Teams chat cases (two main, one held-out). `evals/check.py` gains `must_word` for whole-word matches of one- or two-letter abbreviations.
- Opus, medium effort, 3 runs each: the repeated-request case went from 0/3 on 2.13.0 to 3/3; the customer case stayed at 3/3 with no abbreviations; the held-out case went from 0/3 to 3/3. The 14 existing chat cases still pass.

## 2.13.0

Evals on real Codex, and fixes for three mistakes only Codex made.

- `evals/run.py --codex` runs each case through `codex exec` without MCP servers, plugins or personal skills, and stops early if the Codex sandbox cannot run a shell command or the workspace is out of credits. Ubuntu 24.04 needs an AppArmor profile for bubblewrap; see `evals/README.md`.
- The description now says the skill is not for code, factual or arithmetic questions. With the old description Codex (gpt-6.2-sol, medium) loaded the skill for 18/30 runs of 10 new near-miss prompts; with the new one, 0/20 on the same prompts, while should-trigger prompts stayed at 44/44. Claude never false-triggered and triggered on 48/48.
- Posts in the user's own name with no story, lessons or opinions of their own now get two to four questions instead of an invented draft. Already-natural casual messages are returned verbatim even when the user asks to "make it more natural".
- Codex, one run: 55/63 to 59/63 main cases, 7/13 to 10/13 held-out cases. Claude: 60/63 main, 10/13 held-out; the 11 drafting cases passed 33/33 runs after the final wording.

## 2.12.0

Trigger tests, a wider skill description, and a Codex-style eval mode.

- The description now mentions translating into Vietnamese and reports. On 16 new prompts written after the change, the skill triggered on 30/30 runs that should trigger (24/30 with the old description, which missed every translation prompt) and on 0/18 near-miss runs. On the 41 original prompts: 60/60 and 0/45.
- `evals/run.py --trigger` sends ordinary prompts without naming the skill; `check.py --trigger` counts runs where the skill was loaded. The trigger set has 21 should-trigger, 15 near-miss and 5 either-way prompts, plus 16 held-out ones.
- `run.py --kieu-codex` loads the skill the way Codex does (`.agents/skills/`, no Skill tool, Codex CLI 0.171 skill instructions, `$viet-nhu-nguoi`). The model is still Claude, because the Codex workspace was out of credits. One run: 58/63 main cases, 10/13 held-out cases, 20/20 triggers and no false triggers.

## 2.11.0

An automated, repeatable eval suite, new tells from 2025-2026 Vietnamese press coverage, and the checker measured on a few thousand news articles.

- `evals/run.py` runs each case through `claude -p` in an isolated temp folder (also `--khong-skill` for a no-skill baseline). `check.py` grades which reference files were read as a separate indicator and reports pass rates with Wilson 95% intervals over several runs. Every case has a reference answer that must pass; empty answers and copied inputs must fail. 11 new held-out cases (13 total).
- New tells merged into existing items: links ending in `utm_source=chatgpt.com`, references that cannot be found, "if you want, I can go deeper" offers, and phrases such as "mang trong mình", "bước tiến", "tầm nhìn chiến lược". Each was checked against 1,800 human news articles from before July 2022 and 2,000 AI rewrites ("không chỉ… mà còn": 0.9 vs 25.3 per 10,000 words). "Đồng thời" and "Từ đó" turned out to be more common in human text and were left out.
- Checker results: human news unchanged (3.2% score 10 or more); AI rewrites from 43.2% to 45.0%. The checker still misses more than half of AI news-style text. Fixed a regex that hung for minutes on long lines of repeated markers.
- `check_facts.py` treats "31/12" and "31/12/2026" as the same date. Already-natural casual messages are no longer "lightly fixed" for capitals and abbreviations.
- Results (Opus, medium effort, 3 runs): 181/189 runs pass on the 63 main cases (96%, CI 92-98%) vs 32/63 cases without the skill; held-out 34/39 runs after loosening six over-strict checks (23/39 before), vs 2/13 cases without the skill.

## 2.10.0

Load writing, editing, review, chat and slide guidance on demand. Look up a numbered pattern or check an existing presentation directly from the entry point.

## 2.9.0

Design lessons from the 20 most-starred skills on GitHub, a third pass over blader/humanizer, and author voice across sessions.

- Reuse a saved voice note for the right audience; keep sentences outside the requested edit verbatim; separate transcription, light editing and meeting summaries.
- From humanizer: why AI text converges (the model picks what fits the most readers), word habits change per model while structure persists, and every kept sentence must add something. Informal text (messages, comments, angry reviews) keeps its lowercase, abbreviations and bluntness; only leftover chatbot lines are removed.
- New tells: staging with "phần" ("Phần khó là..."), fake alternatives set up to be dismissed, closing "Nhìn chung" lines, chatbot offers, outlet lists and follower counts. More before/after examples across the catalog.
- A "rationalizations" table in `SKILL.md`, after superpowers and gstack, built from mistakes seen in the eval run.
- New messages put the recipient's action in the first sentence (after i-have-adhd); `evals/check.py` gains a `lead_keep` rule for it. A test ties every repo in the top-20 study to a concrete rule or eval case.
- Codex metadata in `agents/openai.yaml`; three new behavior cases (63 total); stricter whole-word matching in `evals/check.py`.
- Results: 62/63 cases and 2/2 held-out cases pass the automatic checks (Opus, medium effort, one run each); the only miss is a 364-word answer to a 300-word school essay. Manual reading found one regression, a missing notice about injected instructions, now required and checked automatically (3/3 reruns pass). Known issue: in the detector-evasion case the note still quotes removed phrases in 2 of 3 runs.

## 2.8.0

Route requests by editing intent, look up patterns by topic, and verify saved edits. Add held-out behavior cases and remove the skill word cap.

## 2.7.13

"Thang điểm 0-100" instead of "chấm 0-100".

- "Chấm 0-100" is a clipped calque of "scores 0-100"; Vietnamese says "chấm theo thang điểm 0-100". The repo description, READMEs, `SKILL.md`, plugin metadata, scanner docstrings and README images now use the full phrase.
- `scan.py` flags "chấm", "chấm điểm", "cho điểm" or "điểm số" right before a 0-5, 0-10, 0-100, 1-5, 1-10 or 1-100 range as translationese. It skips "thang điểm 0-100", ranges followed by "điểm" or "sao", and "cho" without "điểm". Fixture scores are unchanged.

## 2.7.12

Plain Vietnamese for "scanner" and "AI detector".

- The repo now calls `scan.py` "bộ kiểm tra" instead of "máy quét", a word-for-word translation of "scanner" that Vietnamese developers rarely use. AI detectors are "phần mềm kiểm tra AI". README images were redrawn, and `vi-du-may-quet.png` is now `vi-du-bo-kiem-tra.png`.
- `scan.py` flags calqued tool names as translationese: "máy dò AI", "máy quét AI", "máy dò đạo văn", and "máy quét" or "máy dò" next to verbs only software does ("chạy máy quét", "máy quét bắt được"). Document scanners, barcode scanners and metal detectors are not flagged. Fixture scores are unchanged.
- Catalog item 61 and the terminology rule in `SKILL.md` give "AI detector" as a term to keep in English.
- The git history was squashed into one commit and releases 2.7.7 to 2.7.11 were removed. If you cloned before 16 November 2026, `git pull` will fail; run `git fetch origin && git reset --hard origin/main` once (this discards local edits in that folder).

## 2.7.11

Section titles, and invented names in all examples.

- Catalog item 21 now covers section titles that do not say what the section holds: questions or mock dialogue, two parallel halves ("Where your data goes, what the score means"), unrelated topics joined by commas, a label plus colon, and chatty labels such as "Good to know". `SKILL.md` folds this into one rule and stays under 6,000 words. The scanner does not flag these yet.
- People, places and companies in examples, evals and tests now use invented names. The `chat-giong-nghe-an` eval is renamed `chat-giong-nghe`.
- Both READMEs use plainer section titles.
- New eval `sua-tieu-de-readme` (46 in total): a README with five such titles, to check that the assistant renames them. One Opus run at medium effort passed the automatic check and left the body unchanged.

## 2.7.10

A second pass over the same six posts.

- `scan.py` adds bait questions ("Nghe vô lý?", "X là gì mà...?"), runs of three or more clipped sentences on one line, and praise-before-the-point lead-ins ("Điều điên rồ nhất là:").
- New whole-document check for slang wrapped in scare quotes. Label detection now also covers "Label: sentence" lines without a bullet, unless a label repeats as speaker names do in chat logs.
- The six posts moved from 10, 5, 52, 29, 36, 65 to 10, 6, 53, 36, 37, 74. Held-out fixtures: 15.5 to 15.8 for 16 AI drafts, 1.3 unchanged for 6 human texts.
- Catalog examples extended, still 65 patterns. `SKILL.md` rules are unchanged.

## 2.7.9

Based on six AI-written Vietnamese tech posts that the scanner scored too low.

- `scan.py` has two new groups: clickbait wording ("thả bom", "cú sốc", "phá đảo" and similar) and an analogy attached to every point ("Giống...:" three or more times).
- Two new whole-document checks: whole words in capitals used for emphasis inside normal sentences, and unbolded "Label: sentence" bullets.
- False-contrast detection now covers "không còn là X mà là Y", "không nằm ở X, mà nằm ở Y" and a sentence opening with "Không phải vì X.". A closing heading with a leading emoji is recognised.
- The six posts moved from 8, 1, 25, 26, 25, 39 to 10, 5, 52, 29, 36, 65. On held-out fixtures the mean barely changed: 15.4 to 15.5 for 16 AI drafts, 1.3 unchanged for 6 pre-2022 human texts, none of which triggers a new group.
- `SKILL.md` gains one rule for news and tool-announcement posts. The catalog still has 65 patterns.

## 2.7.8

The skill now targets Vietnamese only.

- Removed the English AI-vocabulary list and the English examples from `SKILL.md` and the pattern catalog. English text still gets the structural rules, but there is no longer an English-specific section. `scan.py` is unchanged.
- New writing: the closing sentence is checked on its own. A sentence that interprets the story on the user's behalf is dropped unless the user said it.
- Chat replies: capitalization, end-of-message periods, commas and abbreviations follow the user's own messages instead of being corrected to standard spelling.
- Voice samples: when the sample uses em dashes, the new text uses them at the same rate.
- Added one more calque example to the translationese section ("fail silently").
- Evaluation with Claude Opus at medium effort, one run per prompt: 12 Vietnamese scenarios from `evals/` pass the automated checks, and 4 new prompts written for this release scored 0, 0, 0 and 10 on `scan.py`.

## 2.7.7

- `scan.py`, `check_facts.py` and `evals/check.py` now read and print UTF-8 on every platform. On Windows consoles using cp1252 they used to crash with `UnicodeEncodeError` at the first accented character. A regression test covers this.
- CI runs the tests on Python 3.10, 3.12 and 3.14 on Ubuntu, plus macOS and Windows, and smoke-tests `install.sh` in a temporary HOME on Ubuntu and macOS.
- A version bump pushed to `main` now publishes a GitHub release with a zip of the skill folder attached.
- Dependabot checks the GitHub Actions versions monthly.
