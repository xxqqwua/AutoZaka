import requests
import schedule
import time
import logging

from config import read_config


TOKEN = read_config()
COOKIE = read_config()[1]
logging.basicConfig(filename='logs.txt', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


url = "https://zaka-zaka.com/game/gifts/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://zaka-zaka.com",
    "Connection": "keep-alive",
    "Referer": "https://zaka-zaka.com/game/gifts/",
    "Cookie": COOKIE
}

def random_steam_key():
    # Enters a drawing for a random steam key gift.
    data = {"type": "1", "YII_CSRF_TOKEN": TOKEN}
    r = requests.post(url, headers=headers, data=data)
    logging.info(f"enter a drawing for a random steam key gift, code {r.status_code}")

def random_game():
    # Enters a drawing for a random game gift.
    data = {"type": "4", "YII_CSRF_TOKEN": TOKEN}
    r = requests.post(url, headers=headers, data=data)
    logging.info(f"enter a drawing for a random game gift, code {r.status_code}")

def coupons():
    # Enters a drawing for a coupon gift.
    data = {"type": "5", "YII_CSRF_TOKEN": TOKEN}
    r = requests.post(url, headers=headers, data=data)
    logging.info(f"enter a drawing for a coupon gift, code {r.status_code}")


def scheduler():
    # Enters all drawings at once.
    random_steam_key()
    random_game()
    coupons()

    logging.info("start schedule")
    # Enters drawings at certain times of the day.
    schedule.every().day.at("10:05").do(coupons)
    schedule.every().day.at("20:05").do(coupons)

    schedule.every().day.at("13:05").do(random_steam)
    schedule.every().day.at("17:05").do(random_steam)
    schedule.every().day.at("21:05").do(random_steam)
    schedule.every().day.at("00:05").do(random_steam)

    schedule.every().day.at("20:07").do(good_game)

    # Runs all scheduled functions in a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)
