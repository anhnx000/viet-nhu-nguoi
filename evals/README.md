# Bộ đề thử skill

`scenarios.json` có 68 tình huống thường gặp, dùng khi chỉnh skill. `held-out.json` có 14 đề để riêng, chỉ chạy trên bản đã chốt. Mỗi đề có `tin_nhan` là lời người dùng, `tep` (nếu có) là file đầu vào, `mong_doi` là điều người đọc cần thấy trong câu trả lời, `kiem` là phần script đếm được. `trigger.json` có 41 lời nhờ để thử skill có tự bật đúng lúc không, `trigger-held-out.json` có 32 lời nhờ để riêng cho phần này. File trong `inputs/` là văn viết ra để thử, tên người và số liệu đều bịa.

## Chạy

```bash
python3 -I evals/run.py evals/results/<bản> --runs 3            # 68 đề, mỗi đề 3 lượt
python3 -I evals/run.py evals/results/<bản>-held-out --held-out --runs 3
python3 -I evals/run.py evals/results/<bản>-khong-skill --khong-skill   # cùng đề, không bật skill
python3 -I evals/run.py evals/results/trigger-<bản> --trigger --runs 3   # skill có tự bật đúng lúc không
python3 -I evals/run.py evals/results/<bản>-codex --kieu-codex           # nạp skill theo cách của Codex
python3 -I evals/run.py evals/results/<bản>-codex-that --codex            # chạy thật trên Codex CLI
python3 -I evals/run.py evals/results/<bản>-sonnet --model sonnet --skill-dir <thư mục>   # thử một bản skill khác, ví dụ bản dịch
```

`run.py` gọi `claude -p` cho từng đề trong một thư mục tạm ngoài repo. Thư mục đó chỉ có bản sao skill và file đầu vào. Lệnh chỉ nạp cài đặt của thư mục ấy, không nạp MCP, nên skill cá nhân và plugin đã cài trên máy không lẫn vào. Mỗi lượt ghi lại danh sách skill, plugin đã nạp để kiểm. Trợ lý được đọc file, chạy ba script của skill và ghi file nháp vào `/tmp`, không ghi được vào file đầu vào. Mặc định dùng Opus mức medium. Lệnh chạy lại sẽ bỏ qua đề đã có câu trả lời, nên hết hạn mức giữa chừng thì chạy lại đúng lệnh cũ. Kết quả thô nằm trong `evals/results/` (đã có trong `.gitignore`).

## Chấm

```bash
python3 -I evals/check.py evals/results/<bản> [--held-out]
```

Phần nội dung quyết định đề qua hay trượt, gồm số chữ, cụm phải giữ, cụm cấm, số liệu tự thêm, điểm `scan.py`. Đường đọc (`must_read`, `must_not_read`, `max_refs`, tức trợ lý có mở đúng file trong `references/` không) chấm riêng thành một chỉ số, không làm đề trượt, vì câu trả lời đúng thì quan trọng hơn đường đi tới nó. Đường đọc vẫn đáng xem, vì nó cho biết câu trả lời đúng là nhờ skill hay nhờ mô hình tự biết.

Thư mục có nhiều lượt (`1/`, `2/`, `3/`) thì báo tỉ lệ lượt qua kèm khoảng tin cậy 95% (Wilson), và số đề qua cả ba lượt. Ba lượt qua cả ba chỉ cho biết tỉ lệ thật của đề đó nằm trong khoảng 44-100%, nên đừng đọc một đề trượt một lượt thành hỏng: đọc câu trả lời trước, rồi xem điều kiện chấm. Hai bản so với nhau thì so từng đề.

Sau phần tự động, đọc tay từng câu trả lời theo `mong_doi`, xem giọng có tự nhiên không, ghi chú có ngắn không, có chi tiết nào bịa không.

## Đáp án mẫu

Mỗi đề có một đáp án mẫu trong `dap-an/<id>.md`, phải qua `check.py`. `tests/test_package.py` kiểm điều này, và kiểm thêm chiều ngược lại: câu trả lời rỗng phải trượt mọi đề, chép nguyên file đầu vào phải trượt mọi đề có file (trừ ba đề mà bản gốc vốn đã tự nhiên). Sửa `kiem` mà đáp án mẫu trượt thì xem lại điều kiện trước khi sửa đáp án.

