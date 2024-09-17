import asyncio
from playwright.async_api import async_playwright
import psycopg2
import requests

TOKEN = "7416958256:AAGxXCgIh7Zp6Bd4g3QUkcHcaFklWV1UBhg"
CHAT_ID = 1043507721
IP = '109.172.115.223'
PORT = '5432'

USERNAME = 'postgres'
PASSWORD = '2556505535'
DBNAME = 'artists'

URL = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'

class Telegram:
    @classmethod
    def send(cls, message):
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
        }
        response = requests.post(URL, data=payload)
        return response

class DB:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(dbname=DBNAME, user=USERNAME, password=PASSWORD, host=IP, port=PORT)
        self.cursor = self.conn.cursor()

    async def insert(self, table_name, values):
        if not isinstance(values, tuple):
            values = (values,)
        self.cursor.execute(f'INSERT INTO {table_name} (url) VALUES (%s)', values)
        self.conn.commit()

async def get_button(page, url):
    await page.goto(url)
    btn = await page.evaluate('''() => {
        return document.querySelector('.page_block .PageActionCell.PageActionCell--md-accent.PageActionCell--standalone') !== null;
    }''')
    return btn

async def main(url, id):
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            button_exists = await get_button(url=url, page=page)
            
            if button_exists:
                await DB().insert(table_name='data', values=url)
                print(f"ID {id}: Button exists")
            else:
                print(f"ID {id}: Button does not exist")

            await browser.close()
        except Exception as e:
            error_message = f"Error for ID {id}: {str(e)}"
            Telegram.send(error_message)
            print(error_message)

for i in range(6206, 1000000000):
    id = f'{i:09d}'
    print(f"Processing ID: {id}")
    Telegram.send(f"Processing ID: {id}")
    asyncio.run(main(url=f"https://vk.com/public{id}", id=id))
