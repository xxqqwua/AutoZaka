import os
import configparser
from GUI import input_gui


# Path to the config file
filepath = 'config.txt'

def if_config_exists():
    if not os.path.exists(filepath):  # Check if the config file exists, create the file if it doesn't
        open(filepath, "a").close()
    if os.stat(filepath).st_size == 0:  # If the file is empty, ask for the token and write it to the file
        LOGIN, PASSWORD = input_gui()
        with open(filepath, "w") as f:
            f.write(f"[global]\nLOGIN={LOGIN}\nPASSWORD={PASSWORD}")
        from driver import auth
        auth()


def read_login_n_pass():
    if_config_exists()
    config = configparser.RawConfigParser()
    config.read_file(open(filepath))
    LOGIN = config.get('global', 'LOGIN')
    PASSWORD = config.get('global', 'PASSWORD')
    return LOGIN, PASSWORD

def read_token_n_cookie():
    if_config_exists()
    config = configparser.RawConfigParser()
    config.read_file(open(filepath))
    YII_CSRF_TOKEN = config.get('global', 'YII_CSRF_TOKEN')  # Get the YII_CSRF_TOKEN value from the config file
    COOKIE = config.get('global', 'COOKIE')  # Get the COOKIE value from the config file
    return YII_CSRF_TOKEN, COOKIE
