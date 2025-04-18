import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from authorization.CookiesManager import CookiesManager
from authorization.RecaptchaSolver import RecaptchaSolver

logger = logging.getLogger(__name__)


class AuthManager:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--mute-audio")
        self.driver = webdriver.Firefox(options=self.options)

    def login_via_pass(self, email, password):
        recaptchaSolver = RecaptchaSolver(self.driver)

        logger.info("Going to the authorization site")
        self.driver.get('https://zaka-zaka.com/profile/auth')
        wait = WebDriverWait(self.driver, 180)
        recaptchaSolver.solveCaptcha()

        input_login = wait.until(EC.presence_of_element_located((By.NAME, 'LoginForm[login]')))
        input_login.send_keys(email)
        input_login.send_keys(Keys.ENTER)
        logger.info("The login has been entered")

        input_password = wait.until(EC.visibility_of_element_located((By.NAME, 'LoginForm[password]')))
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        logger.info("The password has been entered")

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-user-name')))

        CksMngr = CookiesManager(self.driver)
        token, PHPSESSID = CksMngr.collect_cookies()
        CksMngr.save_cookies(token, PHPSESSID)
        logger.info("The authorization has been completed & Cookies have been saved")

        self.driver.quit()
