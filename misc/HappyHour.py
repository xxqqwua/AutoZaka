import asyncio
import re
from datetime import datetime

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup as Bs

from misc.SteamGamePriceParser import SteamGamePriceParser


def extract_price(amount):
    match = re.search(r"-?\d+", amount)
    if match:
        return int(match.group())
    else:
        return 0


async def get_converted_price(amount):
    if isinstance(amount, str):
        amount = extract_price(amount)

    async with aiohttp.ClientSession() as session:
        async with session.get('https://open.er-api.com/v6/latest/RUB') as response:
            data = await response.json()

    uah = str(round((data['rates']['UAH']) * amount, 2))
    usd = str(round((data['rates']['USD']) * amount, 2))
    eur = str(round((data['rates']['EUR']) * amount, 2))

    if uah.endswith('.0'):
        uah = uah[:-2]

    if usd.endswith('.0'):
        usd = usd[:-2]

    if eur.endswith('.0'):
        eur = eur[:-2]

    return uah, usd, eur


class HappyHour:
    def __init__(self):
        self.happy_hour_games = []

    async def extract_happy_hour_games(self):
        s = SteamGamePriceParser()
        steam_price = None

        async with aiohttp.ClientSession() as session:
            async with session.get('https://zaka-zaka.com/happyhour') as response:
                html = await response.text()
                soup = Bs(html, 'html.parser')

        games = soup.find_all("div", class_="happy-hour-table-row")

        for game in games:
            link_tag = game.find("a", class_="happy-hour-table-game")
            if not link_tag:
                continue

            game_link = link_tag.get("href")

            name_tag = link_tag.find("div", class_="game-block-name")
            name = name_tag.text.strip() if name_tag else "Can't find the game name"

            if '(steam)' in name:
                name = name.replace('(steam)', '')

            game_app_id = await s.check_game_app_id_by_name(str(name))
            if game_app_id:
                steam_price = await s.check_game_price(game_app_id, 'ru, ua, us, eu')
            else:
                steam_price = None

            game_tags_tag = link_tag.find("div", class_="game-block-desc")
            game_tags = game_tags_tag.text.strip() if game_tags_tag else "Can't find the game description"

            discount_tag = link_tag.find("div", class_="game-block-discount")
            discount = discount_tag.text.strip() if discount_tag else "Can't find the game discount"

            current_price_tag = link_tag.find("div", class_="game-block-price")
            current_price = current_price_tag.text.strip() if current_price_tag else "Can't find the game current price"

            prices = await get_converted_price(current_price)

            self.happy_hour_games.append({
                'name': name,
                'link': game_link,
                'tags': game_tags,
                'discount': discount,
                'current_price': f'RUB: {current_price[:-2]}, '
                                 f'UAH: {prices[0]}, '
                                 f'USD: {prices[1]}, '
                                 f'EUR: {prices[2]}',
                'steam_price': steam_price,
            })

    async def get_next_happy_hour_start(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.happy_hour_games[0]['link']) as response:
                html = await response.text()
                soup = Bs(html, 'html.parser')

        timer_tag = soup.find("div", class_="timer")
        end_time = int(timer_tag.get("data-end"))  # get UNIX timestamp

        return end_time

    async def schedule_next_happy_hour(self):
        next_happy_hour_start = await self.get_next_happy_hour_start()

        scheduler = AsyncIOScheduler()
        run_time = datetime.fromtimestamp(next_happy_hour_start)

        scheduler.add_job(self.extract_happy_hour_games, 'date', run_date=run_time)
        scheduler.start()

        while True:
            await asyncio.sleep(1)
