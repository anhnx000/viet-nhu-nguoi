#!/usr/bin/env python3
"""Vẽ lại banner, ảnh chia sẻ và ảnh ví dụ trong README từ chính các file trong examples/.

Cần Pillow, font Inter và JetBrains Mono (đều có dấu tiếng Việt). Chạy từ thư mục gốc repo:

    python3 assets/make_images.py
    INTER_DIR=/duong/dan/Inter MONO_DIR=/duong/dan/JetBrainsMono python3 assets/make_images.py

Điểm trên ảnh lấy bằng cách chạy scripts/scan.py trên file ví dụ, nên bộ kiểm tra đổi thì
chạy lại script này là ảnh khớp. Ảnh README vẽ gấp đôi (2400 px ngang) cho nét trên màn hình
retina; social.png 1280x640 là ảnh xem trước khi dán link repo lên Facebook, Zalo, Slack
(GitHub > Settings > Social preview).
"""
import os
import pathlib
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
SCAN = ROOT / "skills/viet-nhu-nguoi/scripts/scan.py"
PATTERNS = ROOT / "skills/viet-nhu-nguoi/references/patterns.md"
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
MONO_DIRS = [os.environ.get("MONO_DIR", ""), "/usr/share/fonts/truetype/jetbrains-mono",
             os.path.expanduser("~/.local/share/fonts/JetBrainsMonoNerdFont")]
REPO = "github.com/anhnx000/viet-nhu-nguoi"
S = 2            # hệ số phóng
W = 1200         # bề ngang logic
PAD = 56         # lề ngoài
GAP = 28         # khoảng giữa hai cột, giữa các thẻ
CARD_PAD = 28

BG_TOP, BG_BOTTOM = (10, 10, 11), (19, 19, 22)
TEXT = "#e4e4e7"
MUTED = "#a1a1aa"
FAINT = "#71717a"
ACCENT = "#4ade80"
CHIP, CHIP_LINE = "#18181b", "#2e2e33"
SCHEMES = {
    "bad": {"fill": "#1a1315", "line": "#7f2d2d", "label": "#f87171", "hl": "#4c1d24", "hl_text": "#fecdd3"},
    "good": {"fill": "#0f1a13", "line": "#1f6b3c", "label": "#4ade80", "hl": "#173d26", "hl_text": "#bbf7d0"},
}

_fonts = {}


def font(weight, size, scale=S):
    key = (weight, size, scale)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONT_DIR}/Inter-{weight}.otf", round(size * scale))
    return _fonts[key]


def mono(weight, size, scale=S):
    key = ("mono", weight, size, scale)
    if key not in _fonts:
        for d in MONO_DIRS:
            for name in (f"JetBrainsMono-{weight}.ttf", f"JetBrainsMonoNerdFontMono-{weight}.ttf"):
                if d and os.path.exists(os.path.join(d, name)):
                    _fonts[key] = ImageFont.truetype(os.path.join(d, name), round(size * scale))
                    return _fonts[key]
        _fonts[key] = ImageFont.truetype("DejaVuSansMono.ttf", round(size * scale))
    return _fonts[key]


def tw(text, f, scale=S):
    return f.getlength(text) / scale


def scan(rel):
    """Chạy bộ kiểm tra thật trên file ví dụ, trả về (điểm, số dấu hiệu)."""
    out = subprocess.run([sys.executable, "-I", str(SCAN), str(ROOT / rel)], capture_output=True,
                         text=True, encoding="utf-8", check=True).stdout
    m = re.search(r"Điểm (\d+)/100", out)
    n = re.search(r"(\d+) dấu hiệu", out)
    return int(m.group(1)), int(n.group(1)) if n else 0


def pattern_count():
    return len(re.findall(r"^### \d+\.", PATTERNS.read_text(encoding="utf-8"), re.M))


def background(w, h):
    img = Image.new("RGB", (w, h), BG_TOP)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))
    return img, d


def mark(text, phrases):
    """Trả về danh sách (từ, có tô không); cụm cần tô tìm không phân biệt hoa thường."""
    flags = [False] * len(text)
    low = text.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p.lower()), low):
            for i in range(m.start(), m.end()):
                flags[i] = True
    words = []
    for m in re.finditer(r"\S+", text):
        inside = [flags[i] for i in range(m.start(), m.end())]
        words.append((m.group(0), sum(inside) * 2 >= len(inside)))
    return words


