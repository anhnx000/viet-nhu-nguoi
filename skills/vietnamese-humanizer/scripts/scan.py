#!/usr/bin/env python3
"""Quét nhanh dấu hiệu văn AI bề mặt (từ ngữ, dấu câu, định dạng) trong văn bản Việt/Anh.

Dùng: python3 -I scan.py FILE      hoặc      cat FILE | python3 -I scan.py
      python3 -I scan.py FILE --json       in kết quả dạng JSON
      python3 -I scan.py FILE --max 30     thoát mã 1 nếu điểm > 30 (dùng cho CI, pre-commit)

Điểm 0-100 đo mật độ dấu hiệu bề mặt và độ đều của câu. Điểm cao nghĩa là văn bản có
nhiều thói quen viết theo khuôn, không phải xác suất văn bản do AI viết.
Chỉ bắt dấu hiệu bề mặt. Cấu trúc (bộ ba, câu chốt, sai người đọc) phải tự đọc.
"""
import argparse
import json
import re
import statistics
import sys

PATTERNS = {
    "lời chatbot": [
        r"chắc chắn rồi", r"tất nhiên rồi", r"câu hỏi (rất )?hay", r"hoàn toàn đúng",
        r"hy vọng (điều này|(những )?thông tin (này|trên)|bài viết)", r"đừng ngần ngại", r"bạn có muốn tôi",
        r"dưới đây là", r"\bcertainly!", r"\bof course!", r"great question",
        r"you'?re absolutely right", r"i hope this helps", r"let me know if",
        r"as an ai language model", r"here is an? ",
    ],
    "câu dẫn": [
        r"hãy cùng (tìm hiểu|khám phá)", r"nói thẳng ra", r"thành thật mà nói\?",
        r"ít ai (biết|dám nói)", r"không ai nói", r"let'?s dive in", r"here'?s the thing",
        r"here'?s what you need to know", r"without further ado",
    ],
    "đối lập giả": [
        r"không (chỉ|đơn thuần|phải)\b.{0,80}?\bmà (còn|là)", r"chứ không phải",
        r"\bnot (just|only|merely)\b.{0,80}?\bbut\b", r"\bit'?s not\b.{0,60}?\bit'?s\b",
    ],
    "tổng kết rỗng": [
        r"^\s*(tóm lại|nhìn chung|nói tóm lại|kết luận lại)", r"\bin conclusion\b",
        r"\bto sum up\b", r"\bin summary\b",
    ],
    "thổi phồng": [
        r"(đóng vai trò|yếu tố) (quan trọng|then chốt|chủ chốt)", r"không thể phủ nhận",
        r"minh chứng", r"bước ngoặt", r"dấu ấn sâu đậm", r"kỷ nguyên mới",
        r"tương lai đầy hứa hẹn", r"khẳng định vị thế", r"hơn bao giờ hết",
        r"stands? as a testament", r"pivotal moment", r"the future looks bright",
        r"plays? a (key|crucial|pivotal) role",
    ],
    "từ vựng AI (vi)": [
        r"bức tranh (toàn cảnh)?", r"hành trình", r"\bkhám phá\b", r"nâng tầm",
        r"đáng chú ý là", r"(^|[.!?]\s+)\s*bên cạnh đó",
        r"(^|[.!?]\s+)\s*ngoài ra", r"trong bối cảnh hiện nay", r"thời đại (số|4\.0)", r"kỷ nguyên số",
        r"không ngừng thay đổi", r"điều quan trọng cần lưu ý", r"mang lại giá trị",
        r"góp phần thúc đẩy", r"đa dạng và phong phú", r"chìa khóa", r"đòn bẩy", r"bệ phóng",
        r"kiến tạo", r"\bđồng hành\b", r"lan tỏa", r"hệ sinh thái", r"giá trị cốt lõi",
        r"mở ra cánh cửa", r"tiềm năng to lớn", r"\bvô vàn\b", r"không còn là xu hướng",
    ],
    "văn dịch (vi)": [
        r"\b(được|bị)\b[^.!?\n]{1,60}?\bbởi\b", r"mở khóa tiềm năng", r"điều hướng (sự|những) phức tạp",
        r"tác động có ý nghĩa", r"(ở|tại) (cấp độ )?cốt lõi", r"trải nghiệm liền mạch",
        r"tận dụng (sức mạnh|khả năng|tối đa)", r"khi nói đến", r"là một trong những\b.{0,40}?\bnhất",
        r"đây là lý do (tại sao|vì sao)", r"có (một số|nhiều) cách để", r"được biết đến (như|là)",
        r"với sự (hỗ trợ|giúp đỡ) của",
    ],
    "động từ rỗng (vi)": [
        r"tiến hành (thực hiện|việc)?", r"thực hiện việc", r"nhằm mục đích",
        r"(đưa ra|cung cấp) sự (hỗ trợ|giúp đỡ)", r"hiện thực hóa", r"đóng góp vào",
    ],
    "danh hóa (vi)": [
        r"một cách \w+", r"trở nên \w+", r"có khả năng \w+",
    ],
    "thừa nghĩa (vi)": [
        r"quay trở lại", r"hiện nay đang", r"đang trong quá trình", r"hoàn toàn đầy đủ",
        r"cùng chung", r"các những", r"mọi tất cả", r"\btái \w+ lại\b", r"vẫn còn đang",
    ],
    "từ vựng AI (en)": [
        r"\badditionally\b", r"\balign(s|ed)? with\b", r"\bboasts?\b", r"\bbolstered\b",
        r"\bcrucial\b", r"\bdeep dive\b", r"\bdelve", r"\benduring\b", r"\benhanc",
        r"\bfoster", r"\bgarner", r"\bhighlight(s|ed|ing)?\b", r"\binterplay\b",
        r"\bintricat", r"\blandscape\b", r"\bleverag", r"\bmeticulous", r"\bmultifaceted\b",
        r"\bnavigat(e|ing) the", r"\bpivotal\b", r"\brobust\b", r"\bseamless", r"\bshowcas",
        r"\btapestry\b", r"\btestament\b", r"\bunderscor", r"\bvibrant\b",
        r"today'?s fast-paced", r"it'?s important to note", r"ever-evolving",
    ],
    "quảng cáo": [
        r"nằm giữa lòng", r"vị trí đắc địa", r"ngỡ ngàng", r"không thể bỏ qua", r"đẳng cấp",
        r"\bnestled\b", r"\bbreathtaking\b", r"\bmust-visit\b", r"\brenowned\b",
    ],
    "uy tín mơ hồ": [
        r"các chuyên gia (cho rằng|nhận định)", r"nhiều nghiên cứu (chỉ ra|cho thấy)",
        r"giới quan sát", r"experts (believe|argue|say)", r"industry reports",
    ],
    "né là/có": [
        r"đóng vai trò là", r"tự hào (có|sở hữu)", r"\bserves as\b", r"\bstands as\b",
    ],
    "giới hạn kiến thức": [
        r"tính đến thời điểm (cập nhật|huấn luyện)", r"dựa trên thông tin hiện có",
        r"as of my (last|knowledge)", r"based on available information",
    ],
    "dấu vết công cụ": [
        r"contentReference", r"oaicite", r"turn0search\d", r"\[cite: ?\d+\]", r":::writing",
    ],
}

