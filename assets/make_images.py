#!/usr/bin/env python3
"""Vẽ lại banner và ảnh ví dụ trong README từ chính các file trong examples/.

Cần Pillow và font Inter (có dấu tiếng Việt). Chạy từ thư mục gốc repo:

    python3 assets/make_images.py            # font ở /usr/share/fonts/opentype/inter
    INTER_DIR=/duong/dan/Inter python3 assets/make_images.py

Ảnh xuất ra assets/ ở độ phân giải gấp đôi (2400 px ngang) để hiện nét trên màn hình retina.
Chữ trong ảnh lấy từ examples/, nên sửa ví dụ xong thì chạy lại script này.
"""
import os
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
S = 2            # hệ số phóng
W = 1200         # bề ngang logic
PAD = 56         # lề ngoài
GAP = 28         # khoảng giữa hai cột, giữa các thẻ
CARD_PAD = 28

BG = "#0d1728"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
FAINT = "#64748b"
SCHEMES = {
    "bad": {"fill": "#211b2e", "line": "#f87171", "label": "#f87171", "hl": "#5b2636", "hl_text": "#fecdd3"},
    "good": {"fill": "#14291f", "line": "#4ade80", "label": "#4ade80", "hl": "#1e4d33", "hl_text": "#bbf7d0"},
    "plain": {"fill": "#162238", "line": "#334155", "label": "#cbd5e1", "hl": "#334155", "hl_text": "#e2e8f0"},
}

_fonts = {}


def font(weight, size):
    key = (weight, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONT_DIR}/Inter-{weight}.otf", size * S)
    return _fonts[key]