def wrap(words, f, maxw):
    lines, cur, width = [], [], 0.0
    space = tw(" ", f)
    for word, hl in words:
        w = tw(word, f)
        if cur and width + space + w > maxw:
            lines.append(cur)
            cur, width = [], 0.0
        width += (space if cur else 0) + w
        cur.append((word, hl))
    if cur:
        lines.append(cur)
    return lines


class Block:
    """Một khối trong thẻ: đo chiều cao trước, vẽ sau."""

    def height(self, width):
        raise NotImplementedError

    def draw(self, d, x, y, width, scheme):
        raise NotImplementedError


class Para(Block):
    def __init__(self, text, phrases=(), size=19, color=TEXT, weight="Regular", leading=1.55, after=14):
        self.words, self.size, self.color = mark(text, phrases), size, color
        self.weight, self.leading, self.after = weight, leading, after

    def _lines(self, width):
        return wrap(self.words, font(self.weight, self.size), width)

    def height(self, width):
        return len(self._lines(width)) * self.size * self.leading + self.after

    def draw(self, d, x, y, width, scheme):
        f = font(self.weight, self.size)
        space = tw(" ", f)
        lh = self.size * self.leading
        for line in self._lines(width):
            cx = x
            run_start = None
            spans = []
            for i, (word, hl) in enumerate(line):
                w = tw(word, f)
                if hl and run_start is None:
                    run_start = cx
                if hl and (i + 1 == len(line) or not line[i + 1][1]):
                    spans.append((run_start, cx + w))
                    run_start = None
                cx += w + space
            for a, b in spans:
                d.rounded_rectangle([(a - 4) * S, (y + 1) * S, (b + 4) * S, (y + self.size * 1.42) * S],
                                    radius=5 * S, fill=scheme["hl"])
                d.line([(a - 2) * S, (y + self.size * 1.42) * S, (b + 2) * S, (y + self.size * 1.42) * S],
                       fill=scheme["line"], width=S)
            cx = x
            for word, hl in line:
                d.text((cx * S, (y + self.size * 0.12) * S), word, font=f,
                       fill=scheme["hl_text"] if hl else self.color)
                cx += tw(word, f) + space
            y += lh
        return y + self.after


class Numbered(Block):
    """Danh sách tiêu đề slide: ô số bên trái, chữ bên phải."""

    def __init__(self, items, phrases=(), size=19):
        self.items = [Para(t, phrases, size=size, after=0) for t in items]

    def height(self, width):
        return sum(p.height(width - 44) + 12 for p in self.items) + 2

    def draw(self, d, x, y, width, scheme):
        f = font("SemiBold", 14)
        for i, p in enumerate(self.items, 1):
            d.rounded_rectangle([x * S, (y + 1) * S, (x + 28) * S, (y + 27) * S], radius=7 * S, fill=scheme["hl"])
            n = str(i)
            d.text(((x + 14 - tw(n, f) / 2) * S, (y + 5) * S), n, font=f, fill=scheme["hl_text"])
            y = p.draw(d, x + 44, y, width - 44, scheme) + 12
        return y + 2


