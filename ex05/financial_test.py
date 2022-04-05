#!sgertrud/bin/python3
import sys
from bs4 import BeautifulSoup
import requests as requests
import pytest


def financial(ticker, table_field):
    url = f"https://finance.yahoo.com/quote/{ticker.lower()}/financials"
    resp = requests.get(url, headers={'User-Agent': 'sgertrud'})
    if not resp.ok or resp.url != url:
        raise ConnectionError("No result found")
    soap = BeautifulSoup(resp.text, 'html.parser')
    rows = soap.findAll('div', {'data-test': "fin-row"})
    try:
        row = next(filter(lambda x: x.find(class_='Va(m)').get_text().lower() == table_field.lower(), rows))
    except:
        raise KeyError(f"No such field '{table_field}'")
    elems = row.find_all('span')
    return tuple(map(lambda x: x.get_text(), elems))

def main(args):
    if len(args) != 3:
        raise AttributeError("Usage: ./financial.py 'MSFT' 'Total Revenue'")
    financial(args[1], args[2])


def test_table_field():
    data = financial('msft', 'total revenue')
    assert data[0].lower() == 'total revenue'

def test_table_field_error():
    with pytest.raises(KeyError, match=f"No such field 'not existing field'"):
        financial('msft', 'not existing field')

def test_table_ticker_error():
    with pytest.raises(ConnectionError, match="No result found"):
        financial('not existing ticket', 'total revenue')
def test_type():
    assert isinstance(financial('msft', 'total revenue'), tuple)

if __name__ == '__main__':
    print(main(sys.argv))

# ../sgertrud/bin/python -m pytest