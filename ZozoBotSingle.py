import re
import requests
import concurrent.futures

from bs4 import BeautifulSoup
from parsel import Selector
from time import sleep
from seleniumwire import webdriver

time_delay = 0.1
proxies = [
    # {"http": "http://iyr001010:i9h2zuy@140.227.27.15:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.27.15:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.60.90:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.60.90:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.61.17:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.61.17:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.62.232:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.62.232:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.63.87:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.63.87:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.79.190:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.79.190:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@140.227.81.232:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.227.81.232:3128"
    #  },
    {"http": "http://iyr001010:i9h2zuy@157.65.171.220:3128",
     "https": "http://iyr001010:i9h2zuy@157.65.171.220:3128"
     },
    # {"http": "http://iyr001010:i9h2zuy@140.150.121.218:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.150.121.218:3128"
    #  },
    # {"http": "http://iyr001010:i9h2zuy@210.150.121.218:3128",
    #  "https": "http://iyr001010:i9h2zuy@140.150.121.218:3128"
    #  }
]
target_link = None
query = 'ナイキ SB ズーム ブレーザー MID エッジ スケ'
start_link_nike = "https://zozo.jp/shop/nike/?dord=21&dstk=2"
start_link_atmos = "https://zozo.jp/shop/atmos/shoes/sneakers/?dord=21&dstk=2"
start_link_atmospink = "https://zozo.jp/shop/atmospink/?dord=21&dstk=2"
start_link_mct = "https://zozo.jp/search/?p_keyv=be%40rbrick&dord=21&dstk=2"
seckey = '3009445799cda4b7a6e1f95015ef9c07'
print(f"Query = {query}")
print(f"Start link = {start_link_nike}")
xpath_query = "//img[contains(@alt,'swaphere')]/parent::div/parent::figure/parent::a/@href"
xpath_query = xpath_query.replace('swaphere', query)
cookies = {
    'generation': '0',
    'ZOZO%5FISMEN': '0',
    'ZOZO%5FUID': 'P9206%3A556017144%3A667378465',
    'ASPSESSIONIDSCRATRTB': 'IPFCECBCAKAMACFIDGKMBBBE',
    'BIGipServerIN01_zozo.jp_global_Pool': '3458013194.20480.0000',
    'TS014ab708': '0182a26047e056c5aa3c2abf454639c4854318afbfc85c920be5ad2dc0fdd64bf745bb88a996be40e66b572ab2a8e4e3ce41a11f69',
    'optimizelyEndUserId': 'oeu1614031017725r0.43417870490768373',
    '_gcl_au': '1.1.552387246.1614031025',
    '_ga': 'GA1.2.1451758489.1614031025',
    'krt.vis': '138eef77-bfb1-406f-b78f-e44d89f7b41b',
    'showedBalloon': '1',
    '__lt__cid': '79ae0cb0-c103-4b36-b534-5096de561b8e',
    '_fbp': 'fb.1.1614031030203.525342562',
    'isDisplayedRankingPopover': '1',
    'ASPSESSIONIDSCSCTSRA': 'NMDBDEBCFNJHCDAOICOFIANB',
    'ss_uid': '177cbc63007_325d935c-b961-422d-b167-d166f07d08c6',
    'ASPSESSIONIDQCRARQTB': 'FLAIOPBANEOHPLBGILNLIJAP',
    'ASPSESSIONIDQARCSQSB': 'AJGNBAGAPPIDOCOEDNODGIAH',
    'ASPSESSIONIDQCQBTQSB': 'IFGENEFANEIMPMNACFIDIMLL',
    '_gid': 'GA1.2.1214857235.1614882451',
    'imdid': '',
    'ASPSESSIONIDQCQASQSA': 'FKOPCKJALLGDGOHIONNKEINF',
    'ASPSESSIONIDQAQBTRSB': 'LJPAJOOAGNJBIEAKIOJGABKJ',
    'bm_sz': '51AEDD876461FDBEC9FEBF6D3C8CDD36~YAAQF54QAoB15NN3AQAAsJALAwu9z56XrvtZipsx+07uZ5vR40Vq3LIkuXuTcHLlA3T9Bvp00qjIZBXZ7hcQOTkEh2VPaR5UkdWiOMdLVD6clwP7eNcfwSdzXIIIV4oRp2pJqUtlCmKzln7cqxRFeHQpNJNZzIoMVyuIOtYX5rzovzBsIMBwC7lkFfF4',
    'goods%5Fhistory': '%2C55271018%2C53859099%2C',
    'TS014d8e6a': '0182a26047e2d9a525f30792ca524c14e6dd3f7a05cd35575fc413b1ab90998a0857419e5923ba593e63afdb02e15814c4dccde7e2',
    'ak_bmsc': '7E47DBD010535BC3D5BE723FC026DAE302109E170F5F0000267342603C304470~pl5kXKovgULF7FP0kOnW14WB/hcA57LQ9RGxtao+88jD+2evJdMHgW0sBLqo7UiQJJ94HwiVfnym/S9SEaXKxLD6jpo6Ad3nXaSe61nVwmpYLLe14laKdNa6BN1AFzq/btPGy2Ls7N8RjUu3hWXseBdIyIV5pdd+/l9aDCaxqFo9u6IUOhkdUQNbnEYU6tIjwc8et6vg0AeLE7fTlX7flq1t5Nu58a4/YibwI5MWLQ+EUrSjQGjTMIexuBlSN3YKUf',
    'ss_sid': '17803943f1c_ef2912d8-205e-497e-973f-0642708d87dd',
    '__lt__sid': '20a74694-c41539ac',
    '_im_ses.1001058': '1',
    'goods%5Fhistory%5Fcart': '89352865%2C91803913',
    '_abck': '48755E9CE75F766C4FC1AE132CDA8CCF~0~YAAQF54QAmu25NN3AQAAeTWTAwXZ0xdF/jQrQUhSR17xEbwz28X7uH5vIYObfD9cx9vr6JSyWgf3TQGehsavYclg2BQh/sRrmp1nWK8R5PVt6wOjRjZnlBKJ6/gYaZcvLShbfz4P1UeqJrNFuqeaCym2WPhwxjgbore/BMMZRPmB6MtIyWThme4Ivv5//7rSJUm+zRNsY/GXS5aB8RKaFYF2INaVhQNhjo6uHndy8TRYRnmIbvaM8a1YTuAcGKQiJXTDoI6KgPNsnXMI+bMRNZqsLnygHq54OJZ0td3koEM5bfJ9jkwaU1+vm8sMQuB/UqytsNd4H8y+zVXcnlFD2p76yRKTsIlX+GgeAkyBbqxBDcjIGB47KsTJoZE61XLYul6O9A/1iAOHZr+nbBRlSZNtoFw6~-1~-1~-1',
    '_im_id.1001058': '9a66531054f945d4.1614306575.8.1614967856.1614967757.',
    'krt.context': 'session%3A4267639a-55f1-466a-9d56-8929caaf5d25%3Bcontext_mode%3Acomparing',
    'trackingOfAddToCartForRecommendations': '55271018-156',
    'RT': '\\z=1&dm=zozo.jp&si=d8d0f826-1ac3-49b8-a753-3fe4b6bb1da8&ss=klwm3fsz&sl=6&tt=vs8&bcn=%2F%2F684fc53b.akstat.io%2F&ld=2eko&nu=0bd23a0aea5cc26aca0910d18343829e&cl=3rmm&ul=3rni\\',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '\\Google',
    'sec-ch-ua-mobile': '?0',
    'Origin': 'https://zozo.jp',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://zozo.jp/shop/nike/goods/55271018/?did=91803826',
    'Accept-Language': 'en-US,en;q=0.9',
}

