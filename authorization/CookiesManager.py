class CookiesManager:
    def __init__(self, driver):
        self.driver = driver

    def collect_cookies(self):
        script = """
            var token = window.token;
            return token;
        """

        token = self.driver.execute_script(script)

        cookies = self.driver.get_cookies()
        PHPSESSID = None

        for cookie in cookies:
            if cookie["name"] == "PHPSESSID":  # For the cookie program to work, we only need PHPSESSID
                PHPSESSID = cookie["value"]
                break

        return token, PHPSESSID

    def save_cookies(self, token, PHPSESSID):  # Save cookies function
        import json

        data = {'TOKEN': str(token), 'PHPSESSID': str(PHPSESSID)}
        with open('cookies.json', 'w') as f:
            json.dump(data, f)
