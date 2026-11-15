# Release notes

English notes for each GitHub release. The release workflow publishes the section that matches the version in `SKILL.md`. The full development log, in Vietnamese, is in [CHANGELOG.md](CHANGELOG.md).

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
