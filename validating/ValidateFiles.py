import logging
import os
from pathlib import Path
from tkinter import messagebox

from dotenv import load_dotenv


class Validator:
    def __init__(self):
        self.folder_name = "AutoZaka"
        self.home_dir = Path.home()
        self.possible_docs_folders = ["Documents", "Документы"]  # may vary depending on the language of the system
        self.documents_path = None
        self.app_folder_path = None
        self.dotenv_path = None
        self.log_path = None

    def create_folder(self):
        for folder in self.possible_docs_folders:
            potential_path = self.home_dir / folder
            if potential_path.is_dir():
                self.documents_path = potential_path
                logging.debug(f"Documents folder found at {self.documents_path}")
                break

        if self.documents_path:
            full_path_to_new_folder = self.documents_path / self.folder_name

            try:
                os.makedirs(full_path_to_new_folder, exist_ok=True)
                self.app_folder_path = full_path_to_new_folder
                logging.debug(f"Folder {self.folder_name} created successfully or it already exists.")
            except OSError as e:
                logging.error(f"Error creating folder {self.folder_name}: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
        else:
            logging.error("Documents folder not found.")

    def validate_env_file(self):
        self.create_folder()

        self.dotenv_path = self.app_folder_path / '.env'
        load_dotenv(dotenv_path=self.dotenv_path)

        if not os.path.exists(self.dotenv_path):
            with open(self.dotenv_path, 'w') as f:
                f.write('EMAIL=\nPASSWORD=')

        if not os.getenv('EMAIL') or not os.getenv('PASSWORD'):
            messagebox.showerror("AutoZaka: Error", "Please fill in the .env file and restart the program.")
            logging.error("Please fill in the .env file and restart the program.")
            os.startfile(self.dotenv_path)
            os._exit(0)

        if '@' not in os.getenv('EMAIL'):
            messagebox.showerror("AutoZaka: Error", "Please enter a valid email address and restart the program.")
            logging.error("Please enter a valid email address and restart the program.")
            os.startfile(self.dotenv_path)
            os._exit(0)

        password = os.getenv('PASSWORD')
        email = os.getenv('EMAIL')

        return email, password

    def validate_log_file(self):
        self.create_folder()

        self.log_path = self.app_folder_path / 'app.log'

        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                f.close()
