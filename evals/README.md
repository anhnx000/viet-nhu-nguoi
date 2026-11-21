# Bộ đề thử skill

`scenarios.json` có 63 tình huống thường gặp, dùng khi chỉnh skill. `held-out.json` có 13 đề để riêng, chỉ chạy trên bản đã chốt. Mỗi đề có `tin_nhan` là lời người dùng, `tep` (nếu có) là file đầu vào, `mong_doi` là điều người đọc cần thấy trong câu trả lời, `kiem` là phần script đếm được. `trigger.json` có 41 lời nhờ để thử skill có tự bật đúng lúc không. File trong `inputs/` là văn viết ra để thử, tên người và số liệu đều bịa.

## Chạy

```bash
python3 -I evals/run.py evals/results/<bản> --runs 3            # 63 đề, mỗi đề 3 lượt
python3 -I evals/run.py evals/results/<bản>-held-out --held-out --runs 3
python3 -I evals/run.py evals/results/<bản>-khong-skill --khong-skill   # cùng đề, không bật skill
python3 -I evals/run.py evals/results/trigger-<bản> --trigger --runs 3   # skill có tự bật đúng lúc không
python3 -I evals/run.py evals/results/<bản>-codex --kieu-codex           # nạp skill theo cách của Codex
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

Thêm một mục vào `scenarios.json` và một đáp án mẫu. Điều kiện trong `kiem` nên lỏng vừa đủ: câu trả lời đúng mà viết khác đi một chút thì vẫn phải qua. Đừng đặt `must_not` cho cụm mà trợ lý có thể trích lại trong ghi chú ("mình đã bỏ câu ..."), khi đó dùng `max_overlap`. `lead_keep` dùng cho tin có việc nhờ: dữ kiện phải nằm trong 25 chữ đầu. `max_added_numbers` không dùng cho đề có nguồn tiếng Anh, vì "March 1, 2027" và "1/3/2027" bị tính là hai số khác nhau.

## Skill có tự bật đúng lúc không

Người dùng thường không gõ `/viet-nhu-nguoi`, nên skill chỉ có ích khi trợ lý tự nhận ra lời nhờ cần đến nó. `trigger.json` chia lời nhờ làm ba loại:

- 21 lời nhờ nên bật: soạn email, tin nhắn, mô tả PR, slide, lời phát biểu, dịch sang tiếng Việt, soi hay sửa văn có giọng máy, cả lời nhờ tiếng Anh sửa bài cho bớt giọng AI.
- 15 lời nhờ gần giống mà không nên bật: dịch sang tiếng Anh, hỏi kiến thức bằng tiếng Việt, code có chữ Việt, đếm chữ trong file văn bản, tóm tắt tiếng Anh.
- 5 lời nhờ để tùy (`"bat": null`), như soát chính tả, commit message, tóm tắt cho chính người hỏi.

`run.py --trigger` gửi lời nhờ như người dùng gõ thường và dừng sau 4 bước, `check.py --trigger` đếm số lượt trợ lý gọi skill hoặc mở `SKILL.md`. Thư mục chạy thử có sẵn khoảng 20 skill dựng sẵn của Claude Code bên cạnh skill này, nhưng máy người dùng thường có nhiều skill hơn, nên tỉ lệ bật thật có thể thấp hơn. Sửa `description` theo kết quả thì viết lời nhờ mới để báo kết quả, đừng dùng lại lời nhờ đã dùng để sửa.

## Kiểu Codex

`--kieu-codex` để skill ở `.agents/skills/`, bỏ công cụ Skill và thêm vào lời nhắc hệ thống phần hướng dẫn skill chép từ Codex CLI 0.171 (danh sách skill kèm đường dẫn, luật "tên skill được nhắc hoặc việc khớp mô tả thì phải dùng, đọc trọn `SKILL.md`, đường dẫn tương đối tính từ thư mục skill"). Lời nhờ mở bằng `$viet-nhu-nguoi` như cách gọi trong Codex. Mô hình vẫn là Claude, nên chế độ này chỉ thử phần skill mang sang được: đường dẫn, cách tìm file trong `references/`, script, khi không có công cụ Skill. Muốn thử mô hình GPT thì chạy thẳng `codex exec`.

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
