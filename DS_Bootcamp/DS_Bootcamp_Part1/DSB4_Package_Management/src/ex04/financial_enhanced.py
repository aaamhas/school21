#!/usr/bin/env python3
import sys
import httpx
from bs4 import BeautifulSoup
import time

def get_args():
    s = sys.argv
    if len(s) != 3:
        raise ValueError
    ticker = s[1]
    field = s[2]
    return ticker, field

def get_response(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker}'
    response = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    return response

def get_soup(field, response):
    soup = BeautifulSoup(response.text, 'html.parser')

    any_row = soup.find('div', class_='rowTitle')
    if any_row is None:
        raise ValueError("URL doesn't exist")

    row_title = soup.find('div', class_='rowTitle', attrs = {'title': field})
    if row_title is None:
        raise ValueError(f"Field '{field}' not found")
    
    return row_title

def get_ans(row_title, field):
    row = row_title.parent.parent
    columns = row.find_all('div', class_ = 'column')
    values = [i for i in columns if 'sticky' not in i.get('class')]
    ans = [field]
    for i in values:
        ans.append(i.get_text().strip())
    ans = tuple(ans)
    return ans

def main():
    ticker, field = get_args()
    response = get_response(ticker)
    row_title = get_soup(field, response)
    ans = get_ans(row_title, field)
    print(ans)

if __name__ == '__main__':
    main()

