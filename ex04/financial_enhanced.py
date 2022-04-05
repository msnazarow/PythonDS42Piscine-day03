#!sgertrud/bin/python3
import asyncio
import sys
from bs4 import BeautifulSoup
import aiohttp


async def main(args):
    if len(args) != 3:
        raise AttributeError("Usage: ./financial.py 'MSFT' 'Total Revenue'")
    ticker, table_field = args[1], args[2]
    url = f"https://finance.yahoo.com/quote/{ticker.lower()}/financials"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'sgertrud'}) as resp:
            if not resp.ok:
                raise ConnectionError("No result found")
            data = await resp.text()
            soap = BeautifulSoup(data, 'html.parser')
            rows = soap.findAll('div', {'data-test': "fin-row"})
            try:
                row = next(filter(lambda x: x.find(class_='Va(m)').get_text().lower() == table_field.lower(), rows))
            except:
                raise KeyError(f"No such field '{table_field}'")
            elems = row.find_all('span')
            print(tuple(map(lambda x: x.get_text(), elems)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
