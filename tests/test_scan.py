"""Kiểm máy quét: bắt được dấu hiệu văn AI, không báo nhầm câu tự nhiên.

Chạy: python3 -m unittest discover -s tests
"""
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "skills/viet-nhu-nguoi/scripts/scan.py"
FACTS_PATH = ROOT / "skills/viet-nhu-nguoi/scripts/check_facts.py"
SPEC = importlib.util.spec_from_file_location("scan", SCAN_PATH)
scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scan)
slides = scan.slides_mod
DECK_AI = ROOT / "examples/slide-truoc.pptx"
DECK_HUMAN = ROOT / "examples/slide-sau.pptx"


def groups(text):
    hits, _ = scan.scan(text)
    return set(hits)


class DetectsAiTells(unittest.TestCase):
    def test_translationese_passive(self):
        self.assertIn("văn dịch (vi)", groups("Tính năng được phát triển bởi đội kỹ sư."))

    def test_this_it_sentence_start(self):
        self.assertIn('"Điều này"/"Nó" mở câu', groups("Hệ thống chạy. Điều này giúp tiết kiệm."))

    def test_empty_verbs(self):
        self.assertIn("động từ rỗng (vi)", groups("Nhóm tiến hành thực hiện việc rà soát."))

    def test_nominalisation(self):
        self.assertIn("danh hóa (vi)", groups("Làm việc một cách hiệu quả."))

    def test_redundancy(self):
        self.assertIn("thừa nghĩa (vi)", groups("Dự án hiện nay đang chạy."))

    def test_chain_of_cua(self):
        self.assertIn('chuỗi "của"', groups("Sự tăng của năng suất của nhân viên của công ty."))

    def test_english_gloss(self):
        self.assertIn("chêm tiếng Anh", groups("Cải thiện hiệu suất (performance) rõ."))

    def test_false_contrast(self):
        self.assertIn("đối lập giả", groups("Đây không chỉ là công cụ mà còn là người bạn."))

    def test_chatbot_closing(self):
        self.assertIn("lời chatbot", groups("Hy vọng những thông tin trên sẽ hữu ích cho bạn!"))

    def test_em_dash(self):
        self.assertIn("gạch ngang dài", groups("Kết quả — như dự đoán — rất tốt."))

    def test_example_before(self):
        text = (ROOT / "examples/truoc.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(groups(text)), 6)


class KeepsHumanText(unittest.TestCase):
    def test_casual_chat(self):
        self.assertEqual(groups("Mai mình ghé muộn chút nhé, bạn cứ ăn trước đi."), set())

    def test_dev_jargon(self):
        self.assertEqual(groups("Deploy xong rồi, anh check giúp em cái PR nhé."), set())

    def test_mot_cach_meaning_one_way(self):
        self.assertNotIn("danh hóa (vi)", groups("Cả deck chỉ dùng một cách gọi. Có một cách khác là hỏi Lan."))

    def test_acronym_in_parens(self):
        self.assertEqual(groups("Phát hành theo giấy phép mã nguồn mở (MIT)."), set())

    def test_code_block_ignored(self):
        self.assertEqual(groups("```\nx = 'được gọi bởi' — tiến hành\n```"), set())

    def test_examples_after(self):
        for name in ("sau.md", "sau-co-chi-tiet.md"):
            text = (ROOT / "examples" / name).read_text(encoding="utf-8")
            self.assertEqual(groups(text), set(), name)


class Score(unittest.TestCase):
    def test_ai_draft_scores_high(self):
        text = (ROOT / "examples/truoc.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(scan.score(text, scan.scan(text)[0])["score"], 60)

    def test_rewrite_scores_zero(self):
        text = (ROOT / "examples/sau-co-chi-tiet.md").read_text(encoding="utf-8")
        result = scan.score(text, scan.scan(text)[0])
        self.assertEqual((result["score"], result["band"]), (0, "sạch"))

    def test_max_flag_exit_code(self):
        cmd = [sys.executable, "-I", str(SCAN_PATH), str(ROOT / "examples/truoc.md"), "--max", "30"]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
        cmd[3] = str(ROOT / "examples/sau.md")
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)


class CheckFacts(unittest.TestCase):
    def run_check(self, old, new):
        with tempfile.TemporaryDirectory() as d:
            a, b = pathlib.Path(d, "a.md"), pathlib.Path(d, "b.md")
            a.write_text(old, encoding="utf-8")
            b.write_text(new, encoding="utf-8")
            return subprocess.run([sys.executable, "-I", str(FACTS_PATH), str(a), str(b)],
                                  capture_output=True, text=True)

    def test_same_facts_pass(self):
        r = self.run_check("Bản 2.3 được phát hành bởi đội Android lúc 15:00 ngày 30/4.",
                           "Đội Android phát hành bản 2.3 lúc 15:00 ngày 30/4.")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_changed_number_fails(self):
        r = self.run_check("Doanh thu tăng 12% theo https://example.com/a.",
                           "Doanh thu tăng mạnh 15% theo https://example.com/a.")
        self.assertEqual(r.returncode, 1)
        self.assertIn("12%", r.stdout)
        self.assertIn("15%", r.stdout)

    def test_lost_code_fails(self):
        r = self.run_check("Chạy `npm test` trước khi push.", "Chạy test trước khi push.")
        self.assertEqual(r.returncode, 1)

    def test_code_moved_into_block_passes(self):
        r = self.run_check("Chạy `npm test` (hoặc `npm run lint`) trước khi push.",
                           "Chạy trước khi push:\n\n```bash\nnpm test\nnpm run lint\n```\n")
        self.assertEqual(r.returncode, 0, r.stdout)


def scan_deck(path):
    deck = slides.read_pptx(str(path))
    text, index = slides.to_text(deck)
    hits, _ = scan.scan(text)
    scan.slide_checks(deck, index, hits)
    return deck, text, hits


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def sp(text, ph=None):
    nv = f'<p:nvPr><p:ph type="{ph}"/></p:nvPr>' if ph else "<p:nvPr/>"
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="x"/><p:cNvSpPr/>{nv}</p:nvSpPr>'
            f'<p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')


