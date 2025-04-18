from validating.ValidateFiles import Validator
from giveaway.Participation import Participation
from authorization.AuthManager import AuthManager

import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


def main():
    v = Validator()
    v.validate_env_file()

    p = Participation()
    if p.load_cookies() != 'FileNotFoundError':
        if p.enter_the_giveaway() != 'CSRF ERROR':
            p.scheduling()
        else:
            login_and_participate(p, email, password)
    else:
        login_and_participate(p, email, password)


def login_and_participate(p, email, password):
    auth = AuthManager()
    auth.login_via_pass(email, password)
    p.load_cookies()
    p.enter_the_giveaway()
    p.scheduling()


if __name__ == '__main__':
    main()
