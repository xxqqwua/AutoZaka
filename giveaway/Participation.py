import schedule
import requests
import logging
import time
import json


class Participation:
    def __init__(self):
        self.YII_CSRF_TOKEN = None
        self.PHPSESSID = None

        self.cookies = {
            'PHPSESSID': self.PHPSESSID,
            'curr': 'wmu',
            'agent_id': None,
            'deduplication_cookie': 'admitad'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://zaka-zaka.com',
            'Alt-Used': 'zaka-zaka.com',
            'Connection': 'keep-alive',
            'Referer': 'https://zaka-zaka.com/game/gifts/random-steam/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0'
        }

    def load_cookies(self):
        try:
            with open('cookies.json', 'r') as f:
                data = json.load(f)

            self.YII_CSRF_TOKEN = data['YII_CSRF_TOKEN']
            self.PHPSESSID = data['PHPSESSID']
            self.cookies['PHPSESSID'] = data['PHPSESSID']
        except FileNotFoundError:
            return 'FileNotFoundError'

    def enter_the_giveaway(self, interval=1.5, ga_type=None):
        def do_enter(ga_type):
            data = {
                'type': ga_type,
                'YII_CSRF_TOKEN': self.YII_CSRF_TOKEN
            }

            r = requests.post('https://zaka-zaka.com/game/gifts/ajax/', cookies=self.cookies, headers=self.headers,
                              data=data)

            if 'сайта' in r.text or ':E' in r.text:
                return 'CSRF ERROR'

            if '{"code":304}' in r.text:
                logging.info(f"There's already been a drawing for the {'steam random key' if ga_type == '1' else 'random game' if ga_type == '4' else 'coupons' if ga_type == '5' else 'vip'}")
            else:
                logging.info(
                    f"The giveaway for {'steam random key' if ga_type == '1' else 'random game' if ga_type == '4' else 'coupons' if ga_type == '5' else 'vip'} has been entered")
            logging.debug(r.text)

        if ga_type is not None:
            do_enter(ga_type)
        else:
            for giveaway_type in ['1', '4', '5']:
                time.sleep(interval)
                do_enter(giveaway_type)

    def scheduling(self):
        """
        steam: 23:00, 13:00, 17:00
        game: 20:00
        coupons: 20:00
        vip: 21:00

        type 1 - steam
        type 4 - random game
        type 5 - coupons
        type 2 - vip
        """
        logging.info('Scheduling started')

        schedule.every().day.at('23:05', tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=1))
        schedule.every().day.at('13:05', tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=1))
        schedule.every().day.at('17:05', tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=1))
        schedule.every().day.at('21:05', tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=1))

        schedule.every().day.at("20:05", tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=4))

        schedule.every().day.at("20:06", tz='Europe/Sofia').do(lambda: self.enter_the_giveaway(ga_type=5))

        while True:
            schedule.run_pending()
            time.sleep(1)
