#!/usr/bin/env python3
"""Quét nhanh dấu hiệu văn AI bề mặt (từ ngữ, dấu câu, định dạng) trong văn bản Việt/Anh.

Dùng: python3 -I scan.py FILE      hoặc      cat FILE | python3 -I scan.py
      python3 -I scan.py FILE --json       in kết quả dạng JSON
      python3 -I scan.py FILE --max 30     thoát mã 1 nếu điểm > 30 (dùng cho CI, pre-commit)
      python3 -I scan.py FILE --titles     chỉ in các tiêu đề theo thứ tự, để đọc lướt xem có thành mạch không
      python3 -I scan.py FILE.pptx --text  in toàn bộ chữ của từng slide (tiêu đề, nội dung, bảng, ghi chú)
      python3 -I scan.py FILE --chat       văn bản là tin nhắn trả lời: kiểm thêm định dạng, độ dài, câu khách sáo
FILE có thể là .md, .txt hoặc .pptx. Với .pptx, bộ kiểm tra đọc tiêu đề, nội dung, bảng và ghi chú
thuyết trình của từng slide, và chạy thêm các kiểm riêng cho slide.

Điểm theo thang 0-100, đo mật độ dấu hiệu bề mặt và độ đều của câu. Điểm cao nghĩa là văn bản có
nhiều thói quen viết theo khuôn, không phải xác suất văn bản do AI viết.
Chỉ bắt dấu hiệu bề mặt. Cấu trúc (bộ ba, câu chốt, sai người đọc) phải tự đọc.

Với bài dài, bộ kiểm tra đếm thêm trên cả bài: một khuôn câu lặp từ 3 lần, dấu hai chấm dồn dập,
đoạn nào cũng 1-3 câu, bài đăng chia nhiều mục viết hoa. Câu chốt cuối đoạn thì phải tự đọc.
Các dấu hiệu này cộng điểm cố định, không chia theo độ dài, nên bài dài không "loãng" thành sạch.
"""
import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I bỏ thư mục script khỏi sys.path
import slides as slides_mod  # noqa: E402

