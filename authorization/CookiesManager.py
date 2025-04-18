import logging

logger = logging.getLogger(__name__)


class CookiesManager:
    def __init__(self, driver):
        self.driver = driver

    def collect_cookies(self):
        script = """
            var token = window.token;
            return token;
        """

        token = self.driver.execute_script(script)
        logger.info("The token has been collected")

        cookies = self.driver.get_cookies()
        phpsessid = None

        for cookie in cookies:
            if cookie["name"] == "PHPSESSID":  # For the cookie program to work, we only need PHPSESSID
                phpsessid = cookie["value"]
                break
        logger.info("The phpsessid has been collected")

        return token, phpsessid

    @staticmethod
    def save_cookies(token, phpsessid):  # Save cookies function
        import json

        data = {'YII_CSRF_TOKEN': str(token), 'PHPSESSID': str(phpsessid)}
        with open('cookies.json', 'w') as f:
            json.dump(data, f)
