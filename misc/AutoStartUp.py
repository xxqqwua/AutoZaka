import winreg
import os
import logging


class AutoStartUp:
    def __init__(self):
        self.app_name = "AutoZaka.exe"
        self.app_path = os.path.abspath(self.app_name)

    def set_autostartup(self):
        if not os.path.exists(self.app_path):
            logging.error("File not found. AutoStartUp is not set.")
            return "File not found"

        logging.debug("Setting AutoStartUp...")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        try:
            winreg.SetValueEx(key, "AutoZaka", 0, winreg.REG_SZ, self.app_path)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            winreg.CloseKey(key)

    @staticmethod
    def remove_autostartup():
        logging.debug("Removing AutoStartUp...")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(key, "AutoZaka")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            winreg.CloseKey(key)

    @staticmethod
    def check_autostartup():
        logging.debug("Checking AutoStartUp...")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, "AutoZaka")
            logging.debug("AutoStartUp has already been set")
            return True
        except Exception as e:
            logging.debug(f"AutoStartUp is not set: {e}")
            return False
        finally:
            winreg.CloseKey(key)