def tiny_deck(path):
    """Deck tối thiểu viết tay: thứ tự slide trong presentation.xml ngược với tên file, có ghi chú."""
    head = f'<p:sld xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree>'
    tailx = "</p:spTree></p:cSld></p:sld>"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("ppt/presentation.xml",
                   f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst>'
                   '<p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId1"/></p:sldIdLst></p:presentation>')
        z.writestr("ppt/_rels/presentation.xml.rels",
                   f'<Relationships xmlns="{REL}">'
                   '<Relationship Id="rId1" Type="x" Target="slides/slide1.xml"/>'
                   '<Relationship Id="rId2" Type="x" Target="slides/slide2.xml"/></Relationships>')
        z.writestr("ppt/slides/slide1.xml", head + sp("Slide thứ hai", "title") + sp("Nội dung B") + tailx)
        z.writestr("ppt/slides/slide2.xml", head + sp("Slide đầu", "title") + sp("Nội dung A") + tailx)
        z.writestr("ppt/slides/_rels/slide1.xml.rels",
                   f'<Relationships xmlns="{REL}"><Relationship Id="rId9" Type="{R}/notesSlide" '
                   'Target="../notesSlides/notesSlide1.xml"/></Relationships>')
        z.writestr("ppt/notesSlides/notesSlide1.xml",
                   f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree>'
                   + sp("3", "sldNum") + sp("Lời nói cho slide B", "body") + "</p:spTree></p:cSld></p:notes>")


