from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from openpyxl import load_workbook
import selenium.common.exceptions
from bs4 import BeautifulSoup
from datetime import datetime
import re

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

print (driver.title)
path = ''
file_name = "amazon_spider.xlsx"
wb = load_workbook(path + file_name)
ws = wb['Sheet1']

row = 2
page = 1
stop = 0

while True:
    url = ws.cell(row=int(row), column=2).value
    soup = BeautifulSoup(driver.page_source, 'lxml')
    a = datetime.now()
    driver.get(url)


    try:
        for shop_info in soup.find_all(class_="a-unordered-list a-nostyle a-vertical"):
            text = shop_info.get_text()
            info =text.replace('お問い合わせ先電話番号:',':').replace('住所:',':').replace('販売業者:',':').replace('運営責任者名:',':').replace('店舗名:',':').replace('古物商許可証番号:',':').rsplit(':')

            print(len(info),info)
            company = info[1]
            phone = int(info[2])
            street = info[3]
            name = info[4]
            shop = info[5]
            lic = info[6]
            ws.cell(row=int(row), column=3).value = company
            ws.cell(row=int(row), column=4).value = phone
            ws.cell(row=int(row), column=6).value = name
            ws.cell(row=int(row), column=7).value = shop
            ws.cell(row=int(row), column=8).value = lic
            row +=1

            print(company, phone, street, name, lic)
            wb.save(file_name)


    except selenium.common.exceptions.NoSuchElementException:
        pass
        ws.cell(row=int(row),column=5).value = "Error"
        print('Error')
        row+=1

    if  page == stop :
        break



