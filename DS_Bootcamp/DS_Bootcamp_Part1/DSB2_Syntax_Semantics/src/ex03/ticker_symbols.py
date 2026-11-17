import sys

def outp(a):

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
    s = ''
    for key, value in COMPANIES.items():
        if value == a:
            s = key

            break
    if s == '':
        return "Unknown ticker"
    return f'{s} {STOCKS[a]}'

def process():
    inp = sys.argv
    if len(inp) != 2:
        return
    print(outp(inp[1].upper()))
    

if __name__ == '__main__':
    process()
 