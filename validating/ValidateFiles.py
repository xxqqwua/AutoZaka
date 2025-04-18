from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

import tkinter as tk
from tkinter import messagebox


class Validator:
    def __init__(self):
        pass

    @staticmethod
    def validate_env_file():
        if not os.path.exists(os.path.join(os.path.dirname(__file__), '.env')):
            with open('.env', 'w') as f:
                f.write('EMAIL=\nPASSWORD=')

        if not os.getenv('EMAIL') or not os.getenv('PASSWORD'):
            messagebox.showerror("AutoZaka: Error", "Please fill in the .env file and restart the program.")
            logger.error("Please fill in the .env file and restart the program.")
            os.startfile(os.path.join(os.path.dirname(__file__), '.env'))
            exit()

        if not '@' in os.getenv('EMAIL'):
            messagebox.showerror("AutoZaka: Error", "Please enter a valid email address and restart the program.")
            logger.error("Please enter a valid email address and restart the program.")
            os.startfile(os.path.join(os.path.dirname(__file__), '.env'))
            exit()