## Đề để riêng

Chỉ dùng lỗi ở `scenarios.json` để sửa skill. Đề trong `held-out.json` chạy sau khi đã chốt bản. Nếu dùng một đề để riêng làm căn cứ sửa skill, chuyển nó sang `scenarios.json` và viết đề mới thay vào.

## Thêm đề

Thêm một mục vào `scenarios.json` và một đáp án mẫu. Điều kiện trong `kiem` nên lỏng vừa đủ: câu trả lời đúng mà viết khác đi một chút thì vẫn phải qua. Đừng đặt `must_not` cho cụm mà trợ lý có thể trích lại trong ghi chú ("mình đã bỏ câu ..."), khi đó dùng `max_overlap`. `lead_keep` dùng cho tin có việc nhờ: dữ kiện phải nằm trong 25 chữ đầu. `must_word` tìm chữ đứng riêng, dùng cho chữ tắt một hai ký tự như "a", "r", "ko", vì `must_keep` sẽ khớp nhầm "a" trong "anh". `max_added_numbers` không dùng cho đề có nguồn tiếng Anh, vì "March 1, 2027" và "1/3/2027" bị tính là hai số khác nhau.

## Skill có tự bật đúng lúc không

Người dùng thường không gõ `/viet-nhu-nguoi`, nên skill chỉ có ích khi trợ lý tự nhận ra lời nhờ cần đến nó. `trigger.json` chia lời nhờ làm ba loại:

- 21 lời nhờ nên bật: soạn email, tin nhắn, mô tả PR, slide, lời phát biểu, dịch sang tiếng Việt, soi hay sửa văn có giọng máy, cả lời nhờ tiếng Anh sửa bài cho bớt giọng AI.
- 15 lời nhờ gần giống mà không nên bật: dịch sang tiếng Anh, hỏi kiến thức bằng tiếng Việt, code có chữ Việt, đếm chữ trong file văn bản, tóm tắt tiếng Anh.
- 5 lời nhờ để tùy (`"bat": null`), như soát chính tả, commit message, tóm tắt cho chính người hỏi.

`run.py --trigger` gửi lời nhờ như người dùng gõ thường và dừng sau 4 bước, `check.py --trigger` đếm số lượt trợ lý gọi skill hoặc mở `SKILL.md`. Thư mục chạy thử có sẵn khoảng 20 skill dựng sẵn của Claude Code bên cạnh skill này, nhưng máy người dùng thường có nhiều skill hơn, nên tỉ lệ bật thật có thể thấp hơn. Sửa `description` theo kết quả thì viết lời nhờ mới để báo kết quả, đừng dùng lại lời nhờ đã dùng để sửa.

## Kiểu Codex

`--kieu-codex` để skill ở `.agents/skills/`, bỏ công cụ Skill và thêm vào lời nhắc hệ thống phần hướng dẫn skill chép từ Codex CLI 0.171 (danh sách skill kèm đường dẫn, luật "tên skill được nhắc hoặc việc khớp mô tả thì phải dùng, đọc trọn `SKILL.md`, đường dẫn tương đối tính từ thư mục skill"). Lời nhờ mở bằng `$viet-nhu-nguoi` như cách gọi trong Codex. Mô hình vẫn là Claude, nên chế độ này chỉ thử phần skill mang sang được: đường dẫn, cách tìm file trong `references/`, script, khi không có công cụ Skill. Muốn thử mô hình GPT thì dùng `--codex`.

## Chạy trên Codex

```bash
python3 -I evals/run.py evals/results/<bản>-codex-that --codex
python3 -I evals/run.py evals/results/trigger-<bản>-codex-that --codex --trigger
```

