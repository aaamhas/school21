import sys


def find_price(a):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    if a not in COMPANIES:
        return "Unknown company"
    return STOCKS[COMPANIES[a]]


def process():
    inp = sys.argv
    if len(inp) != 2:
        return
    print(find_price(inp[1].title()))

if __name__ == '__main__':
    process()