import sys
def find_company(a, COMPANIES):
    s = ''
    for key, value in COMPANIES.items():
        if value == a:
            s = key

            break
    return s

def find_answer(lst):
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

    ans = ''
    for i in lst:
        k = i.strip()
        if k == '': 
            return
        if k.title() in COMPANIES.keys():
            ans += f'{k.title()} stock price is {STOCKS[COMPANIES[k.title()].upper()]}\n'
        elif find_company(k.upper(), COMPANIES) != '':
            ans += f'{k.upper()} is a ticker symbol for {find_company(k.upper(), COMPANIES)}\n'
        else:
            ans += f'{k} is an unknown company or an unknown ticker symbol\n'
    return ans

def process():
    inp = sys.argv
    if len(inp)!=2:
        return 
    
    s = inp[1]
    lst = s.split(',')
    if find_answer(lst) == None: 
        return
    else:
        ans = find_answer(lst)
    print(ans[:-1])

if __name__ == '__main__':
    process()