from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os
import sys


def on_quit(icon):  # Stop the icon and exit the program.
    icon.stop()
    sys.exit(0)

def on_logs():  # Open the log file.
    os.startfile("logs.txt")

def create_image():
    # Создание изображения с белым фоном 32x32 (размер как в SVG)
    image = Image.new('RGB', (32, 32), 'white')
    draw = ImageDraw.Draw(image)

    # Нарисовать прямоугольник как основу билета
    draw.rectangle([(0, 0), (31, 31)], outline='#231f20', width=2)

    # Нарисовать элементы внутри билета (эти данные упрощены)
    draw.rectangle([(4, 4), (28, 28)], outline='#231f20', width=1)  # Внутренний квадрат
    draw.line([(4, 8), (28, 8)], fill='#231f20', width=1)  # Верхняя линия
    draw.line([(4, 24), (28, 24)], fill='#231f20', width=1)  # Нижняя линия

    return image


menu = Menu(
    MenuItem('Logs', on_logs),
    MenuItem('Quit', on_quit)
)

def icon_run():  # Start the icon.
    icon = Icon("Test Tray", create_image(), menu=menu)
    icon.run()