class Stats(Block):
    """Lưới con số lớn kèm chú thích, hai cột."""

    ROW = 98

    def __init__(self, pairs):
        self.pairs = pairs

    def height(self, width):
        return (len(self.pairs) + 1) // 2 * self.ROW + 14

    def draw(self, d, x, y, width, scheme):
        col = width / 2
        for i, (num, label) in enumerate(self.pairs):
            cx = x + (i % 2) * col
            cy = y + (i // 2) * self.ROW
            d.text((cx * S, cy * S), num, font=font("Bold", 30), fill=scheme["label"])
            lines = wrap([(w.replace("\u00a0", " "), False) for w in label.split(" ")], font("Regular", 15), col - 16)
            for j, line in enumerate(lines[:2]):
                d.text((cx * S, (cy + 38 + j * 19) * S), " ".join(w for w, _ in line),
                       font=font("Regular", 15), fill=MUTED)
        return y + self.height(width)


class Spacer(Block):
    def __init__(self, h):
        self.h = h

    def height(self, width):
        return self.h

    def draw(self, d, x, y, width, scheme):
        return y + self.h


def score_badge(d, right, top, score, sc, big=34):
    """Điểm to kiểu '84/100' canh phải, trả về bề ngang đã vẽ."""
    fn, fs = font("Bold", big), mono("Medium", big * 0.42)
    num, rest = str(score), "/100"
    w = tw(num, fn) + 4 + tw(rest, fs)
    x = right - w
    d.text((x * S, top * S), num, font=fn, fill=sc["label"])
    d.text(((x + tw(num, fn) + 4) * S, (top + big * 0.62) * S), rest, font=fs, fill=sc["label"])
    return w


class Card:
    HEAD = 52

    def __init__(self, label, kind, blocks, score=None, note=None):
        self.label, self.kind, self.blocks, self.score, self.note = label, kind, blocks, score, note

    def height(self, width):
        inner = width - 2 * CARD_PAD
        return CARD_PAD + self.HEAD + sum(b.height(inner) for b in self.blocks) + CARD_PAD - 10

    def draw(self, d, x, y, width):
        sc = SCHEMES[self.kind]
        h = self.height(width)
        d.rounded_rectangle([x * S, y * S, (x + width) * S, (y + h) * S], radius=18 * S,
                            fill=sc["fill"], outline=sc["line"], width=2 * S)
        d.text(((x + CARD_PAD) * S, (y + CARD_PAD) * S), self.label, font=font("Bold", 21), fill=sc["label"])
        if self.note:
            d.text(((x + CARD_PAD) * S, (y + CARD_PAD + 28) * S), self.note, font=mono("Regular", 13), fill=MUTED)
        if self.score is not None:
            score_badge(d, x + width - CARD_PAD, y + CARD_PAD - 10, self.score, sc)
        cy = y + CARD_PAD + self.HEAD
        for b in self.blocks:
            cy = b.draw(d, x + CARD_PAD, cy, width - 2 * CARD_PAD, sc)
        return y + h


def chips(d, x, y, items, size=16, scale=S):
    """Hàng nhãn bo tròn, mỗi nhãn một chấm xanh."""
    f = mono("Medium", size * 0.92, scale)
    for text in items:
        w = tw(text, f, scale) + 2 * size + 10
        d.rounded_rectangle([x * scale, y * scale, (x + w) * scale, (y + size * 2.1) * scale],
                            radius=size * 1.05 * scale, fill=CHIP, outline=CHIP_LINE, width=scale)
        r = size * 0.22
        cy = y + size * 1.05
        d.ellipse([(x + size * 0.9 - r) * scale, (cy - r) * scale, (x + size * 0.9 + r) * scale, (cy + r) * scale],
                  fill=ACCENT)
        d.text(((x + size * 1.55) * scale, (y + size * 0.52) * scale), text, font=f, fill="#d4d4d8")
        x += w + 10
    return x


def brand(d, y, title_size):
    """Tên repo ở góc phải hàng tiêu đề, để ảnh bị cắt ra đăng lại vẫn còn nguồn."""
    f = mono("Regular", 14)
    d.text(((W - PAD - tw(REPO, f)) * S, (y + title_size * 0.42) * S), REPO, font=f, fill=FAINT)


def compose(name, title, subtitle, left, right, footer=None, title_size=40, gap=GAP, arrow=False, after=None):
    col = (W - 2 * PAD - gap) / 2
    head = PAD + title_size * 1.25 + (30 if subtitle else 0) + 26

    def col_height(cards):
        return sum(c.height(col) for c in cards) + GAP * (len(cards) - 1)

    body = max(col_height(left), col_height(right))
    for cards in (left, right):  # kéo thẻ cuối mỗi cột cho hai cột bằng đáy
        extra = body - col_height(cards)
        if extra > 0:
            cards[-1].blocks.append(Spacer(extra))
    foot = (26 + 28 * len(footer)) if footer else 0
    extra_h = after[0] if after else 0
    H = int(head + body + extra_h + foot + PAD)
    img, d = background(W * S, H * S)
    d.text((PAD * S, (PAD - 6) * S), title, font=font("Bold", title_size), fill="#f8fafc")
    if not arrow:
        brand(d, PAD - 6, title_size)
    if subtitle:
        d.text((PAD * S, (PAD + title_size * 1.25 + 2) * S), subtitle, font=font("Regular", 20), fill=MUTED)
    for cards, x in ((left, PAD), (right, PAD + col + gap)):
        y = head
        for c in cards:
            y = c.draw(d, x, y, col) + GAP
    if arrow:
        cx, cy, r = W / 2, head + body / 2, 26
        d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=CHIP, outline=ACCENT, width=2 * S)
        f = font("Bold", 26)
        d.text(((cx - tw("→", f) / 2) * S, (cy - 17) * S), "→", font=f, fill=ACCENT)
    y = head + body
    if after:
        after[1](d, y + 26)
        y += extra_h
    if footer:
        y += 26
        for i, line in enumerate(footer):
            d.text((PAD * S, y * S), line, font=font("Regular", 17) if i == 0 else mono("Regular", 14),
                   fill="#cbd5e1" if i == 0 else FAINT)
            y += 28
    save(img, name)


