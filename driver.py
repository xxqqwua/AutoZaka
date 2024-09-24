# import necessary modules
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import custom modules
from config import read_login_n_pass
from RecaptchaSolver import RecaptchaSolver

# set up chrome options
options = Options()
options.add_argument("start-maximized")
options.add_argument("--mute-audio")
options.add_argument("--headless=new")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
recaptchaSolver = RecaptchaSolver(driver)

# read login and password from config file
config = read_login_n_pass()
LOGIN = config[0]
PASSWORD = config[1]

# set up stealth
stealth(
    driver,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

def auth():
    # delete all cookies and navigate to zaka-zaka.com/profile
    driver.delete_all_cookies()
    driver.get("https://zaka-zaka.com/profile")
    driver.execute_script("window.localStorage.clear();")

    time.sleep(4)

    # enter login
    login = wait.until(EC.presence_of_element_located((By.NAME, "LoginForm[login]")))
    login.clear()
    login.send_keys(LOGIN)

    try:
        recaptchaSolver.solveCaptcha()  # solve recaptcha
        login.send_keys(Keys.ENTER)  # enter login and password
    except Exception as e:
        print(f"An error occurred: {e}")  # print error message
        driver.quit()

    # enter password
    password = wait.until(EC.visibility_of_element_located((By.NAME, "LoginForm[password]")))
    password.clear()
    password.send_keys(PASSWORD)
    password.send_keys(Keys.ENTER)


    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "profile-user-name")))  # wait for profile page to load
    driver.refresh()  # refresh page to get new token


    token = driver.execute_script("return window.token;")  # get token
    cookies = driver.get_cookies()  # get cookies
    filtered_cookies = [cookie for cookie in cookies if not cookie['name'].startswith('_')]  # filter cookies
    cookie_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in filtered_cookies])


    # write cookie string and token to config file
    with open('config.txt', "a") as c:
        c.write(f"\nCOOKIE={cookie_string}\nYII_CSRF_TOKEN={token}\n")

    # close browser
    driver.quit()
