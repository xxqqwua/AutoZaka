import os
import configparser
from GUI import input_gui


# Path to the config file
filepath = 'config.txt'


def if_config_exists():
    if not os.path.exists(filepath):  # Check if the config file exists, create the file if it doesn't
        open(filepath, "a").close()
    if os.stat(filepath).st_size == 0:  # If the file is empty, ask for the token and write it to the file
        TOKEN = input_gui()
        with open(filepath, "w") as f:
            f.write(f"[global]\nYII_CSRF_TOKEN={TOKEN}")


def read_config():
    if_config_exists()
    config = configparser.RawConfigParser()
    config.read_file(open(filepath))
    YII_CSRF_TOKEN = config.get('global', 'YII_CSRF_TOKEN')  # Get the YII_CSRF_TOKEN value from the config file
    return YII_CSRF_TOKEN
