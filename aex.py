import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_koers():
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = HTMLSession()
    page = session.get('https://beurs.fd.nl/aandelen/amsterdam/aex/')
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find('div', class_="DetailsPriceLine fAr18 pb10").find_all('span')
    values = [span.get_text(strip=True) for span in result]
    values[2] = values[2][:6]
    return values

def get_chart():

    image_url = "https://charting.vwdservices.com/TChart/tchartcached.aspx?user=FD&width=500&height=500&format=image/png&enddate=today&culture=nl-NL&startdate=today&issue=12272&layout=2012.share&res=intraday&showhighlow=true"
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open("image.png", "wb") as f:
            f.write(response.content)
        # print("Download successful")
        return True
    else:
        # print("Failed to download image:", response.status_code)
        return False

def get_winners_losers():
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = HTMLSession()
    page = session.get('https://beurs.fd.nl/aandelen/amsterdam/aex/')
    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find_all('tr', class_="fAr11 bottomDivider topDivider quoteLine")
    stocks = list()
    for tr in results:
        title = tr.find("a")
        if title != None:
            title = title.text.strip()
            subs = tr.find_all("td")
            infolist = list()
            for sub in subs:
                infolist.append(sub.text.strip())
            stocks.append(infolist)
            infolist.append(infolist[4][:-1])
            if infolist[9][0] == '+':
                infolist[9] = infolist[9][1:]
            infolist[9] = float(infolist[9].replace(',', '.'))

    stocks = sorted(stocks, key=lambda x: x[9])
    # for i in stocks:
    #     print(i[9])
    # for i in stocks[:3]:
    #     print(i)
    # for i in stocks[-3:]:
    #     print(i)
    return stocks
        