class Slides(unittest.TestCase):
    def test_reads_order_titles_and_notes(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d, "t.pptx")
            tiny_deck(path)
            deck = slides.read_pptx(str(path))
        self.assertEqual([s["title"] for s in deck], ["Slide đầu", "Slide thứ hai"])
        self.assertEqual(deck[1]["body"], ["Nội dung B"])
        self.assertEqual(deck[1]["notes"], ["Lời nói cho slide B"])  # bỏ số trang
        self.assertEqual(deck[0]["notes"], [])

    def test_ai_deck_slide_tells(self):
        deck, _, hits = scan_deck(DECK_AI)
        self.assertEqual(len(deck), 7)
        for group in ("tiêu đề dạng nhãn", "tiêu đề đếm số ý", "số gạch đầu dòng đều",
                      "hứa suông", "câu khó nói (ghi chú)", "ngoặc trong lời nói"):
            self.assertIn(group, hits)
        titles = [m for _, m in hits["tiêu đề dạng nhãn"]]
        self.assertNotIn("Cảm ơn", titles)  # slide cảm ơn và slide bìa không bị bắt

    def test_label_prefix_title(self):
        deck = [{"no": 1, "title": "Bìa: tên dự án", "body": [], "table": [], "notes": [], "hidden": False},
                {"no": 2, "title": "Kỳ vọng: chi phí thấp hơn", "body": [], "table": [], "notes": [],
                 "hidden": False},
                {"no": 3, "title": "Quý 3 trễ 2 tuần vì thiếu người test", "body": [], "table": [],
                 "notes": [], "hidden": False}]
        _, index = slides.to_text(deck)
        hits = {}
        scan.slide_checks(deck, index, hits)
        self.assertEqual([m for _, m in hits["tiêu đề có tiền tố nhãn"]], ["Kỳ vọng: chi phí thấp hơn"])

    def test_human_deck_clean(self):
        _, text, hits = scan_deck(DECK_HUMAN)
        self.assertEqual(hits, {})
        self.assertEqual(scan.score(text, hits, burst=False)["score"], 0)

    def test_cli_labels_and_titles(self):
        r = subprocess.run([sys.executable, "-I", str(SCAN_PATH), str(DECK_AI)], capture_output=True, text=True)
        self.assertIn("slide 2, ghi chú", r.stdout)
        r = subprocess.run([sys.executable, "-I", str(SCAN_PATH), "--titles", str(DECK_HUMAN)],
                           capture_output=True, text=True)
        self.assertIn("2. Quý 3 trễ 2 tuần", r.stdout)

    def test_cli_text_dump(self):
        r = subprocess.run([sys.executable, "-I", str(SCAN_PATH), "--text", str(DECK_AI)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        block = r.stdout.split("=== Slide 2")[1].split("=== Slide 3")[0]
        self.assertIn("Tiêu đề: Tổng quan", block)
        self.assertIn("Như chúng ta có thể thấy", block)  # ghi chú nằm đúng slide 2

    def test_check_facts_on_pptx(self):
        same = subprocess.run([sys.executable, "-I", str(FACTS_PATH), str(DECK_HUMAN), str(DECK_HUMAN)],
                              capture_output=True, text=True)
        self.assertEqual(same.returncode, 0, same.stdout)
        diff = subprocess.run([sys.executable, "-I", str(FACTS_PATH), str(DECK_HUMAN), str(DECK_AI)],
                              capture_output=True, text=True)
        self.assertEqual(diff.returncode, 1)
        self.assertIn("30/11", diff.stdout)


class WholeDocument(unittest.TestCase):
    """Bài đã sạch từng câu vẫn lộ khi nhìn cả bài: nhãn báo giọng, khuôn lặp, hai chấm, đoạn đều."""

    PARA = ("Kernel giữ phần cấp quyền và chia CPU. Driver chạy ở ngoài như một app thường.\n\n"
            "Nói cho công bằng: cách này vẫn có giá. Khó nhất không phải là code, mà là chọn việc.\n\n"
            "Mình không cần bạn giỏi kernel. Mình cần bạn chịu đọc log.\n\n")

    def long_post(self):
        return ("MÌNH ĐANG VIẾT MỘT HỆ ĐIỀU HÀNH\n\n" + self.PARA
                + "".join(f"PHẦN SỐ {i}, NÓI GỌN\n\n" + self.PARA * 3 for i in range(4))
                + "KẾT\n\nNói rõ để bạn khỏi kỳ vọng sai: đây là dự án nghiên cứu.\n\n#OSDev #Rust\n")

    def test_chopped_sentences(self):
        chopped = "Skill giúp văn dễ đọc hơn. Skill không lừa máy dò. Thường mất một phút.\n\n" * 8
        self.assertIn("câu vụn", scan.scan(chopped)[0])
        joined = ("Skill giúp văn bản dễ đọc hơn nhưng không cam kết qua được máy dò, "
                  "và việc cài thường mất chưa tới một phút trên máy đã có sẵn git.\n\n") * 24
        self.assertNotIn("câu vụn", scan.scan(joined)[0])
        self.assertNotIn("câu vụn", scan.scan("Ngắn thôi. Hai câu.\n")[0])

    def test_meta_skips_quoted_examples(self):
        doc = ('Skill bỏ các cụm như "trong bối cảnh hiện nay" và "nâng tầm".\n\n'
               "> Điều này được chứng minh bởi nhiều nghiên cứu chỉ ra rằng năng suất tăng.\n\n"
               "| Động từ rỗng | tiến hành thực hiện việc rà soát |\n")
        self.assertTrue(scan.scan(doc)[0])
        self.assertEqual(scan.scan(doc, meta=True)[0], {})
        plain = "Trong bối cảnh hiện nay, đội đã tiến hành thực hiện việc rà soát.\n"
        self.assertTrue(scan.scan(plain, meta=True)[0])

    def test_lead_in_colon_not_counted(self):
        lead = "".join(f"Bước {i} cần ba thứ sau đây cho đủ bộ hồ sơ gửi đi:\n\n- một\n- hai\n\n" for i in range(24))
        self.assertNotIn("hai chấm dồn dập", scan.scan(lead)[0])
        staged = "Chi tiết quan trọng nhất: máy đã nhanh hơn trước rất nhiều rồi đấy nhé.\n\n" * 24
        self.assertIn("hai chấm dồn dập", scan.scan(staged)[0])

    def test_overlong_sentence(self):
        long_sent = "Đội mình " + "làm thêm một việc nữa, " * 14 + "rồi mới nghỉ.\n"
        self.assertIn("câu quá dài", scan.scan(long_sent)[0])
        self.assertNotIn("câu quá dài", scan.scan("Đội mình làm xong việc rồi mới nghỉ.\n")[0])

    HUMAN = {
        "email": ("Chào chị Lan,\n\nEm gửi chị bản báo cáo quý 3, chị xem giúp em phần chi phí ở trang 4 "
                  "vì em chưa chắc số bên kế toán đưa đã gồm thuế chưa. Nếu được thì chị phản hồi trước thứ Sáu "
                  "để em kịp sửa trước buổi họp.\n\nEm cảm ơn chị.\nMinh\n"),
        "chat": "Ê mai họp mấy giờ thế?\n\n9 rưỡi nhé, phòng tầng 3.\n\nOk để tao báo thằng Tú.\n",
        "post": ("Hôm qua mình mất gần ba tiếng chỉ để tìm ra một dấu chấm phẩy đặt nhầm chỗ trong file cấu hình. "
                 "Lúc đầu mình cứ tưởng lỗi do thư viện mới cập nhật nên quay về bản cũ, cài lại hai lần mà vẫn không chạy. "
                 "Đến lúc thằng em cùng phòng đi ngang qua liếc một cái rồi chỉ vào dòng 14 thì mình chỉ muốn chui xuống gầm bàn.\n\n"
                 "Kể ra để nhắc bản thân lần sau đọc kỹ thông báo lỗi trước khi đổ cho người khác.\n"),
        "report": ("Tuần này nhóm hoàn thành 7 trên 9 việc đã nhận. Hai việc còn lại bị chậm vì phải chờ bên đối tác "
                   "gửi tài liệu mô tả API, họ hẹn thứ Ba tuần sau.\n\nKhách hàng phản ánh 3 lỗi trên bản thử nghiệm, "
                   "trong đó lỗi đăng nhập đã sửa xong hôm thứ Năm, hai lỗi hiển thị sẽ sửa trong tuần tới.\n"),
    }

    def test_human_samples_have_no_document_tells(self):
        doc_groups = set(scan.DOC_POINTS) | {"tật lặp cả bài", "mục kết dán nhãn", "câu quá dài"}
        for name, text in self.HUMAN.items():
            with self.subTest(name):
                self.assertFalse(doc_groups & set(scan.scan(text)[0]))

    def test_voice_labels(self):
        for text in ("Nói cho thật: tiến độ không dễ.", "Nói rõ để bạn khỏi kỳ vọng sai: đây là bản thử.",
                     "HỆ ĐIỀU HÀNH LÀ GÌ, NÓI GỌN", "Vibe coding, hiểu đơn giản là ngồi nói chuyện với AI.",
                     "Thành thật mà nói, mình cũng chưa chắc."):
            self.assertIn("nhãn báo giọng", groups(text), text)

    def test_plain_noi_ro_is_not_a_label(self):
        self.assertEqual(groups("Anh nói rõ giúp em hạn nộp nhé."), set())
        self.assertEqual(groups("Chị ấy nói thật với mình là chưa xong."), set())

    def test_contrast_variants(self):
        for text in ("Mình không cần bạn giỏi kernel. Mình cần bạn chịu đọc log.",
                     "Con số đó không nói Linux dở. Nó nói một điều khác.",
                     "Việt Nam không đi theo lối mua chip, mà bắt đầu từ thiết kế.",
                     "Driver nằm ở user space chứ không nhét vào kernel."):
            self.assertIn("đối lập giả", groups(text), text)

    def test_khong_phai_meaning_need_not(self):
        self.assertNotIn("đối lập giả", groups("Khách tự xem tiến độ, không phải nhắn hỏi như trước."))

    def test_restating_and_outline(self):
        self.assertIn("diễn giải lại", groups("Bản đo lệch 5%. Tức là thiết kế cũ mới chậm."))
        self.assertIn("tự kể dàn ý", groups("Bài này mình viết để kể dự án cho người mới."))

    def test_long_post_is_not_diluted(self):
        text = self.long_post()
        hits, _ = scan.scan(text)
        for group in ("tật lặp cả bài", "hai chấm dồn dập", "đoạn ngắn đều nhau",
                      "bài đăng chia mục viết hoa", "mục kết dán nhãn"):
            self.assertIn(group, hits)
        result = scan.score(text, hits)
        self.assertGreaterEqual(result["document_points"], 30)
        self.assertGreaterEqual(result["score"], 30)

    def test_long_post_example(self):
        """Bài đăng thật: bản gốc lộ vì lặp khuôn cả bài, bản viết lại sạch và không thêm số liệu."""
        before = (ROOT / "examples/bai-dang-truoc.md").read_text(encoding="utf-8")
        after = (ROOT / "examples/bai-dang-sau.md").read_text(encoding="utf-8")
        hits, _ = scan.scan(before)
        self.assertGreaterEqual(scan.score(before, hits)["score"], 40)
        self.assertGreaterEqual(len(hits["đối lập giả"]), 8)
        self.assertGreaterEqual(len(hits["nhãn báo giọng"]), 5)
        hits, _ = scan.scan(after)
        self.assertEqual(hits, {})
        self.assertEqual(scan.score(after, hits)["score"], 0)
        numbers = lambda t: set(re.findall(r"\d[\d.,]*\d|\d", t))
        self.assertLessEqual(numbers(after), numbers(before))

    def test_one_contrast_is_not_a_tic(self):
        hits, _ = scan.scan("Lỗi nằm ở token chứ không phải timeout. Em đã thử tăng timeout rồi.")
        self.assertNotIn("tật lặp cả bài", hits)

    def test_document_checks_skip_code_and_lists(self):
        text = "# Cài đặt\n\n" + "- Bước một: tải về.\n" * 30 + "\n```\nKẾT\n```\n"
        self.assertEqual(groups(text), set())


class DeepTranslationese(unittest.TestCase):
    """Văn dịch từng chữ: không cụm nào sai nhưng câu theo khuôn tiếng Anh (nhóm K)."""

    def test_agentless_passive(self):
        self.assertIn("bị động dịch sát", groups("Số liệu bạn đưa được giữ nguyên và skill được cập nhật mỗi tuần."))
        self.assertNotIn("bị động dịch sát", groups("Email này gửi được rồi, mai em làm được."))

    def test_object_as_subject(self):
        self.assertIn("vật làm chủ ngữ", groups("Công cụ này cho phép bạn so hai bản."))
        self.assertNotIn("vật làm chủ ngữ", groups("Muốn so hai bản thì dùng công cụ này."))

    def test_calqued_openers(self):
        self.assertIn("mở câu dịch sát", groups("Để cập nhật, bạn chạy lại lệnh."))
        self.assertIn("mở câu dịch sát", groups("Với sự thay đổi này, đội làm nhanh hơn."))
        self.assertNotIn("mở câu dịch sát", groups("Muốn cập nhật thì chạy lại lệnh. Em để file trên bàn."))

    def test_calqued_idioms(self):
        self.assertIn("văn dịch (vi)", groups("Tin tốt là bản mới làm nên sự khác biệt."))
        self.assertIn("quan hệ từ dịch sát", groups("Đây là nơi mà đội họp mỗi sáng."))

    def test_calqued_set_phrases(self):
        for text in ("Đầu tiên và quan trọng nhất, lên kế hoạch cho mỗi ngày.",
                     "Cuối cùng nhưng không kém phần quan trọng, ngủ đủ giấc.",
                     "Nếu đang tìm mẹo làm việc thì bạn đã đến đúng nơi.",
                     "Như một quy tắc chung, sáng nào cũng dành mười lăm phút."):
            self.assertIn("văn dịch (vi)", groups(text), text)
        self.assertNotIn("văn dịch (vi)", groups("Trước hết là lên kế hoạch. Cuối cùng thì ngủ cho đủ."))

    def test_calqued_templates(self):
        for text in ("Tôi hy vọng email này tìm thấy anh trong tình trạng sức khỏe tốt.",
                     "Vui lòng tìm thấy tệp đính kèm là bản báo cáo cuối cùng.",
                     "Tôi mong chờ được nghe từ anh sớm.",
                     "Cho tôi biết nếu anh có bất kỳ câu hỏi hoặc mối quan tâm nào.",
                     "Sản phẩm này được thiết kế với bạn trong tâm trí.",
                     "Cho dù bạn là sinh viên hay người đi làm, đây là sự lựa chọn hoàn hảo.",
                     "Nếu vấn đề vẫn còn tồn tại, hãy liên hệ đội hỗ trợ.",
                     "Hãy chắc chắn để sao lưu dữ liệu trước khi tiếp tục."):
            self.assertIn("văn dịch (vi)", groups(text), text)
        human = ("Anh Minh ơi, em gửi bản báo cáo cuối trong file đính kèm. Anh xem có gì chưa ổn thì báo em nhé. "
                 "Máy vẫn lỗi thì khởi động lại, còn lỗi nữa thì gọi bên hỗ trợ.")
        self.assertNotIn("văn dịch (vi)", groups(human))

    def test_calqued_report_and_explainer(self):
        for text in ("Tiến về phía trước, nhóm tập trung mở rộng quy mô.",
                     "Quý này nhóm đã đạt được những tiến bộ đáng kể.",
                     "Hãy nghĩ về nó như một đứa trẻ học nhận biết con vật.",
                     "Điều đó nói rằng, học máy không phải là không có những hạn chế của nó."):
            self.assertIn("văn dịch (vi)", groups(text), text)
        self.assertIn("danh hóa (vi)", groups("Nhóm có nhiều tiến bộ trong việc cải thiện hiệu suất."))
        self.assertIn("văn dịch (vi)", groups("Chúng tôi đã làm được điều này mà không cần tăng chi phí."))
        self.assertIn("văn dịch (vi)", groups("Chúng tôi muốn gửi lời cảm ơn đặc biệt đến cả nhóm."))
        self.assertIn("quan hệ từ dịch sát", groups("Học máy là một nhánh của trí tuệ nhân tạo mà tập trung vào dữ liệu."))
        self.assertIn("quan hệ từ dịch sát", groups("Càng nhiều ví dụ mà nó nhìn thấy, nó càng giỏi."))
        self.assertIn("bị động dịch sát", groups("Mô hình không được lập trình sẵn từng bước."))
        human = ("Quý này hệ thống phản hồi nhanh hơn 30%, chi phí không tăng. Quý sau nhóm lo phần mở rộng. "
                 "Học máy giống đứa trẻ tập nhận mặt con vật, xem càng nhiều thì nhận càng đúng, nhưng cũng có giới hạn.")
        for g in ("văn dịch (vi)", "quan hệ từ dịch sát", "bị động dịch sát"):
            self.assertNotIn(g, groups(human))

    def test_dense_filler_words(self):
        translated = 'Tóm tắt cuộc họp: Đánh giá Dự án Q3\n\nNgười tham dự: Hà, Tuấn, Nga, Phong.\n\nCuộc họp bắt đầu với một cập nhật từ Hà về tiến độ hiện tại. Dự án được báo cáo là đang đi đúng hướng, mặc dù một vài rủi ro đã được nêu lên. Tuấn đã đề cập rằng việc tích hợp thanh toán có thể được trì hoãn do các vấn đề của bên thứ ba. Nhóm đã đồng ý rằng một cuộc kiểm tra sẽ được tổ chức vào tuần tới. Nga được giao nhiệm vụ cập nhật tài liệu, trong khi Phong sẽ liên hệ với nhà cung cấp. Các bước tiếp theo: hoàn tất ngân sách trước thứ Sáu và đưa các bên liên quan vào vòng lặp. Cuộc họp được hoãn lúc 3 giờ chiều.'
        human = 'Biên bản họp: Rà soát dự án quý 3\n\nTham dự: Hà, Tuấn, Nga, Phong.\n\nHà báo cáo tiến độ: dự án đang đúng kế hoạch, nhưng còn vài rủi ro. Tuấn cho biết phần tích hợp thanh toán có thể trễ vì bên thứ ba đang gặp lỗi. Cả nhóm thống nhất họp kiểm tra lại vào tuần sau. Nga cập nhật tài liệu, Phong liên hệ nhà cung cấp.\n\nViệc tiếp theo: chốt ngân sách trước thứ Sáu và báo cho các bên liên quan. Họp kết thúc lúc 15 giờ.'
        self.assertIn("chữ đệm dịch dày", groups(translated))
        self.assertNotIn("chữ đệm dịch dày", groups(human))

    def test_no_double_count_make_sure(self):
        hits, _ = scan.scan("Hãy chắc chắn rằng bạn ngủ đủ giấc.")
        self.assertEqual(len(hits["văn dịch (vi)"]), 1)

    def test_dense_pronouns(self):
        dense = "Bạn mở ứng dụng của bạn rồi bạn chọn file bạn muốn sửa trong máy tính.\n\n" * 8
        self.assertIn("đại từ dày", groups(dense))
        sparse = ("Mở ứng dụng lên rồi chọn file muốn sửa, sửa xong thì lưu lại vào đúng thư mục cũ.\n\n" * 7
                  + "Bạn nào chưa cài thì nhắn mình.\n")
        self.assertNotIn("đại từ dày", groups(sparse))


class EmptyPromises(unittest.TestCase):
    def test_detects(self):
        self.assertIn("hứa suông", groups("Chi tiết sẽ được trao đổi sau."))
        self.assertIn("hứa suông", groups("Nhóm sẽ tiếp tục nghiên cứu thêm."))

    def test_concrete_plan_ok(self):
        self.assertNotIn("hứa suông", groups("Lan gửi bảng giá chi tiết trước thứ Sáu 14/11."))


if __name__ == "__main__":
    unittest.main()
