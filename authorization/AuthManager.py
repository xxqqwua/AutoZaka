from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthManager:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.driver = webdriver.Chrome(options=self.options)

    def login_via_pass(self, email, password):
        from authorization.RecaptchaSolver import RecaptchaSolver
        recaptchaSolver = RecaptchaSolver(self.driver)

        self.driver.get('https://zaka-zaka.com/profile/auth')
        wait = WebDriverWait(self.driver, 180)
        recaptchaSolver.solveCaptcha()

        input_login = wait.until(EC.presence_of_element_located((By.NAME, 'LoginForm[login]')))
        input_login.send_keys(email)
        input_login.send_keys(Keys.ENTER)

        input_password = wait.until(EC.visibility_of_element_located((By.NAME, 'LoginForm[password]')))
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-user-name')))

        from authorization.CookiesManager import CookiesManager
        CksMngr = CookiesManager(self.driver)
        token, PHPSESSID = CksMngr.collect_cookies()
        CksMngr.save_cookies(token, PHPSESSID)

        self.driver.quit()