PATTERNS = {
    # Hứa làm sau mà không nói ai, khi nào, làm gì
    "hứa suông": [
        r"chi tiết (sẽ được|sẽ) (trao đổi|gửi|cập nhật|trình bày|làm rõ)( thêm)? (sau|trong (thời gian tới|buổi khác))",
        r"sẽ (tiếp tục )?(nghiên cứu|xem xét|cân nhắc|cập nhật|làm rõ) (thêm|sau|trong thời gian tới)",
        r"sẽ được (làm rõ|cập nhật|bổ sung) (sau|trong thời gian tới)",
        r"\bwill (be )?(shared|discussed|clarified|provided) (later|separately|in due course)",
        r"\bdetails to follow\b", r"\bmore details (will follow|later)\b",
    ],
    "lời chatbot": [
        r"chắc chắn rồi", r"tất nhiên rồi", r"câu hỏi (rất )?hay", r"hoàn toàn đúng",
        r"hy vọng (điều này|(những )?thông tin (này|trên)|bài viết)", r"đừng ngần ngại", r"bạn có muốn tôi",
        # lời mời làm tiếp còn sót cuối câu trả lời: "Nếu bạn muốn, mình có thể phân tích sâu hơn"
        r"nếu bạn muốn,? (mình|tôi|em) có thể (phân tích|viết|soạn|tóm tắt|gợi ý|giúp|mở rộng|đi sâu|liệt kê|chỉnh|làm thêm)",
        r"dưới đây là", r"\bcertainly!", r"\bof course!", r"great question",
        r"you'?re absolutely right", r"i hope this helps", r"let me know if",
        r"as an ai language model", r"here is an? ",
    ],
    "câu dẫn": [
        # Khen trước rồi mới nói: "Điều điên rồ nhất là:", "Đây là điểm mình thấy ấn tượng nhất", "Kết quả ấn tượng:"
        r"(điều|điểm|cái|thứ) [^.!?\n:]{0,30}(ấn tượng|đáng sợ|điên rồ|thú vị|bất ngờ|quan trọng|đáng chú ý) nhất[^.!?\n:]{0,25}(là\b|:)",
        r"kết quả (rất |cực kỳ |vô cùng )?(ấn tượng|bất ngờ|đáng kinh ngạc)\s*:", r"\btin (mình|tôi) đi\b",
        r"đây là toàn bộ\b", r"từ a(-| đến )z\b",
        r"hãy cùng (tìm hiểu|khám phá)", r"nói thẳng ra", r"thành thật mà nói\?",
        r"ít ai (biết|dám nói)", r"không ai nói", r"let'?s dive in", r"here'?s the thing",
        r"here'?s what you need to know", r"without further ado",
    ],
    # "Nói gọn", "Nói cho thật:", "Nói rõ để...:": báo trước mình sắp nói kiểu gì thay vì nói luôn.
    "nhãn báo giọng": [
        r"(^\W*|[.!?…]\s+)(mình |tôi |em |anh |chị |xin |phải |cứ )?nói (cho )?(thật|thẳng|gọn|rõ|ngắn gọn|"
        r"đơn giản|nhanh|trắng ra|công bằng|thật lòng|thẳng thắn|chính xác|đúng ra)( ra| thì| là| luôn| nhé)?\s*[:,]",
        r"(^\W*|[.!?…]\s+)nói (cho )?(thật|thẳng|gọn|rõ|công bằng) (để|cho|trước)\b[^.!?\n:]{0,50}:",
        r",\s*nói (gọn|nhanh|thật|thẳng|ngắn gọn|đơn giản)\s*$",
        r"(thành thật|thật lòng|công bằng|thẳng thắn|thú thật|nghiêm túc) mà nói",
        r"(điều )?(mình|tôi|em) (chỉ )?muốn nói( là)?\s*:", r"(^\W*|[.!?…]\s+)(thú thật|nói thật)( là)?\s*[,:]",
        r"(hiểu|nói|giải thích) (một cách )?(đơn giản|nôm na|ngắn gọn|dễ hiểu)( nhất)?( là\b| thì\b|\s*[:,])",
        r"cứ hiểu (nó |đơn giản )?(như|là)\b",
        r"(^\W*|[.!?]\s+)(to be (honest|fair|clear)|let'?s be (honest|real|clear)|honestly|frankly|"
        r"simply put|put simply|long story short)\s*[,:]",
    ],
    "đối lập giả": [
        r"không (chỉ|đơn thuần|phải)\b.{0,80}?\bmà (còn|là)", r"chứ không(?! thì)\b",
        # "Câu hỏi không còn là X mà là Y"; "giá trị không nằm ở X, mà nằm ở Y"; "Không phải vì X." mở câu
        r"không (còn |chỉ )?(là|ở|nằm ở)\b[^.!?\n]{1,90}?\bmà (là|ở|nằm ở)\b",
        r"(^\W*|[.!?…]\s+)không phải (vì|để)\b[^.!?\n]{1,80}[.!?]",
        # "không X, mà Y"; tách hai câu "Mình không cần X. Mình cần Y."
        # Không bắt đuôi ", không phải Y" vì trùng với "không phải" nghĩa là "khỏi phải".
        r"không (?!chỉ\b|đơn thuần\b|phải\b)[^.!?\n,;:]{1,60}, mà (?!còn\b)",
        r"không (?!phải\b|có\b|được\b|thể\b|biết\b)(\w+)\b[^.!?\n]{0,60}[.!?]\s+(?:\w+\s+){1,3}\1\b",
        # "X không chỉ là A. Nó là B."; "X là A, không phải B" (bỏ "không phải" nghĩa là "khỏi phải")
        r"không (chỉ|đơn thuần) (là )?[^.!?\n]{1,80}[.!?]\s+(nó|đây|đó)\b",
        r"\blà [^.!?\n,]{1,40}, không phải (là )?(?!làm|gõ|cài|cấu hình|chờ|lo|trả|đi|mua|sửa|viết|đợi|nghĩ|hỏi|tốn|mất|ai|lúc|khi)\w",
        # "PM không phải là A. PM là B."; "không có nghĩa là A, mà là B"; "Đừng A, hãy B"; "Không có A, chỉ có B"
        r"(\w+) không phải (là )?[^.!?\n]{1,60}[.!?]\s+\1 là\b", r"không có nghĩa là\b[^.!?\n]{0,60}?\bmà là\b",
        r"(^|[.!?*]\s*)đừng [^.!?\n,]{1,40}, hãy\b", r"\bkhông có [^.!?\n,]{1,40}, chỉ có\b",
        # "Không ồn ào, không chạy theo trend, chỉ kể một câu chuyện": hai lần phủ định dọn đường cho vế chốt
        r"(^|[.!?]\s+)không [^.,!?\n]{2,30}, không [^.,!?\n]{2,30}(, (chỉ|nhưng|vậy mà)\b|\.\s+(chỉ|nhưng|vậy mà)\b)",
        r"\bnot (just|only|merely)\b.{0,80}?\bbut\b", r"\bit'?s not\b.{0,60}?\bit'?s\b",
    ],
    # Câu kết mời bình luận, mời theo dõi: khuôn của bài mạng xã hội viết để kéo tương tác.
    "mời tương tác": [
        r"(chia sẻ|để lại|comment|bình luận|kể)\b[^.!?\n]{0,50}(bình luận|comment|cmt|bên dưới|phía dưới)",
        r"\bbạn (nghĩ sao|thấy sao|thì sao)\b", r"\bcòn bạn\??\s*$", r"(^|[.!?]\s+)còn bạn,[^.!?\n]{0,80}\?",
        r"nếu bạn (cũng )?(đang|từng)[^.!?\n]{0,80}(nhắn|inbox|kể|chia sẻ)",
        # bài kể chuyện mình rồi cuối bài quay sang khuyên người đọc: "Nếu bạn đang ở ngã rẽ tương tự, hãy..."
        r"nếu bạn (cũng )?(đang|từng|còn)[^.!?\n]{0,90}(?<!nhắn)(?<!kể)[,:]? (hãy|cứ|đừng|thì)\b(?! (nhắn|inbox|kể|chia sẻ))",
        r"\bai [^.!?\n]{2,50}?(chia sẻ|cho (mình|em|tớ) xin (thêm )?(kinh nghiệm|ý kiến|cảm nhận|review)|mách (mình|em))[^.!?\n]{0,40}(nhé|nha|với)\b\s*([.!?]|$)",
        r"(^|[.!?]\s+)ai (đang|có|sắp|định|muốn|còn) [^.!?\n]{3,70} thì (cứ|hãy|đừng|nhớ)\b",
        r"bạn đã (từng|bao giờ) [^.!?\n]{1,50} chưa\?", r"kể (cho )?(mình|tôi) nghe", r"hãy (tiếp tục )?(theo dõi|đồng hành cùng)",
        r"điều gì (bạn|anh chị)[^.!?\n]{0,50}\?\s*$", r"(tag|gắn thẻ) (ngay )?(một )?(người|ai đó|bạn bè)",
        r"(follow|theo dõi) (mình|tôi|page|trang)[^.!?\n]{0,20} để", r"\bwhat do you think\?",
        r"\b(let me know|share your thoughts|drop a comment)[^.!?\n]{0,30}(comments|below)", r"\bagree\?\s*$",
    ],
    # Châm ngôn truyền cảm hứng và lời tri ân theo khuôn: gắn vào bài nào cũng được.
    "khẩu hiệu": [
        r"tương lai thuộc về", r"chỉ là (sự |bước )?khởi đầu", r"chưa bao giờ (là )?(dễ dàng|muộn)",
        r"bắt đầu từ những bước (nhỏ|đầu tiên)", r"mọi (điều|thứ) đều có thể", r"bạn sẽ (phải )?ngạc nhiên",
        r"(bắt đầu|hành động|thử|đăng ký|ra khỏi nhà) ngay hôm nay", r"thay vì (lo sợ|sợ hãi|chờ đợi)",
        r"phía trước còn (rất )?nhiều (thách thức|khó khăn)", r"vững bước", r"chặng đường (phía trước|sắp tới)",
        r"cột mốc (quan trọng|đáng nhớ)", r"nỗ lực không ngừng", r"không ngừng (học hỏi|nỗ lực|phát triển|đổi mới|hoàn thiện)",
        r"lòng biết ơn sâu sắc", r"biến (tầm nhìn|ước mơ|ý tưởng) thành hiện thực", r"tạo ra giá trị( thực| thật)?",
        r"thay đổi mọi thứ", r"phải thừa nhận rằng", r"(làm việc|nỗ lực|cống hiến) không (biết )?mệt mỏi",
        r"(bước )?ra khỏi vùng an toàn", r"phiên bản tốt (hơn|nhất) của", r"bài học (quý|lớn|đắt)( giá)? nhất",
        r"câu trả lời (ngắn gọn )?(là|không đơn giản)", r"không hề dễ dàng", r"siêu năng lực",
        r"(hành trình|chặng đường|con đường) phía trước còn (dài|nhiều)", r"(điều|thứ) gì đó có ý nghĩa",
        r"ước gì (mình |tôi )?(được )?biết sớm hơn", r"đây là câu chuyện của (mình|tôi)", r"không (bao giờ là|phải là) quá muộn",
        r"đằng sau (mỗi|những|từng) [^.!?\n]{2,40} là\b", r"(hãy|nên) (luôn )?nhớ rằng",
        r"không hứa [^.!?\n]{3,60}, nhưng [^.!?\n]{0,15}hứa",
        r"tin (tưởng )?vào tầm nhìn", r"\bthe future belongs to\b", r"\bthis is just the beginning\b",
    ],
    # Câu công văn dùng trong email, tin nhắn thường ngày
    "khuôn công văn": [
        r"rất mong nhận được sự", r"xin (được )?trình bày( chi tiết)? như sau", r"tiềm ẩn (nhiều )?(rủi ro|nguy cơ)",
        r"(?<!rất mong )nhận được sự (quan tâm|xem xét|ủng hộ|phê duyệt)", r"kính mong (anh|chị|quý)[^.!?\n]{0,30}(xem xét|tạo điều kiện)",
    ],
    # Nêu sự việc xong lại giải nghĩa hộ người đọc.
    "diễn giải lại": [
        r"(^\W*|[.!?…]\s+)(tức là|nghĩa là|có nghĩa là|điều đó có nghĩa là|(hay )?nói (một )?cách khác|"
        r"nói đơn giản hơn)\b",
        r"\bin other words\b", r"\bwhich means\b",
    ],
    "tự kể dàn ý": [
        r"bài (viết )?này (mình |tôi |em |chúng tôi )?(viết để|sẽ (nói|kể|chia sẻ|trình bày|đi qua|giải thích|"
        r"điểm qua)|gồm \w+ phần|chia (làm|thành))",
        r"trong bài (viết )?này,? (mình|tôi|em|chúng ta|chúng tôi) sẽ", r"cuối bài (có|là) phần",
        r"\bin this (post|article),? (i|we)( will|'ll)\b",
    ],
    "tổng kết rỗng": [
        r"^\s*(tóm lại|nhìn chung|nói tóm lại|kết luận lại)", r"\bin conclusion\b",
        r"\bto sum up\b", r"\bin summary\b",
    ],
    # Giọng giật tít của bài tin công nghệ: chuyện gì cũng là bom, là quái vật, là cú sốc.
    "giật gân": [
        r"thả bom", r"quả bom", r"cú sốc", r"(con |quái )quái vật", r"\bquái vật (ai|mới)", r"phá đảo", r"cực khủng",
        r"điên rồ", r"đập nát", r"cú vả", r"càn quét", r"thả xích", r"khai tử", r"hất cẳng", r"cướp việc",
        r"bỏ lại phía sau", r"tiến hóa hay là chết", r"đáng gờm", r"gây bão", r"làm mưa làm gió",
        r"thay đổi cuộc chơi", r"luật chơi[^.!?\n]{0,30}thay đổi", r"định (nghĩa|hình) lại", r"bước (đi|tiến) đột phá",
        r"san bằng", r"gõ cửa", r"trong nguy (luôn )?có cơ", r"cưỡi (lên )?(lưng )?(làn )?sóng", r"đáng sợ nhất", r"sự thật tàn khốc", r"chuẩn bị tinh thần chưa",
    ],
    # Mỗi ý kèm một ví von dắt tay người đọc: "Giống quán ăn: ...", "Giống đánh cờ, ...".
    "ví von dắt tay": [
        r"(^\W*|[.!?…]\s+)(cũng )?(giống|giống như|hãy tưởng tượng|tưởng tượng|ví như)\b[^.!?\n:,]{2,50}[:,]",
    ],
    # Câu hỏi thả ra để tự trả lời ngay sau đó, hay gặp ở đầu mục của bài kéo tương tác.
    "câu hỏi mồi": [
        r"(^\W*|[.!?…]\s+)nghe (thì |có vẻ )?(vô lý|khó tin|hấp dẫn|quen không|điên rồ)\s*\?",
        r"\blà (cái )?(quái )?gì mà\b[^.!?\n]{0,80}\?", r"(^\W*|[.!?…]\s+)khoan đã\b",
        r"điều gì sẽ xảy ra\b[^.!?\n]{0,80}\?", r"lựa chọn của bạn là gì\s*\?",
        r"(^\W*|[.!?…]\s+)(và )?(kết quả|vấn đề|điểm yếu|cái giá)( thì sao| là gì| ở đâu)\s*\?",
        r"(^\W*|[.!?…]\s+)(hãy )?thử nghĩ xem\b",
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
        # đo trên tin người viết trước 7/2022 và tin máy viết lại (xem CHANGELOG 2.11.0)
        r"tầm nhìn chiến lược", r"góp (một )?phần không nhỏ", r"\bbước tiến\b", r"mang trong mình",
        r"bài học quý (giá|báu)", r"(^|[.!?]\s+)\s*thêm vào đó,",
    ],
    "văn dịch (vi)": [
        r"\b(được|bị)\b[^.!?\n]{1,60}?\bbởi\b", r"mở khóa tiềm năng", r"điều hướng (sự|những) phức tạp",
        r"tác động có ý nghĩa", r"(ở|tại) (cấp độ )?cốt lõi", r"trải nghiệm liền mạch",
        r"tận dụng (sức mạnh|khả năng|tối đa)", r"khi nói đến", r"là một trong những\b.{0,40}?\bnhất",
        r"đây là lý do (tại sao|vì sao)", r"có (một số|nhiều) cách để", r"được biết đến (như|là)",
        r"với sự (hỗ trợ|giúp đỡ) của",
        # kết hợp từ dịch sát từ thành ngữ tiếng Anh
        r"ở cuối ngày", r"tin (tốt|vui|xấu) là", r"không có gì (đáng )?ngạc nhiên khi",
        r"(làm|tạo) (nên|ra) sự khác biệt", r"chơi (một )?vai trò", r"đóng một vai trò",
        r"(có|lấy|mang lại) (một )?cái nhìn (sâu sắc|tổng quan|rõ ràng)", r"(tốt|đúng|chính xác) hơn (may rủi|ngẫu nhiên)",
        r"là (rất |vô cùng )?(quan trọng|cần thiết|hữu ích) (để|rằng)\b", r"bạn có thể (sẽ )?(muốn|cần phải)",
        r"hãy chắc chắn (rằng|để)", r"(?<!hãy )(đảm bảo|chắc chắn) rằng bạn", r"cảm thấy tự do", r"đừng ngần ngại",
        r"như đã (đề cập|nói|nêu) (ở trên|trước đó)", r"một loạt các", r"theo (một )?cách mà",
        r"(bạn )?đã đến đúng nơi", r"đầu tiên và (quan trọng nhất|trước hết)", r"(như|theo) một (quy tắc|nguyên tắc) chung",
        r"cuối cùng nhưng không (kém|phải là ít) (phần )?quan trọng", r"kẻ thù (lớn nhất|tồi tệ nhất) của (bạn|chúng ta)",
        # khuôn email, mô tả sản phẩm, tài liệu hướng dẫn dịch thẳng
        r"hy vọng (email|thư|tin nhắn) này (tìm thấy|đến với)", r"vui lòng tìm (thấy )?(tệp|file|tài liệu) đính kèm",
        r"mong (chờ |đợi )?(được )?nghe (tin )?từ", r"để theo dõi (về|lại) (cuộc họp|buổi họp|email|thư)",
        r"(bất kỳ|bất cứ) câu hỏi (hoặc|hay) (mối quan tâm|thắc mắc)", r"với (bạn|khách hàng|người dùng) trong tâm trí",
        r"cho dù bạn là", r"sự lựa chọn hoàn hảo", r"nhận được nhiều hơn từ", r"vẫn còn tồn tại",
        r"bạn (sẽ )?không muốn (bỏ lỡ|mất)",
        r"viết (thư|email|mail) này (để|nhằm)", r"xin lỗi vì (sự |bất kỳ sự )(bất tiện|chậm trễ|phiền toái)",
        # khuôn báo cáo và bài giải thích
        r"(làm|đạt) được điều (này|đó) mà không", r"(chúng tôi|tôi) (muốn|xin) gửi lời cảm ơn đặc biệt",
        r"(hào hứng|vui mừng|vui|vinh dự|tự hào) (để|được) chia sẻ rằng",
        r"(?<!được )(?<!bị )\b(dẫn dắt|dẫn đầu|tài trợ|phát triển|xây dựng|thiết kế|tạo ra|thực hiện) bởi\b", r"(hãy )?để lại một bình luận",
        r"tiến về phía trước", r"(đạt được|có) những tiến bộ đáng kể", r"điều đó (được )?nói rằng",
        r"hãy nghĩ về (nó|điều này|chúng) như", r"không phải là không có (những )?(hạn chế|nhược điểm|thách thức|rủi ro)",
        r"(chúng ta|mình) sẽ cùng nhau (xem xét|tìm hiểu|khám phá|đi qua)", r"(đang )?tìm kiếm một cách để",
        # tên phần mềm dịch từng chữ: "AI detector", "scanner", "plagiarism detector". Máy quét tài liệu,
        # máy dò kim loại là đồ thật nên chỉ bắt khi đi với AI, văn bài, hoặc với việc chỉ phần mềm mới làm.
        r"\bmáy (dò|quét|phát hiện)( văn| văn bản| nội dung| bài)? (ai|gpt|chatgpt)\b", r"\bmáy dò (đạo văn|văn|giọng)",
        r"\b(lọt|qua được|qua mặt|vượt qua|lừa|đánh lừa|né|chạy|chạy thử) (các |mọi |những )?máy (dò|quét)\b",
        r"\bmáy (dò|quét) (chấm|bắt được|báo nhầm|báo|đếm|cho điểm|gắn cờ|đánh dấu)\b",
        # "scores 0-100" dịch cụt thành "chấm 0-100", "điểm số 0-100"; người Việt nói "thang điểm 0-100"
        r"(?<!thang )\b(chấm|chấm điểm|cho điểm) (số )?[01] ?[-–] ?(5|10|100)\b(?! ?(điểm|sao))",
        r"(?<!thang )(?<!chấm )(?<!cho )\bđiểm (số )?[01] ?[-–] ?(5|10|100)\b(?! ?điểm)",
    ],
    "bị động dịch sát": [
        r"\b((sẽ|đã|đang|cần|phải|nên|có thể) )?được (giữ nguyên|cập nhật|cài đặt|thiết kế|xây dựng|phát triển|tạo ra|"
        r"sử dụng|thực hiện|triển khai|cung cấp|áp dụng|đánh giá|xem là|coi là|coi như|lưu trữ|tối ưu|tích hợp|"
        r"quản lý|xử lý|xác định|lập trình|đề cập|thiết lập|cấu hình|ghi nhận|trình bày|mô tả|liệt kê|đặt tên|biết đến)\b(?! bởi)",
    ],
    "vật làm chủ ngữ": [
        r"\b(bảng|hình|biểu đồ|sơ đồ|kết quả|điểm số|số liệu|dữ liệu|con số|báo cáo|bài viết|tài liệu|công cụ|"
        r"tính năng|hệ thống|giải pháp|nền tảng|ứng dụng|skill)( \w+){0,3}? "
        r"(cho phép|giúp bạn|giúp người dùng|mang lại|mang đến|đảm bảo rằng|cho thấy rằng|chỉ ra rằng)",
    ],
    "mở câu dịch sát": [
        r"(?:^|(?<=[.!?:] ))(để [^.!?\n,]{3,60}, (bạn|chúng ta|chúng tôi|hãy)\b|bằng cách \w+|"
        r"với (sự|việc|những|các|một) \w+|đối với \w+|dựa trên \w+|thông qua \w+)",
    ],
    "quan hệ từ dịch sát": [
        r"\b(nơi|người|những người|điều|thứ|lý do|thời điểm) mà\b(?! (không|chưa|vẫn|chẳng|cũng|còn|lại)\b)", r"\bmà (tập trung vào|cho phép|giúp)\b", r"\bcàng nhiều [^.,!?\n]{1,30} mà\b", r"\blà một trong (những|các)\b",
        r"\bcũng như là\b", r"\bvà cũng\b", r"\bvà/hoặc\b",
    ],
    "động từ rỗng (vi)": [
        r"tiến hành (thực hiện|việc)?", r"thực hiện việc", r"nhằm mục đích",
        r"(đưa ra|cung cấp) sự (hỗ trợ|giúp đỡ)", r"hiện thực hóa", r"đóng góp vào",
    ],
    "danh hóa (vi)": [
        r"một cách (?!(gọi|khác|nữa|làm|để|viết|nói|hiểu|nhìn|đơn giản là)\b)\w+", r"trở nên \w+", r"có khả năng \w+", r"\btrong việc (cải thiện|nâng cao|xây dựng|phát triển|giúp|tạo|đảm bảo|thúc đẩy|giải quyết|quản lý)\b",
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
        r"nằm giữa lòng", r"(góc|chốn|khoảng|ốc đảo|không gian)[^.,\n]{0,25} giữa lòng",
        r"vị trí đắc địa", r"ngỡ ngàng", r"không thể bỏ qua", r"đẳng cấp",
        r"điểm (dừng chân|đến|hẹn) (lý tưởng|hấp dẫn)", r"đắm mình", r"nhịp sống (vội vã|hối hả)", r"đậm chất", r"mộng mơ",
        r"trải nghiệm (trọn vẹn|khó quên|tuyệt vời|đáng nhớ)", r"khoảng lặng",
        r"thiên đường (nghỉ dưỡng|mua sắm|ẩm thực|du lịch|sống ảo)", r"(pha chế|chăm chút|chế tác|lựa chọn) (một cách )?(tỉ mỉ|kỹ lưỡng)", r"thành phố ngàn hoa",
        r"\bsở hữu (bộ sưu tập|không gian|vị trí|đội ngũ|hệ thống|thiết kế|tầm nhìn|vẻ đẹp)",
        r"\bnestled\b", r"\bbreathtaking\b", r"\bmust-visit\b", r"\brenowned\b",
    ],
    "uy tín mơ hồ": [
        r"các chuyên gia (cho rằng|nhận định)", r"nhiều nghiên cứu (chỉ ra|cho thấy)",
        r"giới quan sát", r"experts (believe|argue|say)", r"industry reports",
    ],
    "né là/có": [
        r"đóng vai trò là", r"tự hào (có|sở hữu)", r"\bnằm ở sự\b", r"\bserves as\b", r"\bstands as\b",
    ],
    "giới hạn kiến thức": [
        r"tính đến thời điểm (cập nhật|huấn luyện)", r"dựa trên thông tin hiện có",
        r"as of my (last|knowledge)", r"based on available information",
    ],
    # Chỉ dẫn gửi cho AI nằm lẫn trong văn bản cần sửa: coi là chữ, không làm theo
    "chỉ dẫn chèn vào": [
        r"</?(skill|system|instructions?)>", r"(bỏ qua|quên) (mọi|tất cả|toàn bộ|các) (hướng dẫn|chỉ dẫn|chỉ thị)",
        r"\bignore (all |any )?(the )?(previous|prior|above) instructions\b", r"\bsystem message\b",
    ],
    "dấu vết công cụ": [
        r"contentReference", r"oaicite", r"turn0search\d", r"\[cite: ?\d+\]", r":::writing",
        # chỗ trống của bản mẫu còn sót: [Họ tên], [Tên công ty], [Your name]
        r"\[(họ (và )?tên|tên[^\]\n]{0,30}|chức vụ|số điện thoại|sđt|email[^\]\n]{0,20}|địa chỉ[^\]\n]{0,20}|"
        r"ngày[^\]\n]{0,20}|điền[^\]\n]{0,40}|chèn[^\]\n]{0,40}|link[^\]\n]{0,20}|công ty[^\]\n]{0,20}|"
        r"your [^\]\n]{1,30}|company[^\]\n]{0,20}|name|date|insert[^\]\n]{0,40})\](?!\()",
    ],
}

