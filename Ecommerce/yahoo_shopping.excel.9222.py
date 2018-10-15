# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains
import re

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

i=1
path = ''

file_name = "yahoo.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'test_sheet_1'

ws.cell(row=1, column=1).value = 'Time'
ws.cell(row=1, column=2).value = 'Page title'
ws.cell(row=1, column=3).value = 'Hit'
ws.cell(row=1, column=4).value = 'Item'
ws.cell(row=1, column=5).value = 'URL'
ws.cell(row=1, column=6).value = 'Price'

page = 1
url= 'https://shopping.yahoo.co.jp/category/2498/list?oq=&uIv=on&pf=&pt=&used=0&seller=0&ei=UTF-8&b=' + str(page)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')
row = 2
row1 =2
a = datetime.now()
for parent in soup.find_all(class_='mdSearchList elList'):
    for item in parent.find_all('dd', class_="elName", string=True):
        for link in item.find_all('a'):
            ws.cell(row=row, column=4).value = item.string
            ws.cell(row=row, column=5).value = link.get('href')
            ws.cell(row=row, column=1).value = a.ctime()
            ws.cell(row=row, column=2).value = soup.head.title.text
            ws.cell(row=row, column=3).value = soup.find(class_="elOrder", string=True)
            row +=1

for pricea in soup.find_all(class_='elUnit', text=re.compile('円')):
    for priceb in pricea.previous_sibling:
        print(priceb)
        ws.cell(row=row, column=6).value = priceb
        row1 +=1


wb.save(path + file_name)
print(row)
print ("")
next = driver.find_element_by_xpath('//*[@class="elNext"]')
ActionChains(driver).move_to_element(next).click().perform()