def save(img, name):
    path = OUT / name
    img.save(path, optimize=True)
    print(f"{path.relative_to(ROOT)}  {img.size[0]}x{img.size[1]}  {path.stat().st_size // 1024} KB")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").strip()


# Cụm bộ kiểm tra bắt trong examples/truoc.md (xem kết quả scan.py trong README)
EMAIL_TELLS = [
    "Trong bối cảnh hiện nay", "không chỉ là xu hướng mà còn", "yếu tố then chốt", "nâng tầm",
    "Điều này", "được chứng minh bởi", "nhiều nghiên cứu chỉ ra", "một cách đáng kể", "Bên cạnh đó",
    "tiến hành thực hiện việc", "nhằm mục đích", "trải nghiệm liền mạch", "Nó giúp", "trở nên dễ dàng",
    "Hy vọng những thông tin trên",
]
SLIDES_AI = ["Chuyển đổi số: Hành trình kiến tạo giá trị", "Tổng quan", "Thách thức", "3 trụ cột giải pháp",
             "Lợi ích", "Kết luận", "Cảm ơn"]
SLIDES_HUMAN = ["Đề xuất thuê thêm 1 QA cho quý 1/2027", "Hai bản phát hành quý 3 đều trễ vì thiếu người test",
                "Thuê 1 QA tốn ít hơn tiền phạt mỗi lần trễ hạn", "Cần anh duyệt trước 30/11 để kịp tuyển người"]
SLIDE_TELLS = ["Hành trình kiến tạo giá trị", "Tổng quan", "Thách thức", "3 trụ cột", "Lợi ích", "Kết luận",
               "Cảm ơn"]
POST_QUOTES = [
    "Nói cho thật: tiến độ không dễ.",
    "Khó nhất không phải là code, mà là chọn việc gì để làm.",
    "Mình không cần bạn giỏi kernel. Mình cần bạn kiên nhẫn đọc log.",
]
POST_TELLS = ["Nói cho thật:", "không phải là code, mà là", "Mình không cần", "Mình cần"]

