import asyncio
from playwright.async_api import async_playwright
import psycopg2

IP = '109.172.115.223'
PORT = '5432'
USERNAME = 'postgres'
PASSWORD = 2556505535
DBNAME = 'artists'

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

async def main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        button_exists = await get_button(url=url, page=page)
        
        if button_exists is True:
            await DB().insert(table_name='data', values=(url))
            print(True)

        await browser.close()

for i in range(1, 1000000000):
    id = f'{i:09d}'
    asyncio.run(main(url=f"https://vk.com/public{id}"))





