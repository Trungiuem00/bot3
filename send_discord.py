import os
import time
import threading
import requests
from flask import Flask

# ========== Cấu hình ==========
TOKEN = os.getenv("DISCORD_TOKEN")  # Token tài khoản Discord
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID của kênh Discord
FILE_PATH = "noidung.txt"  # File chứa nội dung
DELAY = 6  # Thời gian gửi tin nhắn lại mỗi lần (giây)

# ========== Header cho API Discord ==========
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# ========== Flask giữ tool luôn chạy ==========
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot đang chạy"

# ========== Hàm đọc và định dạng nội dung ==========
def format_file_content(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return "\n".join([f"> # {line.strip()}" for line in lines if line.strip()])
    except FileNotFoundError:
        return "> # File noidung.txt không tồn tại."

# ========== Hàm gửi tin nhắn vào Discord ==========
def send_loop():
    while True:
        content = format_file_content(FILE_PATH)
        if len(content) > 2000:
            print("⚠️ Nội dung vượt quá giới hạn 2000 ký tự.")
        else:
            res = requests.post(
                f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages",
                headers=headers,
                json={"content": content}
            )
            if res.status_code == 200:
                print("✅ Gửi thành công.")
            else:
                print(f"❌ Lỗi {res.status_code}: {res.text}")
        
        time.sleep(DELAY)

# ========== Khởi chạy bot và Flask server ==========
if __name__ == "__main__":
    if not TOKEN or not CHANNEL_ID:
        print("⚠️ Thiếu biến môi trường DISCORD_TOKEN hoặc CHANNEL_ID.")
    else:
        print("🚀 Khởi động bot và Flask server...")

        # Chạy bot trong một luồng riêng
        threading.Thread(target=send_loop).start()

        # Chạy Flask giữ server "sống"
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