`--codex` gọi `codex exec` với mô hình và mức suy luận trong `~/.codex/config.toml` (ghi `--model`, `--effort` để đổi). Skill nằm ở `.agents/skills/` của thư mục tạm. Lệnh không nạp `config.toml` (nên không có MCP), tắt plugin, app, trình duyệt, hook, và tắt các skill cá nhân trong `~/.codex/skills` và `~/.agents/skills`, chỉ còn skill hệ thống của Codex nằm cạnh. Lệnh shell chạy trong sandbox `workspace-write` của Codex. Trước khi chạy cả bộ, `run.py` nhờ Codex `cat` một file có chuỗi ngẫu nhiên. Nếu shell không chạy, script dừng ngay, vì khi đó Codex không đọc được skill lẫn file đầu vào mà vẫn trả lời như thường, kiểu "bạn dán nội dung vào đây nhé".

Trên Ubuntu 24.04 trở lên, sandbox của Codex thường hỏng với lỗi `bwrap: setting up uid map: Permission denied` hay `bwrap: loopback: Failed RTM_NEWADDR`, vì AppArmor chặn chương trình chưa có profile tạo user namespace (`kernel.apparmor_restrict_unprivileged_userns = 1`). Cách thường dùng là cho riêng bubblewrap một profile:

```bash
BWRAP="$(npm root -g)/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-resources/bwrap"
sudo tee /etc/apparmor.d/codex-bwrap >/dev/null <<EOF
abi <abi/4.0>,
include <tunables/global>
profile codex-bwrap "$BWRAP" flags=(unconfined) {
  userns,
}
profile system-bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
}
EOF
sudo apparmor_parser -r /etc/apparmor.d/codex-bwrap
```

Đã thử trên Ubuntu 24.04.5 với Codex CLI 0.171: sau khi nạp profile, sandbox `workspace-write` chạy được lệnh shell, kể cả khi chính Codex được gọi từ trong sandbox của Claude Code. Profile này nới giới hạn của Ubuntu cho đúng hai file bubblewrap. Cài lại Codex bằng npm ở chỗ khác thì đường dẫn đổi, phải sửa profile. Không muốn đụng AppArmor thì có thể chạy với `--codex-sandbox danger-full-access`: lệnh của Codex không còn sandbox, chỉ nên làm khi tự chạy và đã đọc các file trong `inputs/`.

Cách chấm dựa theo:

- Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): đáp án mẫu, chấm kết quả trước đường đi, pass^k.
- [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825): câu trả lời rỗng phải trượt.
- [Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints](https://arxiv.org/abs/2503.01747): khoảng tin cậy Wilson khi ít đề.
- [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): đo cả khi không bật skill.

## Thử giọng qua hai phiên

Ở phiên đầu, nhờ lưu giọng cho bản tin nội bộ vào một file tạm. Cho một câu mẫu có số liệu và dặn chỉ xưng “tụi mình” khi viết cho đồng nghiệp. Mở phiên mới, đưa đường dẫn file và một sự việc khác. Nhờ viết tin cho đồng nghiệp và cho khách. Đọc cả hai tin, kiểm tra đối tượng nào được xưng “tụi mình” và có chi tiết cũ nào lọt sang bài mới.

Để thử lời chỉnh giữa cuộc trò chuyện, mở một phiên khác. Lượt đầu dặn “Trong nhóm chạy bộ gọi mình là Nam thay vì anh”. Lượt sau nhờ báo chị Hà bên kế toán là mình đã gửi bảng lương, xưng em gọi chị. Kiểm tra tin gửi chị Hà có giữ đúng vai và bỏ qua cách gọi của nhóm chạy bộ hay không.

## Đọc kết quả

Mô hình trả lời mỗi lần một khác, nên một đề trượt một lượt thì đọc câu trả lời trước, rồi chạy lại vài lượt nếu cần. Lượt chạy đủ đầu tiên của bản 2.7.0 trên Claude Opus mức medium có 13 đề qua, ba đề còn lại trượt vì điều kiện chấm đặt quá chặt chứ câu trả lời thì đúng: viết "9h tối" thay cho "21h", dẫn số mục kiểu "(45, 3)" không kèm chữ "mục", để `[Họ tên]` chờ người dùng điền. Điều kiện đã nới theo ba chỗ đó, chấm lại thì cả 16 đề qua. Đề thứ mười bảy (một ý gửi ba người nhận) thêm sau, rút từ lần thử phần cá nhân hóa trên tin nhắn thật. Bản 2.7.1 gọt hai chỗ trùng lặp trong `SKILL.md` rồi chạy lại đủ 17 đề, cả 17 qua phần tự động và phần đọc tay. Chín đề cuối thêm ở bản 2.7.1 cho những phần chưa có đề nào thử: mẫu giọng có gạch ngang dài, giọng gọi tên, tài liệu kỹ thuật có code, tin viết từ nguồn tiếng Anh, daily report, mô tả PR, bài dài quá mức của kênh, yêu cầu qua được phần mềm kiểm tra AI, bài nộp cho trường. Lượt đầu cả chín đều qua, chạy thêm lượt hai (bốn đề cần phán đoán chạy cả lượt ba) cũng vậy. Riêng đề mẫu giọng, đọc tay thấy trợ lý hay tự thêm một câu cảm nghĩ, bản 2.7.2 đã sửa. Một tình huống thử tay mà không đưa vào bộ đề vì `check.py` chỉ đọc câu trả lời: nhờ sửa thẳng vào file có front matter và khối lệnh (file sửa xong còn nguyên code, link, phiên bản). Ba đề viết mới thiếu chuyện riêng là chỗ bản 2.6.1 trượt (trả bài khung có 4-19 chỗ trống thay vì hỏi lại).

Năm đề `chat-giong-*` thử phần cá nhân hóa trên năm giọng khác nhau (miền Tây, giọng Nghệ, sinh viên viết tắt, cô giáo viết trang trọng, dân văn phòng chêm tiếng Anh). Năm đoạn chat đó do một mô hình không bật skill viết, lời dặn thì cố ý xưng "tôi" và viết trang trọng để xem tin trả lời theo giọng mẫu hay theo giọng lời dặn. Lượt đầu cả năm đúng giọng mẫu.

Ba đề `luot-hai-*` thử lượt hai của chế độ viết mới: người dùng đã trả lời các câu skill hỏi, giờ skill phải viết bài từ đúng những gì họ kể. Phần đọc tay ở ba đề này là chỗ quan trọng nhất: bài có thêm cảnh, lời thoại hay cảm nghĩ nào người dùng chưa kể không.

Tám đề `spoken-*` thử sắc thái lời nói: trợ từ, phạm vi phủ định, mức chắc chắn, lời nhờ, bản chép lời, câu vốn tự nhiên không được sửa.

Bốn đề nhóm chat thử việc đổi giọng theo người nhận. `chat-cung-nhom-khac-vai` đưa sẵn mẫu cho bạn thân, trưởng nhóm lớn tuổi và cả nhóm. `chat-nhom-tra-loi-sep` và `chat-nhom-tra-loi-hai-nguoi` dùng một đoạn chat năm người, trong đó phần lớn tin của người dùng là giọng suồng sã với bạn, chỉ vài tin lễ phép với sếp và chị lớn tuổi hơn. Đọc tay ở các đề này là xem tin gửi người trên có lẫn "tui", "ông", ":v" của giọng bạn bè không.

## Lời dặn tiếng Việt hay tiếng Anh

Câu hỏi đặt ra: viết lời dặn của skill bằng tiếng Anh thì mô hình yếu hơn Opus có làm tốt hơn không. Bản thử dịch toàn bộ `SKILL.md` và `references/` sang tiếng Anh, còn ví dụ trước và sau, cụm cần tìm, câu trích thì để nguyên tiếng Việt. Chạy ngày 22/11/2026 trên bản 2.13.0, bằng `--skill-dir`, mỗi đề ba lượt.

| | Sonnet 5.5, lời dặn tiếng Việt | Sonnet 5.5, tiếng Anh | Sonnet 5, tiếng Việt | Sonnet 5, tiếng Anh |
|---|---|---|---|---|
| 63 đề chính | 156/189 | 162/189 | 160/189 | 160/189 |
| 13 đề để riêng | 26/39 | 29/39 | 24/39 | 24/39 |
| Đường đọc đúng, đề chính | 157/189 | 154/189 | 156/189 | 161/189 |
| Điểm `scan.py` trung bình | 3,2 | 2,8 | 3,3 | 2,9 |

Không bật skill, Sonnet 5.5 qua 36/63 đề chính và 2/13 đề để riêng.

Để chấm giọng, Opus đọc mù từng cặp câu trả lời của cùng một đề ở các đề viết, sửa, chat, slide và tóm tắt. Thứ tự hai bản trong cặp đảo theo đề, và Opus không biết bản nào dùng lời dặn tiếng gì. Mỗi cặp, Opus chọn bản đọc như người Việt viết hơn và bản làm đúng lời nhờ hơn, hoặc cho ngang. Trên 402 cặp của hai mô hình, về giọng thì lời dặn tiếng Việt hơn 131 cặp, tiếng Anh hơn 134, ngang 137. Về đúng việc, tiếng Việt hơn 112, tiếng Anh hơn 96, ngang 194.

Không chênh lệch nào vượt sai số (kiểm định dấu, p từ 0,2 trở lên). Bản tiếng Anh có 3 câu trả lời quay sang nói tiếng Anh với người dùng, kiểu "I'll draft the ready-to-use PR description now"; bản tiếng Việt có 1. Cả bốn đều trên Sonnet 5.

Skill vì vậy giữ tiếng Việt. Bản dịch không giúp Sonnet làm tốt hơn, có thêm nó chỉ thêm một bản phải sửa cho khớp. Gemini chưa được thử.

## Kết quả bản 2.17.0

Bản này học thêm từ mattpocock/skills. Ba ý được thử: soi bài theo hai phần tách riêng là đúng lời dặn và giọng văn (`code-review`), email hỏi người khác thì mỗi câu một ý, việc quyết định hỏi trước (`to-questionnaire`), và mô tả PR nói rõ thay đổi không lùi lại được (`pr`). Theo `writing-for-agents`, mỗi ý có đề trước, chạy bản 2.16.0 trước khi viết quy tắc. Opus mức medium, ba lượt mỗi đề.

| | Bản 2.16.0 | Bản 2.17.0 |
|---|---|---|
| `soi-ban-ai-theo-loi-dan` | 3/3 | |
| `viet-email-hoi-nha-cung-cap` | 3/3 | |
| `mo-ta-pr-xoa-cot` | 0/3 | 3/3 |
| `mo-ta-pr` | | 3/3 |

Hai đề đầu bản cũ đã qua cả ba lượt: bản soi tự tách mục "sai hoặc thiếu so với lời dặn" (phòng 302 bị đổi, số 30% tự thêm, mất lời nhờ báo nhóm kế toán) lên trước lỗi giọng, email tự đánh số bốn câu hỏi. Thêm quy tắc cho hai việc này chỉ tốn chữ, nên skill không đổi, hai đề giữ lại làm chốt chặn. Ở `mo-ta-pr-xoa-cot`, bản cũ có đủ số test trước/sau và lỗi API v1 nhưng không lượt nào nói migration xóa cột thì revert không lấy lại được dữ liệu. Bản mới cả ba lượt nói rõ và chỉ cách lùi là khôi phục từ backup. `mo-ta-pr` (thêm retry, lùi lại được) không bị thêm câu cảnh báo nào.

## Kết quả bản 2.14.0

Bản này thêm hai quy tắc cho tin nhắn trên Teams: gõ tắt chừng một nửa số chữ có dạng tắt quen, và đọc lại ba tin gần nhất của người gửi để không chép lại câu nhờ cũ. Ba đề mới dùng đoạn chat Teams bịa. Chạy bằng Opus mức medium, ba lượt mỗi đề, so với bản 2.13.0 bằng `--skill-dir`.

| | Bản 2.13.0 | Bản 2.14.0 |
|---|---|---|
| `chat-teams-khong-lap` | 0/3 | 3/3 |
| `chat-teams-khach` | 3/3 | 3/3 |
| `chat-teams-bao-tien-do` (để riêng) | 0/3 | 3/3 |
| 14 đề chat cũ, một lượt | | 14/14 |

Ở `chat-teams-khong-lap`, ba tin trước của người gửi đều kết bằng "anh duyệt giúp em nha". Bản cũ lượt nào cũng kết đúng câu đó và viết đủ chữ. Bản mới đổi câu nhờ ("a duyệt hộ em với ạ", "anh approve cho e với ạ", "A xem giúp e với ạ") và gõ tắt xen chữ đủ, có một lượt tắt gần hết. `chat-teams-khach` là tin gửi khách hàng ngoài công ty, cả hai bản đều viết đủ chữ. Đề để riêng chạy sau khi chốt bản. Bản cũ trượt chỉ vì không gõ tắt: lời dặn không nhắc tới file tiến độ nên không lượt nào chép câu "em cập nhật file tiến độ rồi". Đọc tay 14 đề chat cũ thì tin gửi sếp, chị PM vẫn viết đủ chữ, có "Dạ", "ạ", phần gửi bạn vẫn giữ chữ tắt theo mẫu. Lỗi chưa sửa: tin gửi khách có lượt tự thêm ngày "28/11" cho "thứ Bảy này".

## Kết quả bản 2.13.0

Chạy thật trên Codex CLI 0.171 (gpt-6.2-sol, mức medium, một lượt mỗi đề chính) và trên Claude (Opus mức medium).

| | Codex, bản 2.12.0 | Codex, bản 2.13.0 | Claude, bản 2.13.0 |
|---|---|---|---|
| 63 đề chính | 55/63 | 59/63 | 60/63, rồi 33/33 lượt ở 11 đề viết mới sau khi sửa |
| 13 đề để riêng | 7/13 | 10/13 | 10/13 |
| Bật đúng, `trigger.json` | 20/20 | 60/60 (3 lượt) | 20/20 |
| Bật nhầm, `trigger.json` | 9/15 | 1/45 (3 lượt) | 0/15 |
| Bật đúng, 32 lời nhờ để riêng | 18/18 (16 lời nhờ mới) | 44/44 | 48/48 |
| Bật nhầm, 32 lời nhờ để riêng | 18/30 (16 lời nhờ mới) | 1/38 | 0/48 |

Lời nhờ để riêng của phần bật skill có 16 câu mới, viết và chạy trên bản 2.12.0 trước khi sửa `description`. Ở bản cũ, Codex đọc skill cho 60% câu hỏi về code, kiến thức hay phép tính (Claude 0%). Lượt thứ ba của 14 lời nhờ mới trên Codex bị mất vì hết credit nên không tính. Bản 2.12.0 trên Codex được chấm lại bằng `check.py` mới (bỏ qua cách xuống dòng, nhận "600 mét"), từ 53 lên 55 đề.

Trước khi sửa, Codex tự nghĩ ra năm bài học cho bài LinkedIn "5 năm làm product manager", viết 1.300 chữ khi được nhờ bài Facebook 1.500 chữ, và sửa tin nhắn viết thường đã tự nhiên thành giọng chỉnh tề. Câu hỏi trước rồi dừng đưa lên `SKILL.md` thì Claude hỏi 6 câu mà không mở `draft.md`, nên thêm "hai đến bốn câu". Codex chưa được chạy lại với chữ này vì hết credit. Các đề hỏi trước giờ qua mà không mở `draft.md`, nên đường đọc của chúng báo thiếu dù câu trả lời đúng.

Còn trượt trên Codex: `slide-chua-co-so-lieu` hỏi bằng câu nhờ không có dấu hỏi, `giong-ten-thang` đưa ngày mới vào chữ thứ 27, `daily-report` đổi "thiếu test" thành "cần bổ sung test", `sua-tieu-de-readme` tự thêm "tháng 10". Trên Claude: `luot-hai-bai-quan` (`scan.py` chấm 11).

## Kết quả bản 2.12.0

Bật skill, Opus mức medium, ba lượt. Mô tả cũ trên `trigger.json`: bật 56/63 lượt nên bật, 0/45 lượt bật nhầm, bỏ lỡ daily report và lời nhờ dịch sang tiếng Việt. Mô tả mới (thêm "dịch sang tiếng Việt", "báo cáo") trên 16 lời nhờ viết sau khi sửa: 30/30 và 0/18, trong khi mô tả cũ chỉ được 24/30 trên cùng các lời nhờ đó. Trên `trigger.json`: 60/60 và 0/45.

Kiểu Codex, một lượt: 58/63 đề chính, 10/13 đề để riêng, đường đọc đúng 72/76 lượt, bật skill 20/20 và 0/15 bật nhầm. Lỗi chỉ thấy ở kiểu này: `sua-co-chi-dan-chen` không mở `edit.md` và không báo dòng chỉ dẫn chèn vào.

## Kết quả bản 2.11.0

Chạy bằng `run.py`, Opus mức medium, mỗi đề ba lượt, hết khoảng 27 USD cho cả bốn đợt.

63 đề chính: 181/189 lượt qua phần tự động (96%, khoảng tin cậy 95%: 92-98%), 56/63 đề qua cả ba lượt. Đường đọc đúng ở 186/189 lượt. Không bật skill thì 32/63 đề qua. Bảy đề trượt một lượt trở lên: ba đề quá giới hạn chữ vài chữ (341/330, 96/90, 383 và 399/380), `tieng-anh-linkedin` một lượt còn emoji, `tra-loi-cau-hoi-thuong` một lượt in đậm bốn chỗ, `soi-bai-ai` một lượt không dẫn số mục, `giong-mau-gach-ngang` một lượt không mở `voice.md` và bỏ mất gạch ngang dài. `sua-tin-gian-giu-nguyen`, đề trượt ở 2.10.0, giờ cả ba lượt đều giữ nguyên tin, lượt trượt chỉ vì ghi chú dài 96 chữ.

13 đề để riêng: lần chấm đầu 23/39 lượt qua (59%, khoảng 43-73%). Đọc từng câu trả lời trượt thì sáu đề trượt vì điều kiện chấm đặt chặt hơn đáp án đúng cần: giới hạn chữ thấp hơn độ dài một bài soát có dẫn chứng, cấm "hai mươi" trong khi ghi chú phải trích câu "hai mươi mốt năm" để giải thích vì sao bỏ, đếm "7" trong "bảy tiêu đề" là số tự thêm. Nới sáu điều kiện đó (đáp án mẫu vẫn qua, skill không đổi) rồi chấm lại đúng các câu trả lời cũ: 34/39 (87%, khoảng 73-94%), 10/13 đề qua cả ba lượt. Không bật skill: 2/13. Lỗi thật còn lại: `slide-ket-qua-quy` cả ba lượt tự tính ngược doanh thu quý 3 từ mức tăng 8% (có ghi là số tính ra, nhưng người dùng không đưa số này), `soi-email-xin-loi` một lượt không dẫn số mục, `sua-thong-bao-cham-cong` một lượt để tên ứng dụng ra ngoài 25 chữ đầu. Theo luật đề để riêng, skill chưa sửa theo các lỗi này.

## Kết quả bản 2.9.0

Lượt chạy đủ đầu tiên trên bản nháp 2.9.0 qua 53/60 đề phần tự động. Đọc tay thấy 2 đề sai: không báo dòng chỉ dẫn chèn vào, và gợi ý gộp cả câu bên cạnh khi chỉ được nhờ soi. Ghi chú hay kể điểm `scan.py`, trích lại cụm đã bỏ, tin nhắn kèm lời giải thích đã bắt chước giọng thế nào. Hai đề trượt vì script chấm: "Mùng 4" viết hoa đầu tin, "ông" khớp nhầm trong "không". Đề email IT trượt vì ngày 8/12 nằm sau hôm chạy thử.

Sau khi sửa skill, sửa `check.py` và đổi ngày trong đề, lượt chạy đủ thứ hai (63 đề, thêm ba đề cho văn thân mật và chữ "phần") qua 62/63 và 2/2 đề giữ riêng. Đề trượt là `bai-nop-cho-truong`, dài 364 chữ so với giới hạn 300. Lượt này chạy làm hai đợt vì hết hạn mức giữa chừng. Đọc tay các đề then chốt thì đúng, trừ `sua-co-chi-dan-chen` vẫn không báo dòng chỉ dẫn chèn vào. Ghi chú giờ bắt buộc có câu báo, đề có thêm phần chấm tự động cho câu này, ba lượt chạy lại đều qua. Lỗi còn lại: ở `qua-may-do`, ghi chú trích lại các cụm đã bỏ trong hai trên ba lượt.

## Kết quả bản 2.7.6

Bản này chưa có lượt nào chạy đủ 45 đề trên cùng một bản `SKILL.md`. Các đề chạy theo từng đợt trong lúc sửa, bằng hai mô hình (Claude và Codex), nên không gộp thành một tỉ lệ qua.

- Tám đề `spoken-*` chạy trên cả ba bản 2.7.1, 2.7.2, 2.7.3 và bản mới. Bản cũ đã giữ đúng ý ở cả tám đề, nên chưa có căn cứ nói bản mới hơn ở nhóm này.
- Đề giới thiệu quán chỉ có tên và địa điểm: cả ba bản cũ dựng bài có nhiều ô trống. Sau khi sửa, bốn đề thiếu dữ kiện (bài PM, chạy bộ, quán, studio) đều hỏi thêm, không dựng bài, mỗi đề một lượt.
- Nhóm chat: năm lượt Opus mức medium trên ba đề (`chat-nhom-tra-loi-sep` hai lượt, `chat-nhom-tra-loi-hai-nguoi` hai lượt, `chat-tra-loi-pm` một lượt) đều qua phần đếm và đúng vai khi đọc tay. Tin gửi sếp và chị lớn tuổi dùng "Dạ", "em", "ạ", phần gửi bạn giữ "ông". Hai lượt Codex về đổi người nhận giữa chừng và chưa rõ gửi cho ai cũng đúng.
- Lỗi còn thấy: mẫu giọng có gạch ngang thì lượt giữ lượt bỏ, tin chat có lúc chuẩn hóa dấu câu hơn mẫu, bài kể dài có lượt tự thêm một câu diễn giải ở đoạn kết dù đủ số liệu. Bài kể trải nghiệm vẫn cần người đứng tên đọc lại từng chi tiết.

## Kết quả bản 2.7.8

Bản này bỏ phần tiếng Anh khỏi `SKILL.md` và thêm ba quy tắc cho ba lỗi ghi ở trên. Mười hai đề chạy lại bằng Opus mức medium, mỗi đề một lượt: `giong-mau-gach-ngang`, ba đề `chat-giong-*` (teencode, miền Tây, văn phòng), `chat-nhom-tra-loi-hai-nguoi`, ba đề `luot-hai-*`, `sua-bai-ai-ke-chuyen`, `sua-nhe-bai-nguoi-viet`, `viet-email-du-du-kien`, `tom-tat-tu-tieng-anh`. Cả mười hai qua phần đếm. Đọc tay thì đoạn theo mẫu có gạch ngang, tin chat giữ kiểu viết hoa và chấm câu của mẫu, ba bài kể đều kết ở sự việc cuối. Mỗi đề mới có một lượt, nên ba lỗi cũ chỉ tính là chưa thấy lại. Đề `tieng-anh-linkedin` vẫn nằm trong bộ đề nhưng không còn là mục tiêu của skill.

`check.py` đổi hai chỗ: `min_questions` nhận cả câu hỏi không đánh số, `min_refs` nhận "Mục" viết hoa và danh sách số sau từ đó. `max_questions` vẫn chỉ đếm mục đánh số, vì dấu hỏi trong email soạn hộ có thể là lời nhờ người nhận.

Câu trả lời thô của các lượt chạy để ở máy người chạy (`evals/results/`, đã nằm trong `.gitignore`) vì log của công cụ có lẫn cấu hình máy.
