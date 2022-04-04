#!sgertrud/bin/python3
import sys
from time import sleep
from bs4 import BeautifulSoup
import requests as requests


def main(args):
    if len(args) != 3:
        raise AttributeError("Usage: ./financial.py 'MSFT' 'Total Revenue'")
    ticker, table_field = args[1], args[2]
    url = f"https://finance.yahoo.com/quote/{ticker.lower()}/financials"
    resp = requests.get(url, headers={'User-Agent': 'sgertrud'})
    if not resp.ok:
        raise ConnectionError("No result found")
    soap = BeautifulSoup(resp.text, 'html.parser')
    rows = soap.findAll('div', {'data-test': "fin-row"})
    try:
        row = next(filter(lambda x: x.find(class_='Va(m)').get_text().lower() == table_field.lower(), rows))
    except:
        raise KeyError(f"No such field '{table_field}'")
    elems = row.find_all('span')
    sleep(5)
    return tuple(map(lambda x: x.get_text(), elems))


if __name__ == '__main__':
    print(main(sys.argv))