headers_dic = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
}


def start(proxies):
    add_to_cart(proxies[0])
    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as executor:
    #     executor.map(add_to_cart, proxies)


def add_to_cart(proxy):
    proxies = proxy
    counter = 0
    while True:
        if counter >= 1:
            break
        counter += 1
        if not target_link:
            response = requests.get(start_link_nike, proxies=proxies, headers=headers_dic)
            response.encoding = response.apparent_encoding
            print(f"Zozo response: {response.status_code}")
            # print(response.text)
            link = None
            soup = BeautifulSoup(response.text, 'lxml')
            for a in soup.findAll("a", {"class": "catalog-link"}):
                if query in str(a):
                    link = a['href']
                    break
            # response = Selector(text=response.text)
            # link = response.xpath(xpath_query).extract_first()
            if link:
                link = f'https://zozo.jp{link}'
                print(f"Item: {query}, link found: {link}")
                response = requests.get(link, proxies=proxies, headers=headers_dic)
                # response = requests.get(f"{link}",proxies=proxies) #this line is taking time this time is taken by server the rest take seconds
                # https://zozo.jp/shop/medicomtoy/goods/54494701/?did=90518895
                print(f"Zozo response for item {query}:", response.status_code)
                response.encoding = response.apparent_encoding
                sid = None
                rid = None
                soup = BeautifulSoup(response.text, 'lxml')
                for cart in soup.findAll("div", {"class": "cartbox"}):
                    if 'sold out' not in str(cart):  # If sold out is found, the item is out of stock
                        # sid_names = [sid['name'] for sid in cart.findAll('input')]
                        sid_values = [sid['value'] for sid in cart.findAll('input')]
                        print(f"Inputs: {cart.findAll('input')}")
                        print(f"SIDs: {sid_values}")
                        sid = sid_values[1]
                        rid = sid_values[2]
                        # seckey = sid_values[3]
                        break
                if sid or seckey or rid:
                    print(f"Adding item {query} to cart")
                    # 'Referer': f'{link}',
                    data = {
                        'c': 'put',
                        'sid': f'{str(sid)}',
                        'rid': f'{str(rid)}',
                        'p_seckey': f'{str(seckey)}'
                    }
                    # params = (
                    #     ('c', 'Message'),
                    #     ('no', '1'),
                    #     ('name', 'PutMessage'),
                    # )
                    response = requests.post('https://zozo.jp/_cart/default.html', headers=headers, cookies=cookies,
                                             data=data, proxies=proxies)
                    print(f"item {query} has been added to cart | response {response.status_code}")
                    break
                else:
                    print(f"Item {query} is out of stock")
            else:
                print(f"Item {query} was not found")
        else:
            response = requests.get(target_link, proxies=proxies, headers=headers_dic)
            response.encoding = response.apparent_encoding
            print(f"Zoho Responded for  {query}", response.status_code)
            response = Selector(text=response.text)
            # response = requests.get(f"{link}",proxies=proxies) #this line is taking time this time is taken by server the rest take seconds
            # https://zozo.jp/shop/medicomtoy/goods/54494701/?did=90518895
            sid = response.xpath("//div[@class='cartbox']//form//input[@name='sid']/@value").extract_first()
            rid = response.xpath("//div[@class='cartbox']//form//input[@name='rid']/@value").extract_first()
            # for data in response.css(".blockMain li.clearfix"):

            #     if data.css('input[value="カートへ入れる"]'):
            #         sid = data.css("input[name='sid']::attr(value)").extract_first()
            #         rid = data.css("input[name='rid']::attr(value)").extract_first()
            #         break
            if sid or seckey or rid:
                print(f"Adding item {query} to cart")
                # 'Referer': f'{link}',
                data = {
                    'c': 'put',
                    'sid': f'{str(sid)}',
                    'rid': f'{str(rid)}',
                    'p_seckey': f'{str(seckey)}'
                }
                response = requests.post('https://zozo.jp/_cart/default.html', headers=headers, cookies=cookies,
                                         data=data, proxies=proxies)
                print(f"Item {query} has been added to cart | response {response}")
                break
            else:
                print(f"Item {query} is out of stock")
        sleep(time_delay)


start(proxies)