def tw(text, f):
    return f.getlength(text) / S


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
        self.size = size

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
        rows = (len(self.pairs) + 1) // 2
        return rows * self.ROW + 14

    def draw(self, d, x, y, width, scheme):
        col = width / 2
        for i, (num, label) in enumerate(self.pairs):
            cx = x + (i % 2) * col
            cy = y + (i // 2) * self.ROW
            d.text((cx * S, cy * S), num, font=font("Bold", 30), fill=scheme["label"])
            lines = wrap([(w, False) for w in label.split()], font("Regular", 15), col - 16)
            for j, line in enumerate(lines[:2]):
                d.text((cx * S, (cy + 38 + j * 19) * S), " ".join(w for w, _ in line),
                       font=font("Regular", 15), fill=MUTED)
        return y + self.height(width)


class Card:
    def __init__(self, label, kind, blocks, score=None):
        self.label, self.kind, self.blocks, self.score = label, kind, blocks, score

    def height(self, width):
        inner = width - 2 * CARD_PAD
        return CARD_PAD + 44 + sum(b.height(inner) for b in self.blocks) + CARD_PAD - 10

    def draw(self, d, x, y, width):
        sc = SCHEMES[self.kind]
        h = self.height(width)
        d.rounded_rectangle([x * S, y * S, (x + width) * S, (y + h) * S], radius=18 * S,
                            fill=sc["fill"], outline=sc["line"], width=2 * S)
        d.text(((x + CARD_PAD) * S, (y + CARD_PAD - 2) * S), self.label, font=font("Bold", 21), fill=sc["label"])
        if self.score:
            f = font("Bold", 17)
            w = tw(self.score, f) + 24
            bx = x + width - CARD_PAD - w
            d.rounded_rectangle([bx * S, (y + CARD_PAD - 5) * S, (bx + w) * S, (y + CARD_PAD + 27) * S],
                                radius=16 * S, fill=sc["hl"])
            d.text(((bx + 12) * S, (y + CARD_PAD + 0.5) * S), self.score, font=f, fill=sc["hl_text"])
        cy = y + CARD_PAD + 44
        for b in self.blocks:
            cy = b.draw(d, x + CARD_PAD, cy, width - 2 * CARD_PAD, sc)
        return y + h


def compose(name, title, subtitle, left, right, footer=None, title_size=40, equal=True):
    col = (W - 2 * PAD - GAP) / 2
    head = PAD + title_size * 1.25 + (30 if subtitle else 0) + 26

    def col_height(cards):
        return sum(c.height(col) for c in cards) + GAP * (len(cards) - 1)

    body = max(col_height(left), col_height(right))
    if equal:  # kéo thẻ cuối mỗi cột cho hai cột bằng đáy
        for cards in (left, right):
            extra = body - col_height(cards)
            if extra > 0:
                cards[-1].blocks.append(Spacer(extra))
    foot = (22 + 26 * len(footer)) if footer else 0
    H = int(head + body + foot + PAD)
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    d.text((PAD * S, (PAD - 6) * S), title, font=font("Bold", title_size), fill="#f8fafc")
    if subtitle:
        d.text((PAD * S, (PAD + title_size * 1.25 + 2) * S), subtitle, font=font("Regular", 20), fill=MUTED)
    for cards, x in ((left, PAD), (right, PAD + col + GAP)):
        y = head
        for c in cards:
            y = c.draw(d, x, y, col) + GAP
    if footer:
        y = head + body + 22
        for i, line in enumerate(footer):
            d.text((PAD * S, y * S), line, font=font("Regular", 17 if i == 0 else 15),
                   fill="#cbd5e1" if i == 0 else FAINT)
            y += 26
    path = OUT / name
    img.save(path, optimize=True)
    print(f"{path.relative_to(ROOT)}  {img.size[0]}x{img.size[1]}  {path.stat().st_size // 1024} KB")


class Spacer(Block):
    def __init__(self, h):
        self.h = h

    def height(self, width):
        return self.h

    def draw(self, d, x, y, width, scheme):
        return y + self.h


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").strip()


# Cụm máy quét bắt trong examples/truoc.md (xem kết quả scan.py trong README)
EMAIL_TELLS = [
    "Trong bối cảnh hiện nay", "không chỉ là xu hướng mà còn", "yếu tố then chốt", "nâng tầm",
    "Điều này", "được chứng minh bởi", "nhiều nghiên cứu chỉ ra", "một cách đáng kể", "Bên cạnh đó",
    "tiến hành thực hiện việc", "nhằm mục đích", "trải nghiệm liền mạch", "Nó giúp", "trở nên dễ dàng",
    "Hy vọng những thông tin trên",
]
SLIDES_AI = ["Chuyển đổi số: Hành trình kiến tạo giá trị", "Tổng quan", "Thách thức", "3 trụ cột giải pháp",
             "Lợi ích", "Kết luận", "Cảm ơn"]
SLIDES_HUMAN = ["Đề xuất thuê thêm 1 QA cho quý 1/2027", "Quý 3 trễ 2 tuần, cả 2 lần đều do thiếu người test",
                "Thuê 1 QA rẻ hơn tiếp tục trễ", "Cần anh duyệt trước 30/11 để kịp tuyển"]
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
        "email_title": "Email, báo cáo", "email_sub": "Cùng một nội dung. Chỗ tô đỏ là cụm máy quét bắt được.",
        "email_note": "Bản này ngắn vì skill không bịa số liệu.",
        "slide_title": "Tiêu đề slide", "slide_sub": "Đọc lướt tiêu đề có biết cần quyết gì không?",
        "slide_ai": "AI làm", "slide_skill": "Làm theo skill",
        "slide_note_ai": "Bảy tiêu đề, không tiêu đề nào nói kết luận.",
        "slide_note": "Bốn tiêu đề đọc liền là hiểu cả đề xuất.",
        "post_title": "Bài đăng dài", "post_sub": "Từng câu đã sạch, nhưng cả bài lặp lại vài kiểu câu.",
        "post_before": "Bài gốc", "post_after": "Bản viết lại",
        "stats_before": [("1.740", "chữ, chia chín mục viết hoa"), ("10", 'câu kiểu "không phải X mà là Y"'),
                         ("6", 'câu mở bằng nhãn "nói gọn", "nói cho thật"'), ("19/88", "câu có dấu hai chấm")],
        "stats_after": [("373", "chữ, không chia mục"), ("1", "việc: rủ người vào làm cùng")],
        "post_old": "Máy quét bản cũ chỉ chấm 3/100 vì từ AI quen mặt đã bỏ gần hết.",
        "post_new": "Không thêm dữ kiện nào ngoài bài gốc.",
    },
    "en": {
        "sfx": ".en", "ai": "AI draft", "skill": "After the skill", "detail": "With details you supplied",
        "email_title": "Emails and reports", "email_sub": "Same content. Red marks are what the scanner flags.",
        "email_note": "Short, because the skill does not invent numbers.",
        "slide_title": "Slide titles", "slide_sub": "Can you tell what to decide from the titles alone?",
        "slide_ai": "Made by AI", "slide_skill": "Made with the skill",
        "slide_note_ai": "Seven titles, none of them states a conclusion.",
        "slide_note": "Four titles read in order give the whole proposal.",
        "post_title": "A long post", "post_sub": "Each sentence is clean, but the post repeats a few shapes.",
        "post_before": "Original", "post_after": "Rewrite",
        "stats_before": [("1,740", "words under nine all-caps headings"), ("10", '"not X but Y" sentences'),
                         ("6", 'sentences opening with a label ("nói gọn")'), ("19/88", "sentences with a colon")],
        "stats_after": [("373", "words, no headings"), ("1", "job: invite people to join")],
        "post_old": "The old scanner gave it 3/100: the familiar AI words were already gone.",
        "post_new": "Adds no fact that the original lacks.",
    },
}


