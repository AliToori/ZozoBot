#!/usr/bin/env python3
"""
    *******************************************************************************************
    ZozoBot.
    Author: Ali Toori, Python Developer [Bot Builder]
    LinkedIn: https://www.linkedin.com/in/alitoori/
    *******************************************************************************************
"""
import datetime
import logging.config
import os
import pickle
import time
from multiprocessing import freeze_support
from pathlib import Path
from time import sleep
import ntplib
import pandas as pd
import pyfiglet
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',  # colored output
            # --> %(log_color)s is very important, that's what colors the line
            'format': '[%(asctime)s] %(log_color)s%(message)s'
        },
    },
    "handlers": {
        "console": {
            "class": "colorlog.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

LOGGER = logging.getLogger()

INSTA_HOME_URL = "https://www.instagram.com/"
INSTA_SEARCH_URL = "https://www.instagram.com/explore/"
driver = None
stop = False


class ZozoBot:

    def __init__(self):
        self.PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.PROJECT_ROOT = Path(self.PROJECT_ROOT)

    # Get cookies
    def get_cookies(self, account_num):
        cookies_path = f'ZozoRes/cookies{account_num}.txt'
        file_cookies = str(self.PROJECT_ROOT / cookies_path)
        with open(file_cookies) as f:
            content = f.read().strip()
        return content

    # Get headers
    def get_headers(self, account_num):
        headers_path = f'ZozoRes/headers{account_num}.txt'
        file_cookies = str(self.PROJECT_ROOT / headers_path)
        with open(file_cookies) as f:
            content = f.read().strip()
        return content

    # Get user-agent
    def get_user_agent(self):
        file_uagents = str(self.PROJECT_ROOT / 'ZozoRes/user_agent.txt')
        with open(file_uagents) as f:
            content = f.read().strip()
        return content

    # Get seckey
    def get_sec_key(self):
        file_uagents = str(self.PROJECT_ROOT / 'ZozoRes/SecKey.txt')
        with open(file_uagents) as f:
            content = f.read().strip()
        return content

    # Get time delay
    def get_time_delay(self):
        file_uagents = str(self.PROJECT_ROOT / 'ZozoRes/TimeDelay.txt')
        with open(file_uagents) as f:
            content = f.read().strip()
        return content

    # Get driver with proxy and user-agent
    def get_proxy_driver(self, proxy, account_num, headless=False):
        LOGGER.info("--------------------------------------------------")
        LOGGER.info("Starting Proxy browser:" + ' Account No.' + str(account_num))
        DRIVER_BIN = str(self.PROJECT_ROOT / "ZozoRes/bin/chromedriver_win32.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server={}".format(proxy))
        options.add_argument("--start-maximized")
        options.add_argument(f'--user-agent={self.get_user_agent()}')
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        if headless:
            options.add_argument("--headless")
        proxy_driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options, service_log_path=os.devnull)
        LOGGER.info("--------------------------------------------------")
        return proxy_driver

    # Login to the website
    def login_zozo(self, driver, account):
        account_num = str(account["AccountNo"])
        email = account["Email"]
        password = account["Password"]
        LOGGER.info(f'[ZozoBot launched][Account {account_num}: {email}]')
        LOGGER.info(f'[Signing-in to the Instagram][Account {account_num}: {email}]')
        cookies = 'Cookies' + str(account_num) + '.pkl'
        FILE_PATH = str(self.PROJECT_ROOT / 'ZozoRes' / cookies)
        if os.path.isfile(FILE_PATH):
            LOGGER.info(f"[Requesting Zozo: {str(INSTA_HOME_URL)}][Account {account_num}: {email}]")
            driver.get(INSTA_HOME_URL)
            # try:
            LOGGER.info( f"[Loading cookies ...][Account {account_num}: {email}]")
            with open(FILE_PATH, 'rb') as cookies_file:
                cookies = pickle.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.get(INSTA_HOME_URL)
            try:
                LOGGER.info(f"[Waiting for Instagram profile to become visible][Account {str(account_num)}: {str(email)}]")
                self.wait_until_visible(driver=driver, xpath='//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[5]/a')
                LOGGER.info(f"[Profile has been visible][Account {account_num}: {email}]")
                LOGGER.info(f"[Cookies login successful][Account {account_num}: {email}]")
                return
            except WebDriverException as ec:
                LOGGER.info(f"[Cookies login failed][Account {account_num}: {email}]")
                os.remove(FILE_PATH)
                pass
        # # If no cookies or cookies login failed, try logging-in normally
        # file_path_account = self.PROJECT_ROOT / 'ZozoRes/Account.txt'
        # # Get account from input file
        # with open(file_path_account) as f:
        #     content = f.readlines()
        # account = [x.strip() for x in content[0].split(':')]
        LOGGER.info(f"[Requesting: {str(INSTA_HOME_URL)}][Email: {email}]")
        driver.get(INSTA_HOME_URL)
        # Try clicking login button
        try:
            LOGGER.info(f"[Waiting for login button to become visible][Account {str(account_num)}: {str(email)}]")
            self.wait_until_visible(driver=driver, xpath='//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button')
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button').click()
            LOGGER.info(f"[Login clicked][Account {str(account_num)}: {str(email)}]")
        except WebDriverException as ec:
            LOGGER.error(f"[Exception clicking login button][Account {str(account_num)}: {str(email)}]: " + str(ec.msg))
            LOGGER.info(f"[Waiting for login button to become visible][Account {str(account_num)}: {str(email)}]")
            self.wait_until_visible(driver=driver, tag_name='button')
            driver.find_element_by_tag_name('button').click()
            LOGGER.info(f"[Login clicked][Account {str(account_num)}: {str(email)}]")
        # Try logging-in
        try:
            LOGGER.info(f"[Waiting for login fields to become visible][Account {str(account_num)}: {str(email)}]")
            self.wait_until_visible(driver=driver, name='username')
            # Filling login fields
            LOGGER.info(f"[Filling username:][Account {str(account_num)}: {str(email)}]")
            email_input = driver.find_element_by_name('username')
            email_input.send_keys(email)
            LOGGER.info(f"[Filling password: ][Account {str(account_num)}: {str(email)}]")
            password_input = driver.find_element_by_name('password')
            password_input.send_keys(password)
            LOGGER.info(f"[Signing in][Account {str(account_num)}: {str(email)}]")
            # Clicking button login
            driver.find_element_by_id('loginForm').find_elements_by_tag_name('button')[2].click()
            LOGGER.info(f"[Waiting for Zozo to become visible][Account {str(account_num)}: {str(email)}]")
            self.wait_until_visible(driver=driver, xpath='//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[5]/a')
            LOGGER.info(f"[Profile has been visible][Account {str(account_num)}: {str(email)}]")
            LOGGER.info(f"[Successfully logged in][Account {str(account_num)}: {str(email)}]")
            # Store user cookies for later use
            LOGGER.info(f"[Saving cookies for][Account {str(account_num)}: {str(email)}]")
            with open(FILE_PATH, 'wb') as cookies_file:
                pickle.dump(driver.get_cookies(), cookies_file)
            LOGGER.info(f"Cookies have been saved][Account {str(account_num)}: {str(email)}]")
            return
        except WebDriverException as ec:
            LOGGER.error(f"[Exception while signing-in][Account {str(account_num)}: {str(email)}]:" + str(ec.msg))
            pass

    def grab_cook_header_sec(self, driver, account_num):
        LOGGER.info(f"[Started saving cookies, headers an seckey][Account {str(account_num)}]")
        item_link = None
        for item in driver.find_elements_by_class_name('catalog-item-container'):
            if '在庫なし' not in str(item.text):  # If item is not sold out
                item_link = item.find_element_by_tag_name('a').get_attribute('href')
                break
        driver.get(item_link)
        LOGGER.info(f"[Waiting for cart button to become visible][Account {str(account_num)}]")
        self.wait_until_visible(driver=driver, class_name='cartbox')
        driver.find_element_by_class_name('cartbox').find_element_by_class_name('btn').click()
        LOGGER.info(f"[Wait while item is being added to the cart][Account {str(account_num)}]")
        self.wait_until_visible(driver=driver, class_name='btnDelete')
        LOGGER.info(f"[Item has been added to the cart][Account {str(account_num)}]")
        # for request in driver.requests:
        #     if request.response and request.url == 'https://zozo.jp/_cart/default.html':
        #         print('REQUEST URL:', request.url)
        #         print('STATUS CODE:', request.response.status_code)
        #         print('REQUEST HEADERS:', request.headers)
        #         print('REQUEST SECKEY:', request.params["p_seckey"])
        # Wait for the request/response to complete
        request = driver.wait_for_request('https://zozo.jp/_cart/default.html')
        LOGGER.info(f"[Saving cookies for][Account {str(account_num)}]")
        sec_key = str(request.params["p_seckey"])
        header_dic = {}
        cookies = {}
        for header in request.headers:
            # print('HEADER1:', header)
            # l = str(line.rstrip().split(':', maxsplit=1)).replace('[', '').replace(']', '').replace(',', ':', 1).replace("' ", "'").replace('"', '')
            head = header.rstrip().replace(' ', '', 1).replace('"', '').split(':', maxsplit=1)
            # print('HEAD:', head)
            # key, val = line.strip().split(':')
            try:
                header_dic[head[0]] = head[1]
            except:
                if head[0] == 'Host':
                    header_dic[head[0]] = 'zozo.jp'
        with open(f"cookies{account_num}.txt", 'w') as f:
            cookie = header_dic['Cookie'].strip().replace('; ', ':').split(':')
            for c in cookie:
                cook = c.strip().replace(' ', '', 1).split('=', 1)
                cookies[cook[0]] = cook[1]
                f.writelines(cook[0] + ':' + cook[1])
            # print('COOKIES:', cookies)
        with open(f"headers{account_num}.txt", 'w') as h_file:
            del header_dic['Cookie']
            headers = header_dic
            # print('HEADERS:', headers)
            for key, value in headers.items():
                h_file.writelines(key + ':' + value)
        file_sec = f'ZozoRes/SecKey{account_num}.txt'
        file_sec = str(self.PROJECT_ROOT / file_sec)
        # print('SECKEY:', sec_key)
        with open(file_sec, 'w') as sec_file:
            sec_file.write(sec_key)
        # print('Response Form Data:', request)
        with open(f"cookies3{account_num}.txt", 'w') as cookies_file:
            cookies_file.writelines(driver.get_cookies())
        LOGGER.info(f"Cookies have been saved][Account {str(account_num)}]")
        LOGGER.info(f"Deleting item from the cart][Account {str(account_num)}]")
        driver.find_element_by_class_name('btnDelete').click()
        self.wait_until_visible(driver=driver, css_selector='.gBtn.btnM')
        LOGGER.info(f"[Item has been deleted from the cart][Account {str(account_num)}]")
        return cookies, headers, sec_key

    def wait_until_clickable(self, driver, xpath=None, element_id=None, name=None, class_name=None, tag_name=None, css_selector=None, duration=10000, frequency=0.01):
        if xpath:
            WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elif element_id:
            WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, element_id)))
        elif name:
            WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.NAME, name)))
        elif class_name:
            WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
        elif tag_name:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))
        elif css_selector:
            WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

    def wait_until_visible(self, driver, xpath=None, element_id=None, name=None, class_name=None, tag_name=None, css_selector=None, duration=10000, frequency=0.01):
        if xpath:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        elif element_id:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, element_id)))
        elif name:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.NAME, name)))
        elif class_name:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
        elif tag_name:
            WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))
        elif css_selector:
            WebDriverWait(driver, duration, frequency).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    def add_to_cart(self, account):
        account_num = str(account["AccountNo"])
        email = account["Email"]
        password = account["Password"]
        proxy = account["Proxy"]
        # proxy_user = 'iyr001010'
        # proxy_pass = 'i9h2zuy'
        # seckey = str(account["SecKey"])
        start_link = account["StartLink"]
        target_link = None
        keyword = account["Keyword"]
        # Create and launch proxy browsers
        driver = self.get_proxy_driver(proxy=proxy, account_num=account_num)
        try:
            driver.get(start_link)
            LOGGER.info('Loading ...')
            # sleep(5)
            # pyautogui.typewrite(proxy_user)
            # pyautogui.press('tab')
            # pyautogui.typewrite(proxy_pass)
            # pyautogui.press('enter')
            # LOGGER.info('Proxy Authenticating ...')
            LOGGER.info('Waiting for page to become visible ...')
            self.wait_until_visible(driver=driver, xpath='//*[@id="hLogo"]')
            # while True:
            #     LOGGER.info(f'Please save credentials of each browser in the files')
            #     done = input("Have you saved the credentials? Y/N")
            #     if done == 'y' or done == 'Y':
            #         break
            #     else:
            #         pass

        except WebDriverException as exc:
            LOGGER.info(f'Exception in link:' + exc.msg)
            return False
        headers_dic = {"User-Agent": self.get_user_agent()}
        # cookies = {self.get_cookies(account_num)}
        # headers = {self.get_headers(account_num)}
        # seckey = str(self.get_sec_key())
        time_delay = float(self.get_time_delay())
        # Grab cookies, headers and seckey and save them
        cookies, headers, seckey = self.grab_cook_header_sec(driver=driver, account_num=account_num)
        LOGGER.info(f"Keyword = {keyword}")
        LOGGER.info(f"Start link = {start_link}")
        xpath_query = "//img[contains(@alt,'swaphere')]/parent::div/parent::figure/parent::a/@href"
        xpath_query = xpath_query.replace('swaphere', keyword)
        proxies = {"http": proxy, "https": proxy}
        # counter = 0
        while True:
            # if counter == 3:
            #     break
            # counter += 1
            if not target_link:
                response = requests.get(start_link, proxies=proxies, headers=headers_dic)
                response.encoding = response.apparent_encoding
                LOGGER.info(f"Zozo responded with: {response.status_code}")
                link = None
                soup = BeautifulSoup(response.text, 'lxml')
                for a in soup.findAll("a", {"class": "catalog-link"}):
                    if keyword in str(a):  # If keyword is found inside a tag the we have found the link
                        link = a['href']  # Get the href out of a tag
                        break
                # response = Selector(text=response.text)
                # link = response.xpath(xpath_query).extract_first()
                if link:
                    link = f'https://zozo.jp{link}'
                    LOGGER.info(f"Item {keyword} link found: {link}")
                    response = requests.get(link, proxies=proxies, headers=headers_dic)
                    # response = requests.get(f"{link}",proxies=proxies) #this line is taking time this time is taken by server the rest take seconds
                    # https://zozo.jp/shop/medicomtoy/goods/54494701/?did=90518895
                    LOGGER.info(f"Zoho responded for item {keyword}", response.status_code)
                    response.encoding = response.apparent_encoding
                    # response = Selector(text=response.text)
                    # sid = response.xpath("//div[@class='cartbox']//form//input[@name='sid']/@value").extract_first()
                    # rid = response.xpath("//div[@class='cartbox']//form//input[@name='rid']/@value").extract_first()
                    sid = None
                    rid = None
                    soup = BeautifulSoup(response.text, 'lxml')
                    for cart in soup.findAll("div", {"class": "cartbox"}):
                        if 'sold out' not in str(cart):  # If sold out is found, the item is out of stock
                            # sid_names = [sid['name'] for sid in cart.findAll('input')]
                            sid_values = [sid['value'] for sid in cart.findAll('input')]
                            sid = sid_values[0]
                            rid = sid_values[1]
                            break
                    # for data in response.css(".blockMain li.clearfix"):
                    #     if data.css('input[value="カートへ入れる"]'):
                    #         sid = data.css("input[name='sid']::attr(value)").extract_first()
                    #         rid = data.css("input[name='rid']::attr(value)").extract_first()
                    #         break
                    if sid or seckey or rid:
                        LOGGER.info(f"Adding item {keyword} to cart")
                        # 'Referer': f'{link}',

                        data = {
                            'c': 'put',
                            'sid': f'{str(sid)}',
                            'rid': f'{str(rid)}',
                            'p_seckey': f'{str(seckey)}'
                        }
                        params = (
                            ('c', 'Message'),
                            ('no', '1'),
                            ('name', 'PutMessage'),
                        )
                        response = requests.post('https://zozo.jp/_cart/default.html', headers=headers, cookies=cookies,
                                                 data=data, proxies=proxies)
                        LOGGER.info(f"item {keyword} has been added to cart | response {response.status_code}")
                        break
                    else:
                        LOGGER.info(f"Item {keyword} is out of stock")
                else:
                    LOGGER.info(f"Item {keyword} was not found")
            else:
                response = requests.get(target_link, proxies=proxies, headers=headers_dic)
                response.encoding = response.apparent_encoding
                LOGGER.info(f"Zoho Responded for  {keyword}", response.status_code)
                # response = Selector(text=response.text)
                # response = requests.get(f"{link}",proxies=proxies) #this line is taking time this time is taken by server the rest take seconds
                # https://zozo.jp/shop/medicomtoy/goods/54494701/?did=90518895
                # sid = response.xpath("//div[@class='cartbox']//form//input[@name='sid']/@value").extract_first()
                # rid = response.xpath("//div[@class='cartbox']//form//input[@name='rid']/@value").extract_first()
                sid = None
                rid = None
                soup = BeautifulSoup(response.text, 'lxml')
                for cart in soup.findAll("div", {"class": "cartbox"}):
                    if 'sold out' not in str(cart):  # If sold out is found, the item is out of stock
                        # sid_names = [sid['name'] for sid in cart.findAll('input')]
                        sid_values = [sid['value'] for sid in cart.findAll('input')]
                        sid = sid_values[0]
                        rid = sid_values[1]
                        break
                # for data in response.css(".blockMain li.clearfix"):

                #     if data.css('input[value="カートへ入れる"]'):
                #         sid = data.css("input[name='sid']::attr(value)").extract_first()
                #         rid = data.css("input[name='rid']::attr(value)").extract_first()
                #         break
                if sid or seckey or rid:
                    LOGGER.info(f"Adding item {keyword} to cart")
                    # 'Referer': f'{link}',
                    data = {
                        'c': 'put',
                        'sid': f'{str(sid)}',
                        'rid': f'{str(rid)}',
                        'p_seckey': f'{str(seckey)}'
                    }
                    response = requests.post('https://zozo.jp/_cart/default.html', headers=headers, cookies=cookies,
                                             data=data, proxies=proxies)
                    LOGGER.info(f"Item {keyword} has been added to cart | response {response}")
                    break
                else:
                    LOGGER.info(f"Item {keyword} is out of stock")
            sleep(time_delay)

    def finish(self):
        try:
            driver.close()
            driver.quit()
            global stop
            stop = True
        except WebDriverException as exc:
            LOGGER.info('Issue occurred while closing the browser ...', exc.args)


def enable_cmd_colors():
    # Enables Windows New ANSI Support for Colored Printing on CMD
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def main():
    freeze_support()
    enable_cmd_colors()
    # Print ASCII Art
    print('************************************************************************\n')
    pyfiglet.print_figlet('____________                   ZozoBot ____________', colors='RED')
    print('\n************************************************************************')
    # Create ZozoBot instance
    zozo_bot = ZozoBot()
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = Path(PROJECT_ROOT)
    file_path_account = str(PROJECT_ROOT / "ZozoRes/Accounts.csv")
    if os.path.isfile(file_path_account):
        account_df = pd.read_csv(file_path_account, index_col=None)
        # Get accounts from Accounts.csv
        account_list = [account for account in account_df.iloc]
        account = account_list[0]
        # zozo_bot.add_to_cart(account=account)
        # start(account)
        # main(account_list[0])
        # Start the process
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(account_list)) as executor:
            executor.map(zozo_bot.add_to_cart, account_list)


if __name__ == '__main__':
    freeze_support()
    main()
