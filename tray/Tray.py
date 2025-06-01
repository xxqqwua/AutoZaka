import asyncio
import datetime
import io
import logging
import os
import threading
from datetime import timedelta
from tkinter import messagebox

import requests
from PIL import Image
from pystray import Icon, Menu, MenuItem as Item

from misc.AutoStartUp import AutoStartUp
from misc.HappyHour import HappyHour
from validating.Validator import Validator

AutoStartUp = AutoStartUp()
AutoStartUp_is_set = AutoStartUp.check_autostartup()


def open_logs():
    logging.debug('Open logs')

    v = Validator()
    v.validate_log_file()
    log_path = v.log_path

    try:
        os.startfile(log_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def open_env():
    logging.debug('.ENV logs')

    v = Validator()
    v.validate_env_file()
    env_path = v.dotenv_path

    try:
        os.startfile(env_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


async def happy_hour():
    HP = HappyHour()
    await HP.extract_happy_hour_games()
    next_happy_hour_sale_unix = await HP.get_next_happy_hour_start()

    next_happy_hour_sale_eu = datetime.datetime.fromtimestamp(
        next_happy_hour_sale_unix)  # convert from unix to european format
    now = datetime.datetime.now()
    delta = next_happy_hour_sale_eu - now
    delta = delta - timedelta(microseconds=delta.microseconds)  # Take away the microseconds

    formatted_games = "\n".join(
        f"Name: {game['name']}\n"
        f"Tags: {game['tags']}\n"
        f"Discount: {game['discount']}\n"
        f"Current Price: {game['current_price']}\n"
        + (f"Steam Prices: {game['steam_price']}\n" if game['steam_price'] else "")
        for game in HP.happy_hour_games
    )

    thread = threading.Thread(target=lambda: messagebox.showinfo("Happy Hour",
                                                                 f'{formatted_games}\nWhen next happy hour?\n{next_happy_hour_sale_eu}\nin {delta}'))
    thread.start()


def happy_hour_wrapper():
    try:
        asyncio.run(happy_hour())
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def set_auto_start_up():
    global AutoStartUp_is_set

    if AutoStartUp_is_set:
        AutoStartUp.remove_autostartup()
        AutoStartUp_is_set = False
    else:
        AutoStartUp.set_autostartup()
        AutoStartUp_is_set = True


def on_quit():
    logging.info('Exit... Bye-bye :(')
    icon.stop()
    os._exit(0)


menu = Menu(
    Item('Happy Hour', happy_hour_wrapper),
    Item('Open Log', open_logs),
    Item('Open .env', open_env),
    Item('AutoStartUp', set_auto_start_up, checked=lambda i: AutoStartUp.check_autostartup()),
    # Double display for AutoStartUP in logs is normal:
    # The first time is when the menu is just being built: you need to understand which items are checked.
    # The second time is when the menu is actually shown to the user, to update the state
    # (in case something changed between opening and rendering).
    Item('Exit', on_quit)
)

icon_bytes = requests.get('https://zaka-zaka.com/favicon.ico').content
icon_image = Image.open(io.BytesIO(icon_bytes))

icon = Icon('My app', icon_image, menu=menu)


def run_tray():
    icon.run()


tray_thread = threading.Thread(target=run_tray)
tray_thread.daemon = True  # Set as daemon so it exits when main thread exits
tray_thread.start()