def banner():
    before = ("Trong bối cảnh hiện nay, việc ứng dụng AI không chỉ là xu hướng mà còn là yếu tố then chốt. "
              "Bên cạnh đó, đội ngũ của chúng tôi đã tiến hành thực hiện việc triển khai hệ thống mới nhằm mục đích "
              "mang lại trải nghiệm liền mạch cho khách hàng... Hy vọng những thông tin trên sẽ hữu ích cho bạn!")
    compose(
        "banner.png", "Viết như người", "Chống giọng văn AI cho tiếng Việt · skill cho Claude và các trợ lý AI khác",
        [Card("Trước: văn AI", "bad", [Para(before, EMAIL_TELLS, size=21)], "84/100")],
        [Card("Sau: giọng người", "good",
              [Para(read("examples/sau.md"), size=21, after=18),
               Para("Bỏ câu sáo rỗng, giữ đúng ý, không thêm số liệu.", size=16, color=MUTED, after=4)], "0/100")],
        footer=['Bỏ văn dịch · "việc/sự/một cách" · giọng công văn · lời chatbot · xưng hô sai vai',
                "github.com/anhnx000/viet-nhu-nguoi · MIT"],
        title_size=56)


def email(t):
    compose(
        f"vi-du-email{t['sfx']}.png", t["email_title"], t["email_sub"],
        [Card(t["ai"], "bad", [Para(p, EMAIL_TELLS) for p in read("examples/truoc.md").split("\n\n")], "84/100")],
        [Card(t["skill"], "good", [Para(read("examples/sau.md")),
                                   Para(t["email_note"], size=15, color=MUTED, after=4)], "0/100"),
         Card(t["detail"], "good", [Para(read("examples/sau-co-chi-tiet.md"))], "0/100")])


def slides(t):
    compose(
        f"vi-du-slide{t['sfx']}.png", t["slide_title"], t["slide_sub"],
        [Card(t["slide_ai"], "bad", [Numbered(SLIDES_AI, SLIDE_TELLS),
                                     Para(t["slide_note_ai"], size=15, color=MUTED, after=4)], "48/100")],
        [Card(t["slide_skill"], "good", [Numbered(SLIDES_HUMAN),
                                         Para(t["slide_note"], size=15, color=MUTED, after=4)], "0/100")])


def post(t):
    paras = [p for p in read("examples/bai-dang-sau.md").split("\n\n") if not p.startswith("#")]
    compose(
        f"vi-du-bai-dang{t['sfx']}.png", t["post_title"], t["post_sub"],
        [Card(t["post_before"], "bad",
              [Stats(t["stats_before"])] + [Para(q, POST_TELLS, size=17, after=8) for q in POST_QUOTES]
              + [Para(t["post_old"], size=15, color=MUTED, after=4)], "55/100")],
        [Card(t["post_after"], "good",
              [Stats(t["stats_after"]), Para(paras[0], size=17, after=10),
               Para("[...]", size=17, color=FAINT, after=10), Para(paras[-1], size=17, after=12),
               Para(t["post_new"], size=15, color=MUTED, after=4)], "0/100")])


if __name__ == "__main__":
    banner()
    for lang in ("vi", "en"):
        email(T[lang])
        slides(T[lang])
        post(T[lang])
