# Hướng dẫn cho trợ lý AI sửa repo này

Repo này là một skill viết bằng Markdown, kèm hai script Python chỉ dùng thư viện chuẩn. `skills/viet-nhu-nguoi/SKILL.md` là phần trợ lý đọc mỗi lần dùng skill, nên đó là sản phẩm chính.

## File chính

- `skills/viet-nhu-nguoi/SKILL.md`: quy tắc. Mỗi lần dùng skill, trợ lý đọc hết file này, nên thêm chữ nào cũng phải đáng. Test chặn file dài quá 6.000 chữ.
- `skills/viet-nhu-nguoi/references/patterns.md`: danh mục dấu hiệu, đánh số liền từ 1, mỗi mục có ví dụ trước và sau.
- `skills/viet-nhu-nguoi/scripts/scan.py`, `check_facts.py`: máy quét và công cụ so dữ kiện.
- `tests/`: `test_scan.py` cho máy quét, `test_package.py` cho phiên bản, số dấu hiệu, độ dài `SKILL.md`.
- `README.md` (tiếng Việt, bản chính), `README.en.md`, `CHANGELOG.md`.

## Khi sửa

- Dấu hiệu mới: trước hết xem có gộp được vào mục đã có không. Thêm, bớt hay đánh số lại mục nào thì sửa con số tổng trong hai README.
- Kiểm tra mới trong `scan.py` phải có test cả hai chiều: bắt được văn có dấu hiệu, không báo nhầm văn người viết.
- Điểm của các file trong `examples/` mà đổi thì sửa mọi chỗ dẫn lại: README hai thứ tiếng, ảnh trong `assets/` (vẽ lại bằng `python3 assets/make_images.py`), test.
- Phiên bản phải giống nhau ở `SKILL.md` (`metadata.version`), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` và mục đầu `CHANGELOG.md`.
- Không thêm mẹo lừa máy dò AI, không hứa qua được máy dò, không bịa số liệu, tên, nguồn.
- Trước khi đẩy code: `python3 -m unittest discover -s tests` và `bash -n install.sh`.

## Viết

Văn trong repo cũng theo đúng skill: chạy `python3 -I skills/viet-nhu-nguoi/scripts/scan.py --meta <file>` cho tài liệu có trích ví dụ, và đọc lại xem có câu nào nghe như dịch từ tiếng Anh.
