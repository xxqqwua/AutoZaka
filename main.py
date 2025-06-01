from validating.Validator import Validator
from giveaway.Participation import Participation
from authorization.AuthManager import AuthManager
import logging
import tray.Tray

import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


def main():
    logging.info("App started")
    v = Validator()
    v.validate_ffmpeg()
    data = v.validate_env_file()

    p = Participation()
    email = data[0]; password = data[1]
    if p.load_cookies() != 'FileNotFoundError' or p.load_cookies() != 'JSONDecodeError':
        if p.enter_the_giveaway() != 'CSRF ERROR':
            p.scheduling()
        else:
            login_and_participate(p, email, password)
    else:
        login_and_participate(p, email, password)


def login_and_participate(p, email, password):
    auth = AuthManager()
    auth.login_via_pass(email, password)
    p.enter_the_giveaway()
    p.scheduling()


if __name__ == '__main__':
    import logging
    from logging_config import LOGGING_CONFIG

    logging.config.dictConfig(LOGGING_CONFIG)

    main()
