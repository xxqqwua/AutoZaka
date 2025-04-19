import logging

import selenium.common
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from authorization.CookiesManager import CookiesManager
from authorization.RecaptchaSolver import RecaptchaSolver


class AuthManager:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        # self.options.add_argument("--headless")
        self.options.add_argument("--mute-audio")
        self.driver = webdriver.Firefox(options=self.options)

    def login_via_pass(self, email, password):
        recaptcha_solver = RecaptchaSolver(self.driver)

        logging.info("Going to the authorization site")
        logging.debug(f"Received data: email - {email}; password - {password}")
        self.driver.get('https://zaka-zaka.com/profile/auth')
        wait = WebDriverWait(self.driver, 180)
        recaptcha_solver.solveCaptcha()

        input_login = wait.until(EC.presence_of_element_located((By.NAME, 'LoginForm[login]')))
        input_login.send_keys(email)
        input_login.send_keys(Keys.ENTER)
        self.error_handling("Wrong email, check the .env file and restart the program.")
        logging.info("The login has been entered")

        input_password = wait.until(EC.visibility_of_element_located((By.NAME, 'LoginForm[password]')))
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        self.error_handling("Wrong password, check the .env file and restart the program.")
        logging.info("The password has been entered")

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-user-name')))

        cks_mngr = CookiesManager(self.driver)
        token, phpsessid = cks_mngr.collect_cookies()
        cks_mngr.save_cookies(token, phpsessid)
        logging.info("The authorization has been completed & Cookies have been saved")

        self.driver.quit()

    def error_handling(self, INFO: str):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.error:nth-child(1)'))
            )
            logging.error(INFO)
            self.driver.quit()
            exit()
        except selenium.common.TimeoutException:
            pass