T = {
    "vi": {
        "sfx": "", "ai": "AI viết", "skill": "Qua skill", "detail": "Có thêm chi tiết bạn đưa",
        "email_title": "Email, báo cáo",
        "email_sub": "Cùng một nội dung. Tô đỏ là {n} chỗ bộ kiểm tra bắt được trong {w} chữ.",
        "email_note": "Bài gốc không có số liệu nào, skill không tự thêm.",
        "slide_title": "Tiêu đề slide", "slide_sub": "Sếp thường chỉ lướt tiêu đề. Lướt bên trái xong vẫn chưa biết phải duyệt gì.",
        "slide_ai": "AI làm", "slide_skill": "Làm theo skill",
        "slide_note_ai": "Cả bảy tiêu đề đều chỉ là nhãn, không cái nào nói ra kết luận.",
        "slide_note": "Chỉ cần đọc liền bốn tiêu đề là hiểu cả đề xuất. Hai file .pptx nằm trong examples/, bộ kiểm tra đọc thẳng file slide.",
        "post_title": "Bài đăng dài", "post_sub": "Câu nào cũng sạch, nhưng cả bài cứ lặp đi lặp lại vài kiểu câu.",
        "post_before": "Bài gốc", "post_after": "Bản viết lại",
        "stats_before": [("1.740", "chữ, chia thành chín mục có tiêu đề viết hoa"), ("10", 'câu kiểu "không phải X\u00a0mà\u00a0là\u00a0Y"'),
                         ("6", 'câu mở bằng nhãn "nói gọn", "nói cho thật"'), ("19/88", "câu có dấu hai chấm")],
        "stats_after": [("373", "chữ, viết liền, không chia mục"), ("1", "việc duy nhất là rủ người vào làm cùng")],
        "post_old": "Từ AI quen mặt gần như không còn, cái lộ ra là vài kiểu câu lặp lại.",
        "post_new": "Bản viết lại không thêm dữ kiện nào ngoài bài gốc.",
    },
    "en": {
        "sfx": ".en", "ai": "AI draft", "skill": "After the skill", "detail": "With details you supplied",
        "email_title": "Emails and reports",
        "email_sub": "Same content. The red marks are the {n} spots the scanner flags in {w} words.",
        "email_note": "The original has no numbers, and the skill adds none.",
        "slide_title": "Slide titles", "slide_sub": "Managers skim the titles. The left deck never says what to approve.",
        "slide_ai": "Made by AI", "slide_skill": "Made with the skill",
        "slide_note_ai": "All seven titles are topic labels; none states a conclusion.",
        "slide_note": "Reading the four titles in order is enough to follow the whole proposal. Both .pptx files are in examples/, and the scanner reads slide files directly.",
        "post_title": "A long post", "post_sub": "Each sentence is clean, but the post repeats a few shapes.",
        "post_before": "Original", "post_after": "Rewrite",
        "stats_before": [("1,740", "words split into nine sections with all-caps headings"), ("10", '"not X but\u00a0Y" sentences'),
                         ("6", 'sentences opening with a label ("nói gọn")'), ("19/88", "sentences with a colon")],
        "stats_after": [("373", "words in plain paragraphs, no headings"), ("1", "thing it does: invite people to join")],
        "post_old": "The familiar AI words are gone. What shows is the repeated sentence shapes.",
        "post_new": "The rewrite adds no fact that the original lacks.",
    },
}


EXCERPT = ("Trong bối cảnh hiện nay, việc ứng dụng AI không chỉ là xu hướng mà còn là yếu tố then chốt. "
           "Bên cạnh đó, đội ngũ của chúng tôi đã tiến hành thực hiện việc triển khai hệ thống mới nhằm mục đích "
           "mang lại trải nghiệm liền mạch cho khách hàng. Nó giúp việc quản lý dự án trở nên dễ dàng hơn... "
           "Hy vọng những thông tin trên sẽ hữu ích cho bạn!")


def selling_points():
    return [f"{pattern_count()} dấu hiệu văn AI", "Bộ kiểm tra chấm 0-100", "Không bịa số liệu",
            "Slide, email, bài đăng, tin nhắn", "Miễn phí, MIT"]


def banner():
    bad, n = scan("examples/truoc.md")
    good, _ = scan("examples/sau.md")
    compose(
        "banner.png", "Viết như người", "Nhờ AI viết tiếng Việt mà đọc lên vẫn ra giọng mình",
        [Card("Trước", "bad", [Para(EXCERPT, EMAIL_TELLS, size=20, after=22),
                               Para(f"Cả email {len(read('examples/truoc.md').split())} chữ, bộ kiểm tra bắt {n} chỗ.",
                                    size=16, color=MUTED, after=4)],
              bad, "email AI viết, trích")],
        [Card("Sau", "good",
              [Para(read("examples/sau.md"), size=20, after=10),
               Para("Bỏ câu sáo, giữ đúng ý, không thêm số liệu nào.", size=16, color=MUTED, after=22),
               Para("Bạn đưa thêm chi tiết thì skill viết cụ thể hơn", size=16, color=ACCENT, weight="SemiBold", after=6),
               Para(read("examples/sau-co-chi-tiet.md"), size=18, after=4)],
              good, "cùng nội dung, giọng người")],
        footer=["Skill cho Claude Code, Codex, Cursor. Cài bằng cách dán link repo vào ô chat.", REPO],
        title_size=56, gap=72, arrow=True,
        after=(40, lambda d, y: chips(d, PAD, y, selling_points(), size=15)))


