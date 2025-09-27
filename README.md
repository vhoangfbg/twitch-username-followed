# Username Follower - Danh sách người đã Follow

Project này đã được thay đổi để trích xuất và gửi **danh sách username những người bạn đã follow trên Twitch** thay vì thông báo live stream.

## Chức năng

- 📧 Đọc email từ Twitch để tìm các username đã follow
- 📋 Tạo danh sách tất cả username
- 💬 Gửi danh sách lên Discord qua webhook
- 💾 Lưu backup danh sách vào file `followed_usernames.txt`
- 🔄 Tự động cập nhật mỗi 6 tiếng

## Cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Cấu hình `config.json`:**
```json
{
    "gmail_user": "your_email@gmail.com",
    "gmail_app_password": "your_app_password",
    "webhook_url": "https://discord.com/api/webhooks/..."
}
```

## Cách sử dụng

1. **Chạy script:**
```bash
python main.py
```

2. **Script sẽ:**
   - Kết nối Gmail và đọc email từ Twitch
   - Tìm tất cả username trong email (từ links, notifications, etc.)
   - Gửi danh sách lên Discord
   - Lưu backup vào `followed_usernames.txt`
   - Chờ 6 tiếng trước lần kiểm tra tiếp theo

## Output

### Discord Message
- 📋 **Danh sách Username đã Follow trên Twitch**
- Tổng số người dùng
- Danh sách username được sắp xếp alphabetically
- Thời gian cập nhật

### File Output
- `followed_usernames.txt` - Backup danh sách username
- `log.txt` - Log hoạt động

## Tính năng

- ✅ Tự động loại bỏ username không hợp lệ
- ✅ Chia nhỏ message nếu danh sách quá dài (Discord limit)
- ✅ Chỉ gửi khi có thay đổi
- ✅ Backup tự động
- ✅ Logging chi tiết

## Lưu ý

- Script chạy mỗi 6 tiếng để tránh spam
- Email sẽ được giữ nguyên (không xóa)
- Username phải có 3-25 ký tự và chỉ chứa chữ cái, số, underscore
- Tự động loại bỏ các link system như unsubscribe, help, etc.

## File Structure

```
username-follower/
├── main.py              # Script chính
├── email_reader.py      # Đọc và trích xuất username từ email
├── config.json          # Cấu hình Gmail và Discord
├── requirements.txt     # Dependencies
├── followed_usernames.txt  # Backup danh sách (auto-generated)
└── log.txt             # Log files (auto-generated)
```

## Troubleshooting

1. **Lỗi Gmail:** Kiểm tra App Password và 2FA
2. **Lỗi Discord:** Kiểm tra webhook URL
3. **Không tìm thấy username:** Kiểm tra email Twitch trong inbox