DASH = re.compile(r"[—–]| -- ")
CURLY = re.compile(r"[“”‘’]")
BOLD_LABEL = re.compile(r"^\s*([-*+]|\d+\.)\s+(\S+\s+)?\*\*[^*]+:?\*\*:?")
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF✅✨➡→]")
FENCE = re.compile(r"^\s*```")
# Chêm tiếng Anh trong ngoặc sau từ Việt: "hiệu suất (performance)"
EN_GLOSS = re.compile(r"\w*[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]\w*\s+\(([a-z][a-z ]{2,30})\)")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
NOMINAL = re.compile(r"\b(việc|sự)\b")
THIS_IT = re.compile(r"^(điều này|điều đó|nó)\b")


def scan(text):
    hits = {}
    in_code = False
    lines = text.splitlines()
    for no, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        prose = re.sub(r"`[^`]*`|https?://\S+", "", line)
        low = prose.lower()
        for group, pats in PATTERNS.items():
            for p in pats:
                for m in re.finditer(p, low, re.MULTILINE):
                    hits.setdefault(group, []).append((no, m.group(0).strip(" .!?")))
        for name, rx in (("gạch ngang dài", DASH), ("ngoặc cong", CURLY),
                         ("emoji/mũi tên", EMOJI)):
            n = len(rx.findall(prose))
            if n:
                hits.setdefault(name, []).append((no, f"x{n}"))
        if BOLD_LABEL.match(prose):
            hits.setdefault("nhãn in đậm", []).append((no, prose.strip()[:40]))
        for m in EN_GLOSS.finditer(low):
            if prose[m.start(1):m.end(1)].islower():  # bỏ qua viết tắt như (MIT), (API)
                hits.setdefault("chêm tiếng Anh", []).append((no, m.group(0)))
        sentence_checks(prose, no, hits)
    return hits, len(lines)