def social():
    """Ảnh 1280x640 hiện ra khi dán link repo lên mạng xã hội."""
    sw, sh, sc = 1280, 640, 2
    img, d = background(sw * sc, sh * sc)
    x = 72
    d.text((x * sc, 64 * sc), "Viết như người", font=font("Bold", 76, sc), fill="#f8fafc")
    for i, line in enumerate(["Nhờ AI viết tiếng Việt", "mà đọc lên vẫn ra giọng mình."]):
        d.text((x * sc, (176 + i * 46) * sc), line, font=font("Regular", 34, sc), fill="#cbd5e1")
    for i, item in enumerate(selling_points()[:4]):
        cy = 312 + i * 42
        d.ellipse([(x + 2) * sc, (cy + 10) * sc, (x + 13) * sc, (cy + 21) * sc], fill=ACCENT)
        d.text(((x + 28) * sc, cy * sc), item, font=font("Regular", 23, sc), fill="#dbe4f0")
    d.text((x * sc, 540 * sc), "Skill cho Claude Code, Codex, Cursor", font=font("SemiBold", 22, sc), fill="#e2e8f0")
    d.text((x * sc, 574 * sc), REPO, font=mono("Regular", 19, sc), fill=FAINT)
    # bên phải: cùng một email, điểm trước và sau
    rx, cw, ch = 820, 360, 150
    rows = ((scan("examples/truoc.md")[0], "email AI viết", "bad", 96),
            (scan("examples/sau.md")[0], "sau khi qua skill", "good", 330))
    for score, label, kind, by in rows:
        s = SCHEMES[kind]
        d.rounded_rectangle([rx * sc, by * sc, (rx + cw) * sc, (by + ch) * sc], radius=22 * sc,
                            fill=s["fill"], outline=s["line"], width=3 * sc)
        fn = font("Bold", 84, sc)
        d.text(((rx + 30) * sc, (by + 12) * sc), str(score), font=fn, fill=s["label"])
        d.text(((rx + 30 + tw(str(score), fn, sc) + 8) * sc, (by + 62) * sc), "/100",
               font=mono("Medium", 24, sc), fill=s["label"])
        d.text(((rx + 32) * sc, (by + 110) * sc), label, font=mono("Regular", 18, sc), fill=MUTED)
    cx, cy, r = rx + cw / 2, (96 + ch + 330) / 2, 28
    d.ellipse([(cx - r) * sc, (cy - r) * sc, (cx + r) * sc, (cy + r) * sc], fill=CHIP, outline=ACCENT, width=2 * sc)
    f = font("Bold", 30, sc)
    d.text(((cx - tw("↓", f, sc) / 2) * sc, (cy - 19) * sc), "↓", font=f, fill=ACCENT)
    d.text((rx * sc, 500 * sc), "Điểm do bộ kiểm tra đi kèm skill chấm,", font=font("Regular", 17, sc), fill=FAINT)
    d.text((rx * sc, 524 * sc), "càng viết theo khuôn càng cao.", font=font("Regular", 17, sc), fill=FAINT)
    save(img.resize((sw, sh), Image.LANCZOS), "social.png")


