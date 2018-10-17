from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from openpyxl import load_workbook
import selenium.common.exceptions
from bs4 import BeautifulSoup
from datetime import datetime
import re
from selenium.webdriver.common.action_chains import ActionChains

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

driver.get('https://www.amazon.co.jp/sp?_encoding=UTF8&asin=&isAmazonFulfilled=1&isCBA=&marketplaceID=A1VC38T7YXB528&orderID=&seller=A1SCG83LRZ2FI9&tab=&vasStoreID=')

soup = BeautifulSoup(driver.page_source, 'lxml')

for aaa in soup.find('span', text=re.compile('お問い合わせ先電話番号:')):
    print(aaa.next_sibling)

for test in soup.find_all(class_="a-unordered-list a-nostyle a-vertical"):
    for test1 in test.find_all(class_='a-text-bold', text=re.compile('お問い合わせ先電話番号:')):
        print(test1.next_sibling)