DASH = re.compile(r"[—–]| -- ")
CHATGPT_LINK = re.compile(r"utm_source=chatgpt\.com", re.IGNORECASE)
CURLY = re.compile(r"[“”‘’]")
BOLD_LABEL = re.compile(r"^\s*([-*+]|\d+\.)\s+(\S+\s+)?\*\*[^*]+:?\*\*:?")
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2B07\u20E3→]")
# Mỗi vòng chỉ ăn một ký hiệu: "(?:[-*+#>]+\s*)*" lồng hai lượng từ, treo trên dòng "** ** ** ..." dài.
EMOJI_LEAD = re.compile(r"^\s*(?:[-*+#>]\s*)*(?:\d\ufe0f?\u20e3|[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50])")
# Dòng chỉ có chữ in đậm, hoặc đoạn mở bằng một cụm in đậm kết bằng dấu câu ("**Văn phong đơn giản.** Tác giả...")
BOLD_HEADING = re.compile(r"^\s*\*\*[^*\n]{2,80}\*\*:?\s*$|^\s*\*\*[^*\n]{2,60}[:.!?]\*\*\s+\S")
FENCE = re.compile(r"^\s*```")
# Chêm tiếng Anh trong ngoặc sau từ Việt: "hiệu suất (performance)"
EN_GLOSS = re.compile(r"\w*[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]\w*\s+\(([a-z][a-z ]{2,30})\)")
VI_LETTER = re.compile(r"[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
NOMINAL = re.compile(r"\b(việc|sự)\b")
THIS_IT = re.compile(r"^(điều này|điều đó|nó)\b")


OFFICIAL = re.compile(r"(?im)^\s*(số:\s*\d+\s*/|v/v\b|kính gửi:)")
QUOTED_LINE = re.compile(r"^\s*[>|]")
QUOTED_SPAN = re.compile(r'"[^"\n]*"|“[^”\n]*”')


def strip_quoted(text):
    """Bỏ phần trích dẫn (dòng '>', dòng bảng, chữ trong ngoặc kép), giữ nguyên số dòng.

    Dùng cho văn bản bàn về dấu hiệu văn AI: ví dụ được trích không tính là lỗi của bài.
    """
    out, in_code = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_code = not in_code
            out.append(line)
        elif in_code:
            out.append(line)
        elif QUOTED_LINE.match(line):
            out.append("")
        else:
            # giữ số chữ để các phép đếm độ dài câu không lệch
            out.append(QUOTED_SPAN.sub(lambda m: '"' + " ".join("_" * len(m.group(0).split())) + '"', line))
    return "\n".join(out)


def scan(text, doc=True, meta=False):
    """doc=False bỏ các kiểm cả bài (dùng cho slide). meta=True bỏ qua phần trích dẫn."""
    if meta:
        text = strip_quoted(text)
    hits = {}
    in_code = False
    lines = text.splitlines()
    for no, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Link chép từ câu trả lời ChatGPT còn đuôi ?utm_source=chatgpt.com. Xét trước khi bỏ URL.
        for m in CHATGPT_LINK.finditer(re.sub(r"`[^`]*`", "", line)):
            hits.setdefault("dấu vết công cụ", []).append((no, m.group(0)))
        prose = re.sub(r"`[^`]*`|https?://\S+", "", line)
        low = prose.lower()
        vietnamese = len(VI_LETTER.findall(low)) >= 3
        for group, pats in PATTERNS.items():
            # Danh sách từ tiếng Anh dành cho văn tiếng Anh; trong câu tiếng Việt, "highlight", "robust" là thuật ngữ
            if vietnamese and group == "từ vựng AI (en)":
                continue
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
        elif BOLD_HEADING.match(prose):
            hits.setdefault("in đậm làm tiêu đề", []).append((no, prose.strip()[:40]))
        if EMOJI_LEAD.match(prose) and len(prose.split()) >= 3:
            hits.setdefault("emoji đầu dòng", []).append((no, prose.strip()[:40]))
        for m in EN_GLOSS.finditer(low):
            if prose[m.start(1):m.end(1)].islower():  # bỏ qua viết tắt như (MIT), (API)
                hits.setdefault("chêm tiếng Anh", []).append((no, m.group(0)))
        sentence_checks(prose, no, hits)
    if OFFICIAL.search(text):  # công văn thật thì câu công văn là đúng chỗ
        hits.pop("khuôn công văn", None)
    # Một dòng chúc mừng mở bằng emoji hay một nhãn in đậm lẻ thì chưa phải khuôn
    for group in ("emoji đầu dòng", "in đậm làm tiêu đề"):
        if len(hits.get(group, [])) < 2:
            hits.pop(group, None)
    if doc:
        document_checks(text, hits)
    return hits, len(lines)


STACCATO = re.compile(r"(?:(?:^|(?<=[.!?])\s+)(?:[^\s.!?]+\s+){0,3}[^\s.!?]+\.(?=\s|$)){3,}")


def sentence_checks(prose, no, hits):
    if not LIST_ITEM.match(prose):
        for m in STACCATO.finditer(prose):
            hits.setdefault("chuỗi câu cụt", []).append((no, m.group(0).strip()[:50]))
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
        if len(words) >= 60 and not QUOTED_LINE.match(prose):
            hits.setdefault("câu quá dài", []).append((no, f"{len(words)} chữ: {sent[:40]}"))
    # Ba câu liền nhau trở lên, mỗi câu 20 chữ trở lên, chênh nhau không quá 4 chữ
    run = 1
    for a, b in zip(lengths, lengths[1:]):
        run = run + 1 if a >= 20 and b >= 20 and abs(a - b) <= 4 else 1
        if run == 3:
            hits.setdefault("câu dài đều nhau", []).append((no, f"{lengths}"))


TIC_GROUPS = ("đối lập giả", "nhãn báo giọng", "diễn giải lại", "ví von dắt tay")
CLOSING_LABEL = re.compile(r"^(kết|kết luận|lời kết|kết bài|tóm lại|tổng kết|lời cuối)$")
HASHTAG = re.compile(r"(?:^|\s)#[^\W\d_]\w+")
LIST_ITEM = re.compile(r"^\s*([-*+>|]|\d+[.)])\s?")
# Hai chấm dẫn vào lời thoại hay câu trích ("Bà nói: «...»", ": - Con về rồi à?") là dùng đúng chỗ, không đếm
COLON = re.compile(r"(?<!\d):(?!\s*[\"“«‘'–—-])(\s|$)")


def prose_lines(text):
    """Trả về (số dòng, dòng đã bỏ code và link); dòng trong khối code thành chuỗi rỗng."""
    in_code = False
    for no, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_code = not in_code
            yield no, ""
        elif in_code:
            yield no, ""
        else:
            yield no, re.sub(r"`[^`]*`|https?://\S+", "", line)


PLAIN_LABEL = re.compile(r"^\s*(?:[-*+•]|\d+[.)]|[\U0001F300-\U0001FAFF\u2600-\u27BF])\s*"
                         r"([^\W\d_][^:\n*]{0,40}): (?!https?:)(\S+(?:\s+\S+){5,})")
BARE_LABEL = re.compile(r"^\s*([^\W\d_][^:\n*?!.,]{2,32}): (?!https?:)(\S.*)$")
VI_VOWEL = re.compile(r"[AEIOUYÀ-ỹ]")


SCARE_QUOTE = re.compile(r'["“]([^\W\d_][^"“”\n]{1,22})["”]')


def scare_quotes(line):
    """Từ lóng, từ ví von bọc ngoặc kép cho an toàn ("ăn tiền", "tay ngang"): viết thường, một đến ba chữ."""
    return [m.group(1) for m in SCARE_QUOTE.finditer(line)
            if m.group(1).islower() and 2 <= len(m.group(1).split()) <= 3 and VI_LETTER.search(m.group(1))]


def bare_labels(text):
    """Dòng "Nhãn: câu" không có gạch đầu dòng. Đoạn chat hay phỏng vấn thì tên người nói lặp lại, danh sách nhãn thì không."""
    found = [(no, m.group(1).strip().lower(), len(m.group(2).split()))
             for no, line in prose_lines(text) for m in [BARE_LABEL.match(line)] if m]
    found = [f for f in found if len(f[1].split()) <= 6]
    names = [name for _, name, _ in found]
    if len(set(names)) < len(names):
        return []
    return [no for no, _, n in found if n >= 8]


def shouted(line):
    """Chữ viết hoa cả từ để nhấn giữa câu thường ("NHỎ hơn mà NHANH hơn"), không tính dòng tiêu đề viết hoa hết."""
    letters = [c for c in line if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) * 2 > len(letters):
        return []
    return [t for t in re.findall(r"[^\W\d_]{2,}", line)
            if t.isupper() and any(ord(c) > 127 for c in t) and VI_VOWEL.search(t)]


def is_caps_heading(s):
    letters = [c for c in s if c.isalpha()]
    return len(letters) >= 3 and s == s.upper() and len(s.split()) <= 20 and not s.startswith("#")


def document_checks(text, hits):
    """Dấu hiệu chỉ thấy khi nhìn cả bài, sau khi từng câu đã sạch."""
    for group in TIC_GROUPS:
        n = len(hits.get(group, []))
        if n >= 3:
            hits.setdefault("tật lặp cả bài", []).append((hits[group][0][0], f"{group} x{n}"))
    if len(hits.get("emoji đầu dòng", [])) >= 3:
        hits.setdefault("chia mục bằng emoji", []).append(
            (hits["emoji đầu dòng"][0][0], f"{len(hits['emoji đầu dòng'])} dòng mở bằng emoji"))
    labels = hits.get("nhãn in đậm", []) + hits.get("in đậm làm tiêu đề", [])
    # Từ bốn chỗ, và dày cỡ một chỗ trên 150 chữ: tài liệu dài có vài nhãn in đậm thì không tính
    if len(labels) >= 4 and len(labels) * 150 >= len(text.split()):
        hits.setdefault("in đậm dày", []).append((min(labels)[0], f"{len(labels)} nhãn hoặc tiêu đề in đậm"))
    filled = [no for no, s in prose_lines(text) if s.strip() and len(HASHTAG.findall(s)) < 2]
    tail = set(filled[-3:])
    cta = [h for h in hits.get("mời tương tác", []) if h[0] in tail]
    if cta and len(filled) >= 5:
        hits.setdefault("kết bài mời tương tác", []).append(cta[0])
    paras, cur, start, caps, tagged, total_words, md_heads = [], [], 0, [], False, 0, 0
    for no, line in list(prose_lines(text)) + [(0, "")]:
        s = line.strip()
        total_words += len(s.split())
        if not s:
            if cur:
                paras.append((start, " ".join(cur)))
                cur = []
            continue
        if len(HASHTAG.findall(s)) >= 2:
            tagged = True
            continue
        md_heading = re.match(r"#{1,6}\s+(.*)", s)
        if md_heading or is_caps_heading(s):
            name = re.sub(r"^[\W_]+|[\W_]+$", "", md_heading.group(1) if md_heading else s).lower()
            if CLOSING_LABEL.match(name):
                hits.setdefault("mục kết dán nhãn", []).append((no, s[:40]))
            if not md_heading:
                caps.append(no)
            else:
                md_heads += 1
            continue
        if LIST_ITEM.match(s):
            continue
        if not cur:
            start = no
        cur.append(s)
    loud = [(no, t) for no, line in prose_lines(text) for t in shouted(line)]
    if len(loud) >= 3:
        hits.setdefault("viết hoa để nhấn", []).append((loud[0][0], f"{len(loud)} chữ: " + ", ".join(t for _, t in loud[:5])))
    plain = [no for no, line in prose_lines(text) if PLAIN_LABEL.match(line)]
    plain = plain if len(plain) >= 3 else bare_labels(text)
    scare = [(no, q) for no, line in prose_lines(text) for q in scare_quotes(line)]
    if len(scare) >= 5 and len(scare) * 200 >= len(text.split()):
        hits.setdefault("ngoặc kép rào đón", []).append((scare[0][0], f"{len(scare)} chỗ: " + ", ".join(q for _, q in scare[:5])))
    if len(plain) >= 3:
        hits.setdefault("gạch đầu dòng có nhãn", []).append((plain[0], f"{len(plain)} dòng kiểu \"Nhãn: câu\""))
    if len(caps) >= 4:
        hits.setdefault("bài đăng chia mục viết hoa", []).append((caps[0], f"{len(caps)} mục"))
    if tagged and total_words > 800:
        hits.setdefault("bài mạng xã hội dài", []).append((1, f"{total_words} chữ"))
    counts, sents_all, colons, short, dense = [], 0, 0, 0, 0
    for _, para in paras:
        sents = [x for x in SENT_SPLIT.split(para) if len(x.split()) >= 2]
        if not sents:
            continue
        counts.append(len(sents))
        sents_all += len(sents)
        # Dấu hai chấm cuối đoạn dẫn vào danh sách, khối lệnh, bảng, trích dẫn: dùng đúng chỗ
        lead_in = para.rstrip(" *_").endswith(":")
        body = sents[:-1] if lead_in else sents
        colons += sum(1 for x in body if COLON.search(x))
        short += sum(1 for x in body if len(x.split()) <= 10)
        dense += len(body)
    first = paras[0][0] if paras else 1
    # Đại từ dịch từ "you/we/your": tiếng Việt thường lược chủ ngữ và sở hữu khi đã rõ
    low_all = " ".join(p for _, p in paras).lower()
    pron = len(re.findall(r"\b(bạn|chúng tôi|chúng ta)\b", low_all))
    para_words = len(low_all.split())
    if pron >= 12 and pron * 1000 / max(para_words, 1) >= 12:
        hits.setdefault("đại từ dày", []).append(
            (first, f"{pron} lần \"bạn\"/\"chúng tôi\"/\"chúng ta\" trong {para_words} chữ"))
    # Chữ đệm của văn dịch: tiếng Anh buộc có mạo từ, số nhiều, thì, bị động, sở hữu, còn tiếng Việt
    # thì lược được. Đo trên bộ thử 10 đoạn dịch / 10 đoạn giọng người cùng nội dung: đoạn dịch
    # 120-188 trên 1.000 chữ, đoạn người viết 30-90, README 30.
    filler = sum(len(re.findall(p_, low_all)) for p_ in FILLER_WORDS)
    filler += len(re.findall(r"\bcủa (bạn|tôi|chúng tôi|chúng ta|họ|anh ấy|cô ấy|nó)\b", low_all))
    if para_words >= 60 and filler * 1000 / para_words >= 110:
        hits.setdefault("chữ đệm dịch dày", []).append(
            (first, f"{round(filler * 1000 / para_words)} chữ đệm trên 1.000 chữ (một, các, những, được, có thể, sẽ, đã, của bạn...)"))
    if sents_all >= 20 and colons >= 6 and colons / sents_all >= 0.15:
        hits.setdefault("hai chấm dồn dập", []).append((first, f"{colons}/{sents_all} câu có dấu hai chấm"))
    # Dấu chấm chặt ý thành câu vụn: từ 30% số câu chỉ dài tối đa 10 chữ (không tính câu dẫn
    # vào danh sách hay khối lệnh). Ngưỡng sát: bản README bị chê vụn là 32%, bản đã sửa 28%.
    if dense >= 20 and short / dense >= 0.3:
        hits.setdefault("câu vụn", []).append((first, f"{short}/{dense} câu dài không quá 10 chữ"))
    # Tài liệu có tiêu đề Markdown (README, hướng dẫn) vốn nhiều đoạn dẫn ngắn, không tính
    if md_heads < 3 and len(counts) >= 12 and max(counts) <= 4 and sum(1 for c in counts if c <= 3) / len(counts) >= 0.9:
        few = sum(1 for c in counts if c <= 3)
        hits.setdefault("đoạn ngắn đều nhau", []).append(
            (first, f"{few}/{len(counts)} đoạn chỉ 1-3 câu, không đoạn nào quá 4 câu"))
    voice_checks(text, hits)


# Tiếng lóng đang thịnh hoặc vừa hết thịnh. Người thật mỗi tin thường chỉ một chữ, bản giả thì dồn
# ba bốn chữ vào một tin. Viết tắt quen tay ("ko", "đc", "j") là thói quen thật, không tính.
SLANG = re.compile(
    r"\b(u là trời|đỉnh nóc( kịch trần)?|đỉnh của chóp|slay|keo (lỳ|lì)|gét gô|xu cà na|ét o ét|chằm zn|"
    r"khum|khét lẹt|báo thủ|ối dồi ôi|xỉu up xỉu down|hết nước chấm|tới công chuyện|flex|chill|mlem|"
    r"ủa alo|dảk dảk|bủh bủh|mãi đỉnh|quá xá xịn|xịn xò|cháy quá|pick me|red flag|green flag)\b")
# Dấu hiệu giọng từng vùng hay gặp trong tin nhắn. Chỉ lấy chữ ít khi gặp ngoài vùng đó.
REGIONS = {
    "Bắc": re.compile(r"\b(giời (ơi|ạ)|nhể|chứ lị|thế cơ|nhá)\b"),
    "Trung": re.compile(r"\b(rứa|chừ|hỉ|(đi|ở|chỗ|bên) mô|(làm|nói) răng|răng (rứa|ri|hè)|(bữa|chỗ|cái) ni)\b"),
    "Nam": re.compile(r"\b(nghen|nhen|dìa|hổng|hông|dzậy|bển|ổng)\b"),
}


def voice_checks(text, hits):
    """Ngữ điệu bắt chước sai: chồng tiếng lóng, trộn dấu hiệu của nhiều vùng."""
    lines = [(no, s.lower()) for no, s in prose_lines(text) if s.strip()]
    low = " ".join(s for _, s in lines)
    total = len(low.split())
    found = [(no, m.group(0)) for no, s in lines for m in SLANG.finditer(s)]
    distinct = {m for _, m in found}
    if len(distinct) >= 3 and len(found) * 25 >= total:
        hits.setdefault("chồng tiếng lóng", []).append(
            (found[0][0], f"{len(found)} chữ lóng trong {total} chữ: {', '.join(sorted(distinct))}"))
    regions = {}
    for name, rx in REGIONS.items():
        for no, s in lines:
            regions.setdefault(name, []).extend((no, m.group(0)) for m in rx.finditer(s))
    present = {k: v for k, v in regions.items() if v}
    if len(present) >= 2 and sum(len(v) for v in present.values()) >= 3:
        first = min(v[0][0] for v in present.values())
        detail = "; ".join(f"{k}: {', '.join(m for _, m in v)}" for k, v in present.items())
        hits.setdefault("trộn giọng miền", []).append((first, detail))


FIRST_PERSON = re.compile(r"\b(mình|tôi|tụi mình|bọn mình)\b")
_UNIT = (r"(năm|tháng|tuần|ngày|giờ|tiếng|phút|km|mét|kg|công ty|người|lần|buổi|triệu|tỷ|nghìn|tuổi|cuộc|dự án|khách|"
         r"đêm|trang|cuốn)")
PERSONAL_DETAIL = re.compile(
    rf"\b\d+(?:[.,]\d+)?\s?(?:{_UNIT}\b|%)|\b(?:tháng|năm|tuần|ngày|lần|km|lớp) thứ \w+|\blớp \d+|\b\d{{1,2}}h\d{{0,2}}\b|"
    rf"\b(?:hai|ba|bốn|sáu|bảy|tám|chín|mười) {_UNIT}\b|\bnăm (?:năm|tuần|lần|buổi|công ty|người)\b")
# Lời người khác nói, trích trong ngoặc kép: đứng sau động từ nói, hoặc là một câu hỏi, câu cảm.
QUOTED_SPEECH = re.compile(
    r'\b(?:nói|bảo|dặn|hỏi|la|hét|kể|cười|nhắn|đáp|trả lời|khuyên|thì thầm|gọi)\b[^."“”\n]{0,25}["“]([^"“”\n]{10,160})["”]|'
    r'["“]([^"“”\n]{10,160}[?!])["”]')


def personal_details(text):
    """Chi tiết riêng trong bài xưng "mình", "tôi": máy không biết thật hay bịa, chỉ liệt kê để hỏi lại.

    Bài mô hình viết hộ hay tự thêm đúng loại chi tiết này: con số ("sau 5 năm, 3 công ty", "tháng thứ tư",
    "5h15") và lời người khác nói ('ông chủ quán dặn "qua cầu nhớ chạy chậm"'). Không tính điểm.
    """
    lines = [(no, s) for no, s in prose_lines(text) if s.strip()]
    if len(FIRST_PERSON.findall(" ".join(s for _, s in lines).lower())) < 3:
        return []
    seen, out = set(), []
    for no, s in lines:
        if is_caps_heading(s.strip()) or len(HASHTAG.findall(s)) >= 2:
            continue
        for m in PERSONAL_DETAIL.finditer(s.lower()):
            if m.group(0) not in seen:
                seen.add(m.group(0))
                out.append((no, m.group(0)))
        for m in QUOTED_SPEECH.finditer(s):
            said = (m.group(1) or m.group(2)).strip()
            out.append((no, 'lời "' + (said if len(said) <= 40 else said[:40].rsplit(" ", 1)[0] + "...") + '"'))
    return out if len(out) >= 2 else []


CHAT_POLITE = re.compile(
    r"^\W*(chào (bạn|anh|chị|em|mọi người|cả nhà)\b|cảm ơn (bạn|anh|chị|em|mọi người)?\s*(đã|vì|rất nhiều vì)\b)|"
    r"(sẽ|xin) (cân nhắc|ghi nhận|tiếp thu)|góp ý (rất )?(hay|quý báu|giá trị)")


def chat_checks(text, hits):
    """Chỉ chạy với --chat: tin nhắn trả lời mà viết như email hay văn bản."""
    lines = [(no, s) for no, s in prose_lines(text) if s.strip()]
    total = sum(len(s.split()) for _, s in lines)
    for no, s in lines:
        if LIST_ITEM.match(s) and not s.lstrip().startswith(">") or re.match(r"\s*#{1,6}\s", s) or "**" in s:
            hits.setdefault("tin nhắn định dạng như văn bản", []).append((no, s.strip()[:40]))
        for sent in SENT_SPLIT.split(s.strip()):
            m = CHAT_POLITE.search(sent.lower())
            if m:
                hits.setdefault("tin nhắn khách sáo", []).append((no, m.group(0).strip()))
    if total > 80:
        hits.setdefault("tin nhắn dài", []).append((lines[0][0] if lines else 1, f"{total} chữ"))


# Tiêu đề slide chỉ là nhãn chủ đề hoặc tả việc đang làm, không nói kết luận.
LABEL_TITLE = re.compile(
    r"^(tổng quan|giới thiệu|bối cảnh|thực trạng|hiện trạng|thách thức|giải pháp|lợi ích|kết luận|"
    r"tóm tắt|tóm lại|phân tích|đánh giá|tổng hợp|định hướng|tầm nhìn|mục tiêu|vấn đề|"
    r"overview|introduction|background|challenges?|solutions?|benefits|conclusions?|summary|"
    r"key takeaways|analysis)\b")
COUNT_TITLE = re.compile(
    r"(^|\s)(\d+|hai|ba|bốn|năm|sáu|bảy) (trụ cột|giải pháp|bước|lý do|điểm|yếu tố|mục tiêu|vấn đề|"
    r"thách thức|lợi ích|xu hướng|chiến lược|nhóm|cách|bài học|nguyên tắc)\b|"
    r"\b(\d+|three|four|five) (pillars|steps|reasons|keys|ways|lessons|principles)\b")
FRAMEWORK = re.compile(r"\b(scr|situation|complication|resolution)\b|(→|->).*(→|->)")
CLOSING_TITLE = re.compile(r"^(cảm ơn|xin cảm ơn|thank you|thanks|q ?& ?a|hỏi đáp)\b")


def words(text):
    return len(text.split())


def slide_checks(deck, index, hits):
    """Kiểm riêng cho slide: tiêu đề, số gạch đầu dòng, độ dày chữ, ghi chú thuyết trình."""
    title_line = {no: line for line, no, kind, _ in index if kind == "tiêu đề"}
    first_line = {}
    for line, no, _, _ in index:
        first_line.setdefault(no, line)
    content = [s for s in deck if s["no"] > 1 and not CLOSING_TITLE.match(s["title"].lower())]
    for s in content:
        title = s["title"].strip().lower()
        line = title_line.get(s["no"], first_line.get(s["no"], 1))
        if title and words(title) <= 6 and not re.search(r"\d", title) and LABEL_TITLE.match(title):
            hits.setdefault("tiêu đề dạng nhãn", []).append((line, s["title"][:50]))
        prefix = re.match(r"^([^:]{2,30}):\s+\S", title)
        if prefix and words(prefix.group(1)) <= 3:
            hits.setdefault("tiêu đề có tiền tố nhãn", []).append((line, s["title"][:50]))
        if COUNT_TITLE.search(title):
            hits.setdefault("tiêu đề đếm số ý", []).append((line, s["title"][:50]))
        if FRAMEWORK.search(title):
            hits.setdefault("lộ tên khung", []).append((line, s["title"][:50]))
        body_words = sum(words(x) for x in s["body"])
        if body_words > 80:
            hits.setdefault("slide nhiều chữ", []).append((line, f"{body_words} chữ"))
    for line, no, kind, text in index:
        if kind == "nội dung" and no > 1 and words(text) > 20:
            hits.setdefault("gạch đầu dòng dài", []).append((line, text[:50]))
        if kind == "ghi chú":
            for sent in SENT_SPLIT.split(text):
                if words(sent) > 30:
                    hits.setdefault("câu khó nói (ghi chú)", []).append((line, sent[:50]))
            if re.search(r"\([^)]{3,}\)", text):
                hits.setdefault("ngoặc trong lời nói", []).append((line, text[:50]))
    # Slide nào cũng đúng 3 (hoặc 4) gạch đầu dòng
    counts = [len(s["body"]) for s in content if len(s["body"]) >= 2]
    if len(counts) >= 4:
        top = max(set(counts), key=counts.count)
        if top in (3, 4) and counts.count(top) / len(counts) >= 0.75:
            hits.setdefault("số gạch đầu dòng đều", []).append(
                (first_line.get(content[0]["no"], 1), f"{counts.count(top)}/{len(counts)} slide có đúng {top} ý"))
    # Ba tiêu đề liền nhau mở bằng cùng hai chữ
    titles = [(title_line[s["no"]], s["title"].lower().split()[:2]) for s in content if s["title"]]
    for (l1, a), (_, b), (_, c) in zip(titles, titles[1:], titles[2:]):
        if len(a) == 2 and a == b == c:
            hits.setdefault("tiêu đề lặp khuôn", []).append((l1, " ".join(a)))
            break


# Trọng số theo độ mạnh của dấu hiệu. Nhóm không có tên ở đây tính 1.
WEIGHTS = {
    "lời chatbot": 3, "câu dẫn": 3, "đối lập giả": 3, "nhãn báo giọng": 3,
    "diễn giải lại": 2, "tự kể dàn ý": 2, "mục kết dán nhãn": 2, "tổng kết rỗng": 3,
    "giới hạn kiến thức": 3, "dấu vết công cụ": 3, "chỉ dẫn chèn vào": 3, "mời tương tác": 2, "khẩu hiệu": 2, "emoji đầu dòng": 2, "văn dịch (vi)": 3, "động từ rỗng (vi)": 3,
    "thổi phồng": 2, "giật gân": 3, "câu hỏi mồi": 2, "chuỗi câu cụt": 2, "uy tín mơ hồ": 2, "quảng cáo": 2, "từ vựng AI (vi)": 2,
    "từ vựng AI (en)": 2, "né là/có": 2, "danh hóa (vi)": 2, "thừa nghĩa (vi)": 2,
    "chuỗi \"của\"": 2, "việc/sự dày": 2, "\"Điều này\"/\"Nó\" mở câu": 2,
    "hứa suông": 2, "tiêu đề dạng nhãn": 2, "tiêu đề đếm số ý": 2, "số gạch đầu dòng đều": 2,
    "lộ tên khung": 2, "tin nhắn định dạng như văn bản": 2, "tin nhắn khách sáo": 3, "tin nhắn dài": 2,
}
# Dấu hiệu cả bài: điểm cố định, không chia theo độ dài.
FILLER_WORDS = [
    r"\bcủa (bạn|tôi|chúng tôi|chúng ta|họ|anh ấy|cô ấy|nó)\b", r"\bmột\b", r"\b(các|những)\b", r"\bđược\b",
    r"\bcó thể\b", r"\bsẽ\b", r"\bđã\b", r"\brằng\b", r"\b(cho phép|giúp)\b", r"\b(điều này|nó)\b", r"\b(việc|sự)\b",
]

DOC_POINTS = {
    "hai chấm dồn dập": 6, "đoạn ngắn đều nhau": 4, "câu vụn": 4, "đại từ dày": 4, "chữ đệm dịch dày": 12,
    "bài đăng chia mục viết hoa": 4, "viết hoa để nhấn": 6, "ngoặc kép rào đón": 4, "gạch đầu dòng có nhãn": 4, "chia mục bằng emoji": 8, "in đậm dày": 5, "kết bài mời tương tác": 5, "bài mạng xã hội dài": 6, "chồng tiếng lóng": 8, "trộn giọng miền": 6,
}
# Ba dấu hiệu cả bài này người viết thật cũng hay có (blog xuống dòng liên tục, truyện ngắn câu cụt,
# bài hướng dẫn xưng "bạn"). Chỉ cộng điểm khi bài còn dính ít nhất một dấu hiệu mạnh.
WEAK_DOC = ("đoạn ngắn đều nhau", "câu vụn", "đại từ dày")
STRONG = {g for g, w in WEIGHTS.items() if w == 3} | (set(DOC_POINTS) - set(WEAK_DOC)) | {"tật lặp cả bài"}
for _g in list(DOC_POINTS) + ["tật lặp cả bài"]:
    WEIGHTS[_g] = 0


def doc_points(hits):
    backed = any(g in hits for g in STRONG)
    points = sum(v for g, v in DOC_POINTS.items() if g in hits and (backed or g not in WEAK_DOC))
    for group in TIC_GROUPS:  # một khuôn lặp 3 lần: 6 điểm, mỗi lần thêm 2 điểm, tối đa 15
        n = len(hits.get(group, []))
        if n >= 3 and "tật lặp cả bài" in hits:
            points += min(15, 6 + 2 * (n - 3))
    return points


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


def score(text, hits, burst=True):
    """Điểm theo thang 0-100: mật độ dấu hiệu có trọng số trên 100 chữ, cộng phần phạt khi câu dài đều nhau.

    burst=False bỏ phần phạt câu đều (dùng cho slide, vì gạch đầu dòng vốn ngắn và đều).
    """
    prose = prose_only(text)
    words = len(prose.split())
    weighted = sum(WEIGHTS.get(g, 1) * len(v) for g, v in hits.items())
    density = weighted * 100 / max(words, 50)
    lengths = [len(x.split()) for x in re.split(r"(?<=[.!?])\s+|\n+", prose) if len(x.split()) >= 3]
    cv = None
    burst_penalty = 0.0
    if burst and len(lengths) >= 5:
        cv = statistics.pstdev(lengths) / statistics.mean(lengths)
        burst_penalty = max(0.0, 0.35 - cv) * 40
    fixed = doc_points(hits)
    value = min(100, round(density * 2 + burst_penalty + fixed))
    band = next(name for limit, name in BANDS if value < limit)
    return {"score": value, "band": band, "words": words, "weighted_hits": weighted,
            "document_points": fixed, "sentence_length_cv": None if cv is None else round(cv, 2)}


def load(path):
    """Đọc file. Trả về (text, deck, index); deck và index là None nếu không phải .pptx."""
    if path and path.lower().endswith(".pptx"):
        deck = slides_mod.read_pptx(path)
        text, index = slides_mod.to_text(deck)
        return text, deck, index
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read(), None, None
    return sys.stdin.read(), None, None


def titles_of(text, deck):
    if deck is not None:
        return [f"{s['no']:>2}. {s['title'] or '(không có tiêu đề)'}" for s in deck]
    return [line.strip() for line in prose_only(text).splitlines() if re.match(r"\s*#{1,6}\s", line)]


def main():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # Windows mặc định cp1252, in chữ có dấu sẽ lỗi
    ap = argparse.ArgumentParser(description="Quét dấu hiệu văn AI bề mặt (Việt/Anh), đọc được cả .pptx.")
    ap.add_argument("file", nargs="?", help="file cần quét (.md, .txt, .pptx); bỏ trống thì đọc stdin")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    ap.add_argument("--max", type=int, metavar="N", help="thoát mã 1 nếu điểm lớn hơn N")
    ap.add_argument("--titles", action="store_true",
                    help="chỉ in các tiêu đề (slide hoặc heading Markdown) theo thứ tự")
    ap.add_argument("--meta", action="store_true",
                    help="bỏ qua phần trích dẫn (dòng '>', bảng, chữ trong ngoặc kép); "
                         "dùng cho văn bản bàn về dấu hiệu văn AI")
    ap.add_argument("--chat", action="store_true",
                    help="văn bản là tin nhắn trả lời: kiểm thêm định dạng, độ dài, câu khách sáo")
    ap.add_argument("--text", action="store_true",
                    help="in chữ của từng slide kèm vị trí (chỉ cho .pptx), không quét")
    args = ap.parse_args()
    text, deck, index = load(args.file)
    if args.text:
        if deck is None:
            sys.exit("--text chỉ dùng cho file .pptx.")
        for s in deck:
            print(f"=== Slide {s['no']}" + (" (ẩn)" if s["hidden"] else ""))
            print(f"Tiêu đề: {s['title'] or '(không có)'}")
            for label, items in (("Nội dung", s["body"]), ("Bảng", s["table"]), ("Ghi chú", s["notes"])):
                if items:
                    print(f"{label}:")
                    print("\n".join(f"  - {x}" for x in items))
            print()
        return
    if args.titles:
        print("\n".join(titles_of(text, deck)) or "Không thấy tiêu đề nào.")
        print("\nĐọc liền các tiêu đề trên: có thành một mạch không, slide nào chỉ là nhãn chủ đề?")
        return
    if args.meta and deck is None:
        text = strip_quoted(text)
    hits, total = scan(text, doc=deck is None)
    if args.chat and deck is None:
        chat_checks(text, hits)
    where = {}
    if deck is not None:
        slide_checks(deck, index, hits)
        where = slides_mod.labels(index)
    result = score(text, hits, burst=deck is None)
    details = personal_details(text) if deck is None and not args.meta else []
    loc = (lambda no: where.get(no, f"dòng {no}")) if deck is not None else (lambda no: f"dòng {no}")
    unit = f"{len(deck)} slide" if deck is not None else f"{total} dòng"
    confirm = ""
    if details:
        confirm = ("\nBài xưng \"mình\"/\"tôi\" có chi tiết riêng (không tính điểm). Nếu bài do AI viết hộ thì hỏi lại "
                   "người đứng tên xem có thật không: " + ", ".join(f"{m} (dòng {no})" for no, m in details[:10])
                   + (f", và {len(details) - 10} chỗ khác" if len(details) > 10 else "") + ".")
    if args.json:
        result["to_confirm"] = [{"line": no, "match": m} for no, m in details]
        result["hits"] = {g: [{"line": no, "where": loc(no), "match": m} for no, m in v]
                          for g, v in hits.items()}
        if deck is not None:
            result["slides"] = len(deck)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not hits:
        print(f"Điểm {result['score']}/100 ({result['band']}). Không thấy dấu hiệu bề mặt. "
              "Vẫn cần tự đọc phần cấu trúc." + confirm)
    else:
        count = sum(len(v) for v in hits.values())
        print(f"Điểm {result['score']}/100 ({result['band']}): {count} dấu hiệu trong {unit}, "
              f"{result['words']} chữ.\n")
        for group, items in sorted(hits.items(), key=lambda kv: -len(kv[1])):
            print(f"[{group}] {len(items)}")
            for no, m in items[:12]:
                print(f"  {loc(no)}: {m}")
            if len(items) > 12:
                print(f"  ... và {len(items) - 12} chỗ khác")
        print("\nMột dấu hiệu đơn lẻ chưa nói lên gì. Nhiều nhóm cùng lúc mới đáng sửa.")
        print("Điểm đo thói quen viết theo khuôn, không phải xác suất do AI viết." + confirm)
    if args.max is not None and result["score"] > args.max:
        sys.exit(1)


if __name__ == "__main__":
    main()