def terminal():
    """Ảnh cửa sổ terminal in nguyên văn kết quả scan.py trên examples/truoc.md."""
    rel = "examples/truoc.md"
    out = subprocess.run([sys.executable, "-I", str(SCAN), str(ROOT / rel)], capture_output=True,
                         text=True, encoding="utf-8", check=True).stdout.rstrip().split("\n")
    size, lh, wpad, bar = 15, 23, 28, 44
    lines = ["$ python3 scan.py " + rel] + [""] + out
    win_w = W - 2 * PAD
    win_h = bar + wpad * 2 + lh * len(lines)
    H = int(PAD + 40 * 1.25 + 30 + 26 + win_h + PAD)
    img, d = background(W * S, H * S)
    d.text((PAD * S, (PAD - 6) * S), "Bộ kiểm tra chạy thật", font=font("Bold", 40), fill="#f8fafc")
    brand(d, PAD - 6, 40)
    d.text((PAD * S, (PAD + 52) * S), "Chấm email AI viết ở examples/truoc.md, kết quả in nguyên văn.",
           font=font("Regular", 20), fill=MUTED)
    x, y = PAD, PAD + 40 * 1.25 + 30 + 26
    d.rounded_rectangle([x * S, y * S, (x + win_w) * S, (y + win_h) * S], radius=14 * S,
                        fill="#0c0c0e", outline="#2e2e33", width=S)
    d.rounded_rectangle([x * S, y * S, (x + win_w) * S, (y + bar) * S], radius=14 * S, fill="#18181b")
    d.rectangle([x * S, (y + bar - 14) * S, (x + win_w) * S, (y + bar) * S], fill="#18181b")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        cx = x + 22 + i * 20
        d.ellipse([(cx - 6) * S, (y + bar / 2 - 6) * S, (cx + 6) * S, (y + bar / 2 + 6) * S], fill=c)
    t = "viet-nhu-nguoi"
    d.text(((x + win_w / 2 - tw(t, mono("Regular", 13)) / 2) * S, (y + 14) * S), t, font=mono("Regular", 13), fill=FAINT)
    ty = y + bar + wpad
    for line in lines:
        f, color = mono("Regular", size), TEXT
        if line.startswith("$"):
            f, color = mono("Medium", size), ACCENT
        elif re.match(r"Điểm \d", line):
            f, color = mono("Bold", size), "#f87171"
        elif line.startswith("["):
            f, color = mono("SemiBold", size), "#fbbf24"
        elif line.startswith("  dòng"):
            head, _, rest = line.partition(": ")
            d.text(((x + wpad) * S, ty * S), head + ": ", font=mono("Regular", size), fill=FAINT)
            d.text(((x + wpad + tw(head + ": ", mono("Regular", size))) * S, ty * S), rest,
                   font=mono("Regular", size), fill="#fecdd3")
            ty += lh
            continue
        elif line and not line.startswith(" "):
            color = MUTED
        d.text(((x + wpad) * S, ty * S), line, font=f, fill=color)
        ty += lh
    save(img, "vi-du-bo-kiem-tra.png")


def email(t):
    bad, n = scan("examples/truoc.md")
    words = len(read("examples/truoc.md").split())
    compose(
        f"vi-du-email{t['sfx']}.png", t["email_title"], t["email_sub"].format(n=n, w=words),
        [Card(t["ai"], "bad", [Para(p, EMAIL_TELLS) for p in read("examples/truoc.md").split("\n\n")], bad)],
        [Card(t["skill"], "good", [Para(read("examples/sau.md")),
                                   Para(t["email_note"], size=15, color=MUTED, after=4)], scan("examples/sau.md")[0]),
         Card(t["detail"], "good", [Para(read("examples/sau-co-chi-tiet.md"))], scan("examples/sau-co-chi-tiet.md")[0])])


def slides(t):
    compose(
        f"vi-du-slide{t['sfx']}.png", t["slide_title"], t["slide_sub"],
        [Card(t["slide_ai"], "bad", [Numbered(SLIDES_AI, SLIDE_TELLS),
                                     Para(t["slide_note_ai"], size=15, color=MUTED, after=4)],
              scan("examples/slide-truoc.pptx")[0])],
        [Card(t["slide_skill"], "good", [Numbered(SLIDES_HUMAN),
                                         Para(t["slide_note"], size=15, color=MUTED, after=4)],
              scan("examples/slide-sau.pptx")[0])])


def post(t):
    paras = [p for p in read("examples/bai-dang-sau.md").split("\n\n") if not p.startswith("#")]
    compose(
        f"vi-du-bai-dang{t['sfx']}.png", t["post_title"], t["post_sub"],
        [Card(t["post_before"], "bad",
              [Stats(t["stats_before"])] + [Para(q, POST_TELLS, size=17, after=8) for q in POST_QUOTES]
              + [Para(t["post_old"], size=15, color=MUTED, after=4)], scan("examples/bai-dang-truoc.md")[0])],
        [Card(t["post_after"], "good",
              [Stats(t["stats_after"]), Para(paras[0], size=17, after=10),
               Para("[...]", size=17, color=FAINT, after=10), Para(paras[-1], size=17, after=12),
               Para(t["post_new"], size=15, color=MUTED, after=4)], scan("examples/bai-dang-sau.md")[0])])


if __name__ == "__main__":
    banner()
    social()
    terminal()
    for lang in ("vi", "en"):
        email(T[lang])
        slides(T[lang])
        post(T[lang])
