from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os
import sys


def on_quit(icon):  # Stop the icon and exit the program.
    icon.stop()
    sys.exit(0)

def on_logs():  # Open the log file.
    os.startfile("logs.txt")

def create_image():  # Create an image for the icon.
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=(0, 0, 0))
    return image


menu = Menu(
    MenuItem('Logs', on_logs),
    MenuItem('Quit', on_quit)
)

def icon_run():  # Start the icon.
    icon = Icon("Test Tray", create_image(), menu=menu)
    icon.run()