def sentence_checks(prose, no, hits):
    """Dấu hiệu theo câu: chuỗi "của", "việc/sự" dày, "Điều này"/"Nó" mở câu, câu dài đều."""
    sents = [x.strip() for x in SENT_SPLIT.split(prose.strip()) if x.strip()]
    lengths = []
    for sent in sents:
        low = sent.lower().lstrip("-*>#0123456789. ")
        words = low.split()
        lengths.append(len(words))
        if len(re.findall(r"\bcủa\b", low)) >= 3:
            hits.setdefault("chuỗi \"của\"", []).append((no, sent[:50]))
        if len(NOMINAL.findall(low)) >= 3:
            hits.setdefault("việc/sự dày", []).append((no, sent[:50]))
        if THIS_IT.match(low):
            hits.setdefault("\"Điều này\"/\"Nó\" mở câu", []).append((no, sent[:40]))
    # Ba câu liền nhau trở lên, mỗi câu 20 chữ trở lên, chênh nhau không quá 4 chữ
    run = 1
    for a, b in zip(lengths, lengths[1:]):
        run = run + 1 if a >= 20 and b >= 20 and abs(a - b) <= 4 else 1
        if run == 3:
            hits.setdefault("câu dài đều nhau", []).append((no, f"{lengths}"))


# Trọng số theo độ mạnh của dấu hiệu. Nhóm không có tên ở đây tính 1.
WEIGHTS = {
    "lời chatbot": 3, "câu dẫn": 3, "đối lập giả": 3, "tổng kết rỗng": 3,
    "giới hạn kiến thức": 3, "dấu vết công cụ": 3, "văn dịch (vi)": 3, "động từ rỗng (vi)": 3,
    "thổi phồng": 2, "uy tín mơ hồ": 2, "quảng cáo": 2, "từ vựng AI (vi)": 2,
    "từ vựng AI (en)": 2, "né là/có": 2, "danh hóa (vi)": 2, "thừa nghĩa (vi)": 2,
    "chuỗi \"của\"": 2, "việc/sự dày": 2, "\"Điều này\"/\"Nó\" mở câu": 2,
}
BANDS = ((10, "sạch"), (30, "vài dấu hiệu"), (60, "nhiều dấu hiệu"), (101, "dày đặc"))


def prose_only(text):
    out, in_code = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_code = not in_code
            continue
        if not in_code:
            out.append(re.sub(r"`[^`]*`|https?://\S+", "", line))
    return "\n".join(out)


def score(text, hits):
    """Điểm 0-100: mật độ dấu hiệu có trọng số trên 100 chữ, cộng phần phạt khi câu dài đều nhau."""
    prose = prose_only(text)
    words = len(prose.split())
    weighted = sum(WEIGHTS.get(g, 1) * len(v) for g, v in hits.items())
    density = weighted * 100 / max(words, 50)
    lengths = [len(x.split()) for x in re.split(r"(?<=[.!?])\s+|\n+", prose) if len(x.split()) >= 3]
    cv = None
    burst_penalty = 0.0
    if len(lengths) >= 5:
        cv = statistics.pstdev(lengths) / statistics.mean(lengths)
        burst_penalty = max(0.0, 0.35 - cv) * 40
    value = min(100, round(density * 2 + burst_penalty))
    band = next(name for limit, name in BANDS if value < limit)
    return {"score": value, "band": band, "words": words, "weighted_hits": weighted,
            "sentence_length_cv": None if cv is None else round(cv, 2)}


def main():
    ap = argparse.ArgumentParser(description="Quét dấu hiệu văn AI bề mặt (Việt/Anh).")
    ap.add_argument("file", nargs="?", help="file cần quét; bỏ trống thì đọc stdin")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    ap.add_argument("--max", type=int, metavar="N", help="thoát mã 1 nếu điểm lớn hơn N")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    hits, total = scan(text)
    result = score(text, hits)
    if args.json:
        result["hits"] = {g: [{"line": no, "match": m} for no, m in v] for g, v in hits.items()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not hits:
        print(f"Điểm {result['score']}/100 ({result['band']}). Không thấy dấu hiệu bề mặt. "
              "Vẫn cần tự đọc phần cấu trúc.")
    else:
        count = sum(len(v) for v in hits.values())
        print(f"Điểm {result['score']}/100 ({result['band']}): {count} dấu hiệu trong {total} dòng.\n")
        for group, items in sorted(hits.items(), key=lambda kv: -len(kv[1])):
            print(f"[{group}] {len(items)}")
            for no, s in items[:12]:
                print(f"  dòng {no}: {s}")
            if len(items) > 12:
                print(f"  ... và {len(items) - 12} chỗ khác")
        print("\nMột dấu hiệu đơn lẻ chưa nói lên gì. Nhiều nhóm cùng lúc mới đáng sửa.")
        print("Điểm đo thói quen viết theo khuôn, không phải xác suất do AI viết.")
    if args.max is not None and result["score"] > args.max:
        sys.exit(1)


if __name__ == "__main__":
    main()
