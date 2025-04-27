import os
import io
import requests
import logging
import threading
import asyncio

import tkinter as tk
from tkinter import messagebox

import pystray
from pystray import Icon, Menu, MenuItem as Item
from PIL import Image

from misc.HappyHour import HappyHour


def open_logs():
    logging.debug('Open logs')
    os.startfile('app.log')


def open_env():
    logging.debug('.ENV logs')
    os.startfile('.env')


async def happy_hour():
    HP = HappyHour()
    await HP.extract_happy_hour_games()

    formatted_games = "\n".join(
        f"Name: {game['name']}\n"
        f"Tags: {game['tags']}\n"
        f"Discount: {game['discount']}\n"
        f"Current Price: {game['current_price']}\n"
        for game in HP.happy_hour_games
    )

    thread = threading.Thread(target=lambda: messagebox.showinfo("Happy Hour", formatted_games))
    thread.start()


def happy_hour_wrapper():
    try:
        asyncio.run(happy_hour())
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def on_quit():
    logging.info('Exit... Bye-bye :(')
    icon.stop()
    os._exit(0)


menu = Menu(
    Item('Happy Hour', happy_hour_wrapper),
    Item('Open Log', open_logs),
    Item('Open .env', open_env),
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
