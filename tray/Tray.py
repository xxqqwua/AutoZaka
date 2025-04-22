import os
import io
import requests
import logging
import threading

import pystray
from pystray import Icon, Menu, MenuItem as Item
from PIL import Image


def open_logs():
    logging.debug('Open logs')
    os.startfile('app.log')


def open_env():
    logging.debug('.ENV logs')
    os.startfile('.env')

def on_quit():
    logging.info('Exit... Bye-bye :(')
    icon.stop()
    os._exit(0)


menu = Menu(
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
