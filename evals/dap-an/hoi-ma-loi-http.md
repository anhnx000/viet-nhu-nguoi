401 nghĩa là máy chủ chưa biết bạn là ai: request không gửi thông tin đăng nhập, hoặc token sai hay đã hết hạn. Đăng nhập lại hoặc gửi đúng token thì có thể qua. Khi trả 401, máy chủ nên kèm header `WWW-Authenticate` để báo cách xác thực.

403 nghĩa là máy chủ đã biết bạn là ai nhưng bạn không có quyền làm việc đó, ví dụ tài khoản thường gọi API chỉ dành cho admin. Đăng nhập lại cũng không giải quyết được.

Cách chọn: thiếu hoặc sai thông tin đăng nhập thì trả 401; đăng nhập đúng mà không đủ quyền thì trả 403. Nếu không muốn để lộ là tài nguyên có tồn tại, nhiều hệ thống trả 404 thay cho 403.
