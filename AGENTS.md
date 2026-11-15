# Hướng dẫn cho trợ lý AI sửa repo này

Repo này là một skill viết bằng Markdown, kèm hai script Python chỉ dùng thư viện chuẩn. `skills/viet-nhu-nguoi/SKILL.md` là phần trợ lý đọc mỗi lần dùng skill, nên đó là sản phẩm chính.

## File chính

- `skills/viet-nhu-nguoi/SKILL.md`: quy tắc. Mỗi lần dùng skill, trợ lý đọc hết file này, nên thêm chữ nào cũng phải đáng. Test chặn file dài quá 6.000 chữ.
- `skills/viet-nhu-nguoi/references/patterns.md`: danh mục dấu hiệu, đánh số liền từ 1, mỗi mục có ví dụ trước và sau.
- `skills/viet-nhu-nguoi/scripts/scan.py`, `check_facts.py`: bộ kiểm tra và công cụ so dữ kiện.
- `tests/`: `test_scan.py` cho bộ kiểm tra, `test_package.py` cho phiên bản, cách đánh số danh mục, độ dài `SKILL.md`.
- `evals/`: 46 đề thử hành vi của skill (`scenarios.json`), file đầu vào và `check.py` chấm phần đếm được. Sửa `SKILL.md` hay file trong `references/` thì chạy lại các đề liên quan theo `evals/README.md`.
- `README.md` (tiếng Việt, bản chính), `README.en.md`, `CHANGELOG.md`, `RELEASE_NOTES.md` (tiếng Anh).

## Khi sửa

- Dấu hiệu mới: trước hết xem có gộp được vào mục đã có không. README và ảnh không ghi tổng số dấu hiệu, vì danh mục còn thêm dần.
- Kiểm tra mới trong `scan.py` phải có test cả hai chiều: bắt được văn có dấu hiệu, không báo nhầm văn người viết.
- Thêm hay chỉnh ngưỡng trong `scan.py` thì đo trên hai phía rồi ghi số vào `CHANGELOG.md`: bài mô hình viết theo đề bài thường gặp mà không bật skill, và bài người viết đăng trước 11/2022. Đề bài dùng để chỉnh thì không dùng lại để báo kết quả, viết đề mới.
- Điểm của các file trong `examples/` mà đổi thì sửa mọi chỗ dẫn lại: README hai thứ tiếng, ảnh trong `assets/` (vẽ lại bằng `python3 assets/make_images.py`), test.
- Phiên bản phải giống nhau ở `SKILL.md` (`metadata.version`), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` và mục đầu `CHANGELOG.md`. Mỗi phiên bản có thêm một mục tiếng Anh, ngắn, trong `RELEASE_NOTES.md`: trang release trên GitHub lấy ghi chú từ đó, còn `CHANGELOG.md` vẫn viết tiếng Việt.
- Không thêm mẹo lừa phần mềm kiểm tra AI, không hứa qua được các phần mềm đó, không bịa số liệu, tên, nguồn.
- Trước khi đẩy code: `python3 -m unittest discover -s tests` và `bash -n install.sh`.

## Viết

Văn trong repo cũng theo đúng skill: chạy `python3 -I skills/viet-nhu-nguoi/scripts/scan.py --meta <file>` cho tài liệu có trích ví dụ, và đọc lại xem có câu nào nghe như dịch từ tiếng Anh.
