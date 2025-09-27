import imaplib
import email
from bs4 import BeautifulSoup
import json
import re
from email.utils import parsedate_to_datetime

def read_followed_usernames():
    """
    Đọc email từ Twitch để trích xuất danh sách username đã follow
    """
    try:
        print("[📥] Đang đọc cấu hình...")
        with open("config.json") as f:
            config = json.load(f)

        gmail_user = config["gmail_user"]
        gmail_pass = config["gmail_app_password"]

        print("[🔐] Đang kết nối Gmail...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_pass)
        mail.select("inbox")

        print("[📨] Đang tìm email Twitch...")
        result, data = mail.search(None, '(FROM "twitch")')
        if result != "OK":
            print("[❌] Không thể tìm email.")
            return []

        mail_ids = data[0].split()
        if not mail_ids:
            print("[❌] Không có email nào khớp.")
            return []

        # Lấy email gần đây nhất (500 email)
        latest_emails = reversed(mail_ids[-500:])
        print(f"[ℹ️] Đang kiểm tra {len(mail_ids[-500:])} email gần đây...")

        followed_usernames = set()

        for mail_id in latest_emails:
            result, data = mail.fetch(mail_id, "(RFC822)")
            if result != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Trích xuất usernames từ email
            usernames = extract_usernames_from_email(msg)
            followed_usernames.update(usernames)

        mail.close()
        mail.logout()

        return list(followed_usernames)

    except Exception as e:
        print(f"[❌] Lỗi khi đọc email: {e}")
        return []

def extract_usernames_from_email(msg):
    """
    Trích xuất usernames từ một email
    """
    usernames = set()
    
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    usernames.update(extract_usernames_from_html(html_body))
        else:
            if msg.get_content_type() == "text/html":
                html_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                usernames.update(extract_usernames_from_html(html_body))

        return usernames

    except Exception as e:
        print(f"[❌] Lỗi khi xử lý email: {e}")
        return set()

def extract_usernames_from_html(html_body):
    """
    Trích xuất usernames từ HTML của email
    """
    usernames = set()
    
    try:
        soup = BeautifulSoup(html_body, "html.parser")
        
        # Tìm tất cả các link twitch.tv
        # Pattern 1: Links có href chứa twitch.tv
        twitch_links = soup.find_all("a", href=re.compile(r"twitch\.tv/[^/\s]+"))
        for link in twitch_links:
            href = link.get("href", "")
            username = extract_username_from_url(href)
            if username and is_valid_username(username):
                usernames.add(username)
        
        # Pattern 2: Text chứa twitch.tv/username
        twitch_text_links = soup.find_all(text=re.compile(r"twitch\.tv/[^/\s]+"))
        for text in twitch_text_links:
            matches = re.findall(r"twitch\.tv/([^/\s]+)", text)
            for match in matches:
                if is_valid_username(match):
                    usernames.add(match)
        
        # Pattern 3: Tìm trong href attribute
        all_links = soup.find_all("a")
        for link in all_links:
            href = link.get("href", "")
            if "twitch.tv" in href:
                username = extract_username_from_url(href)
                if username and is_valid_username(username):
                    usernames.add(username)
        
        return usernames

    except Exception as e:
        print(f"[❌] Lỗi khi phân tích HTML: {e}")
        return set()

def extract_username_from_url(url):
    """
    Trích xuất username từ URL Twitch
    """
    try:
        # Loại bỏ protocol và domain
        if "twitch.tv/" in url:
            parts = url.split("twitch.tv/")
            if len(parts) > 1:
                username_part = parts[1]
                # Lấy phần đầu trước dấu / hoặc ?
                username = username_part.split('/')[0].split('?')[0].strip()
                return username
        return None
    except:
        return None

def is_valid_username(username):
    """
    Kiểm tra username có hợp lệ không
    """
    if not username:
        return False
    
    # Loại bỏ các username không hợp lệ
    invalid_usernames = {
        "email-unsubscribe", "unsubscribe", "www", "m", "help", "support",
        "login", "signup", "directory", "p", "videos", "clips", "settings",
        "friends", "following", "downloads", "activate", "reset", "verify"
    }
    
    if username.lower() in invalid_usernames:
        return False
    
    # Username phải có độ dài hợp lý (3-25 ký tự)
    if len(username) < 3 or len(username) > 25:
        return False
    
    # Username chỉ chứa chữ cái, số và underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    
    return True

# Để tương thích với code cũ, giữ lại function name cũ
def read_latest_game_email():
    """
    Function cũ để tương thích, giờ sẽ trả về danh sách username
    """
    usernames = read_followed_usernames()
    return usernames
