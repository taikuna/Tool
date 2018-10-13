# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
import cchardet
from datetime import datetime

rl=2
rt=2
i=5
path = ''
file_name = "rakuten_item.xlsx"
wb = load_workbook(path + file_name)
ws = wb['Sheet1']

ws.cell(row=1, column=1).value = 'Time'

while True:
    print(i)
    url = "https://search.rakuten.co.jp/search/mall/%E5%A5%B3%E6%80%A7%E7%94%A8%E3%80%80%E3%82%B9%E3%82%AB%E3%83%BC%E3%83%95/"
    r = requests.get(url)
    r.encoding = cchardet.detect(r.content)["encoding"]
    soup = BeautifulSoup(r.text, 'lxml')
    pg = soup.head.title

    thread = soup.find(class_="count _medium").text
    th_sp = thread.replace('\n', '').replace(' ', '')
    a = datetime.now()
    print(th_sp)


    for shop_list in soup.find_all(class_="content title"):
     for thread_title in shop_list.find_all('a', href=True):
        print(thread_title)
        print(shop_list)
        ws.cell(row=rl, column=5).value = shop_list['href']
        ws.cell(row=rl, column=2).value = pg.text
        rl += 1


    for shop_title in soup.find_all(class_="content title"):
        for thread_title in shop_title.find_all('a', href=True):
            ws.cell(row=rt, column=4).value = thread_title.text
            ws.cell(row=rt, column=3).value = th_sp
            ws.cell(row=rt, column=1).value = a.ctime()
            rt += 1



    wb.save(path + file_name)
    i+=1
    print(pg)
    print(rl)
    print(rt)
    print(i)
    if rl >10:
        break

