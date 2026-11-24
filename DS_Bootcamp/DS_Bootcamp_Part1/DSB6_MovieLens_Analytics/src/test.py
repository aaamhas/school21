import requests
from bs4 import BeautifulSoup

url = "https://www.themoviedb.org/movie/862"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
r = requests.get(url, headers=headers)
print(r.status_code)
print(len(r.text))
soup = BeautifulSoup(r.text, "html.parser")
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(r.text)