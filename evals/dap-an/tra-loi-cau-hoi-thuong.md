Cả hai đều dùng để đưa thay đổi từ nhánh này sang nhánh khác. Chỗ khác nhau là cách chúng ghi lại lịch sử.

`git merge` giữ nguyên lịch sử của cả hai nhánh, rồi tạo thêm một commit merge để nối chúng lại. Ví dụ bạn đang ở `feature` và chạy `git merge main`: các commit cũ vẫn giữ nguyên, Git chỉ thêm một commit có hai cha. Lịch sử phản ánh đúng chuyện đã xảy ra, nhưng nếu merge nhiều thì đồ thị commit sẽ rối, nhìn như mạng nhện.

`git rebase` lấy từng commit của nhánh bạn đặt lại lên đầu nhánh kia, như thể bạn bắt đầu làm từ đó. Chạy `git rebase main` khi đang ở `feature` thì các commit của `feature` sẽ được tạo lại, có hash mới, và nằm nối tiếp sau commit mới nhất của `main`. Lịch sử thành một đường thẳng, dễ đọc, dễ `git log` và `git bisect`. Đổi lại, bạn đã viết lại lịch sử.

Dùng rebase khi:
- Nhánh còn ở máy bạn hoặc chỉ mình bạn làm, và bạn muốn cập nhật code mới từ `main` trước khi mở PR.
- Muốn dọn commit trước khi gửi review: gộp, sửa message, bỏ commit thừa bằng `git rebase -i`.

Dùng merge khi:
- Nhánh đã push lên và có người khác cùng làm. Rebase nhánh chung sẽ đổi hash, người khác pull về sẽ bị lệch và phải xử lý rất mệt.
- Đưa một feature đã xong vào `main`/`develop` và muốn giữ dấu vết là feature này được gộp vào lúc nào.
- Team cần lịch sử đúng như thực tế để truy vết.

Nhiều team làm kết hợp: rebase nhánh cá nhân lên `main` cho gọn, rồi merge vào `main` qua PR. Có team chọn squash merge để mỗi feature chỉ còn một commit. Bạn chỉ cần nhớ một nguyên tắc: không rebase nhánh mà người khác đã pull về.

Gặp conflict thì merge bắt bạn xử lý một lần cho cả nhánh. Rebase có thể dừng ở từng commit, bạn sửa xong thì `git add` rồi `git rebase --continue`, còn muốn bỏ thì `git rebase --abort`.
