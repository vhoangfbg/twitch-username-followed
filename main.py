import time
import json
import requests
from datetime import datetime
from email_reader import read_latest_game_email

def send_username_list_to_discord(usernames):
    """
    Gửi danh sách username đã follow lên Discord
    """
    try:
        with open("config.json") as f:
            config = json.load(f)

        webhook_url = config["webhook_url"]
        
        if not usernames:
            print("[ℹ️] Không có username nào để gửi.")
            return
        
        # Tạo message với danh sách username
        username_text = "\n".join([f"• {username}" for username in sorted(usernames)])
        
        # Chia nhỏ message nếu quá dài (Discord limit 2000 chars)
        max_length = 1800  # Để lại chỗ cho title và format
        
        if len(username_text) <= max_length:
            # Gửi một message
            data = {
                "content": "�� **Danh sách Username đã Follow trên Twitch**",
                "embeds": [
                    {
                        "title": f"Tổng cộng: {len(usernames)} người dùng",
                        "description": f"```\n{username_text}\n```",
                        "color": 9442302,  # Purple color
                        "footer": {
                            "text": f"Cập nhật lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                        }
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=data)
            if response.status_code != 204:
                print(f"[❗] Discord webhook failed: {response.status_code} - {response.text}")
            else:
                print(f"[✅] Đã gửi danh sách {len(usernames)} username")
                log_to_file(f"[✅] Đã gửi danh sách {len(usernames)} username")
        else:
            # Chia nhỏ thành nhiều message
            chunks = []
            current_chunk = []
            current_length = 0
            
            for username in sorted(usernames):
                line = f"• {username}\n"
                if current_length + len(line) > max_length:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = [username]
                    current_length = len(line)
                else:
                    current_chunk.append(username)
                    current_length += len(line)
            
            if current_chunk:
                chunks.append(current_chunk)
            
            # Gửi từng chunk
            for i, chunk in enumerate(chunks):
                chunk_text = "\n".join([f"• {username}" for username in chunk])
                
                data = {
                    "content": f"📋 **Danh sách Username đã Follow trên Twitch (Phần {i+1}/{len(chunks)})**",
                    "embeds": [
                        {
                            "title": f"Phần {i+1}: {len(chunk)} người dùng",
                            "description": f"```\n{chunk_text}\n```",
                            "color": 9442302,
                            "footer": {
                                "text": f"Tổng: {len(usernames)} - Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                            }
                        }
                    ]
                }
                
                response = requests.post(webhook_url, json=data)
                if response.status_code != 204:
                    print(f"[❗] Discord webhook failed for chunk {i+1}: {response.status_code}")
                else:
                    print(f"[✅] Đã gửi phần {i+1}/{len(chunks)} ({len(chunk)} username)")
                
                # Delay giữa các message để tránh rate limit
                if i < len(chunks) - 1:
                    time.sleep(1)
            
            log_to_file(f"[✅] Đã gửi danh sách {len(usernames)} username trong {len(chunks)} phần")

    except Exception as e:
        print(f"[❌] Gửi Discord thất bại: {e}")

def log_to_file(log_message):
    """
    Ghi log vào file
    """
    try:
        with open("log.txt", "a", encoding='utf-8') as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - {log_message}\n")
    except Exception as e:
        print(f"[❌] Lỗi khi ghi log: {e}")

def main_loop():
    """
    Vòng lặp chính - chạy một lần để lấy danh sách username
    """
    last_sent_count = 0
    
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[⏱] Kiểm tra lúc {now}...")

        usernames = read_latest_game_email()
        if usernames:
            print(f"[📧] Tìm thấy {len(usernames)} username.")
            
            # Chỉ gửi nếu có thay đổi về số lượng hoặc chưa gửi lần nào
            if len(usernames) != last_sent_count:
                print("[🚀] Gửi danh sách username lên Discord...")
                send_username_list_to_discord(usernames)
                last_sent_count = len(usernames)
                
                # Lưu danh sách vào file để backup
                with open("followed_usernames.txt", "w", encoding='utf-8') as f:
                    for username in sorted(usernames):
                        f.write(f"{username}\n")
                print("[💾] Đã lưu danh sách vào followed_usernames.txt")
                
            else:
                print("[🔁] Số lượng username không thay đổi, không gửi lại.")
        else:
            print("[ℹ️] Không tìm thấy username nào.")

        # Chạy mỗi 6 tiếng (21600 giây) thay vì 1 phút
        print("[💤] Chờ 6 tiếng trước lần kiểm tra tiếp theo...")
        time.sleep(21600)

if __name__ == "__main__":
    main_loop()
