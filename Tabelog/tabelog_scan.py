from bs4 import BeautifulSoup
import requests
from datetime import datetime
from requests import get
import pandas as pd
import numpy as np
import re
import sys
a = datetime.now()


def scan():
    url = 'https://tabelog.com/hokkaido/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for page in soup.find_all(class_='list-rst__rst-name-target cpy-rst-name'):
        content_dict = {}
        time = datetime.now()
        title = page.text
        link = page.get('href')
        content_dict['time'] = time
        content_dict['title'] = title
        content_dict['link'] = link

        print(title)
        print(link)
        content_list.append(content_dict)
        df = pd.DataFrame(content_list,columns=['time','title','link'])
        df.to_csv("tabelog_scan.csv")

def info():
    csv_input = pd.read_csv(filepath_or_buffer='tabelog_scan.csv', sep=",")
    url = csv_input.values[0, 3]
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    content_list =[]



    for page_name in soup.find_all(class_="display-name"):
        page = page_name.text.strip()
        print(page)
    for street_add in soup.find_all(class_='rstinfo-table__address'):
        street = street_add.text
        print(street)

        content_dict = {}
        time = datetime.now()
        content_dict['time'] = time
        content_dict['title'] = page
        content_dict['street'] = street
        content_list.append(content_dict)
        df = pd.DataFrame(content_list,columns=['time','title','street'])
        df.to_csv("tabelog.csv")

    for info in soup.find_all(class_='c-table c-table--form rstinfo-table__table'):
        for info2 in info.find_all('tr'):

                print(info2)

def test():
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from tabulate import tabulate
    content_list=[]

    url_no = 0
    stop =5



    while True:

        content_dict ={}

        csv_input = pd.read_csv(filepath_or_buffer='tabelog_scan.csv', sep=",")
        url = csv_input.values[url_no, 3]
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        table = soup.find_all(class_='rstinfo-table')[0]
        df = pd.read_html(str(table))

        print( tabulate(df[0], headers='keys', tablefmt='psql') )
        print( tabulate(df[1], headers='keys', tablefmt='psql') )
        print( tabulate(df[2], headers='keys', tablefmt='psql') )
        print( tabulate(df[3], headers='keys', tablefmt='psql') )

        content_dict['時間'] = datetime.now()
        content_dict['店名'] = df[0].at[0,1]
        content_dict['ジャンル'] = df[0].at[1,1]
        content_dict['予約・お問い合わせ'] = df[0].at[2,1]
        content_dict['予約可否'] = df[0].at[3,1]
        content_dict['住所'] = df[0].at[4,1]
        content_dict['交通手段'] = df[0].at[5,1]
        content_dict['営業時間'] = df[0].at[6,1]
        content_dict['定休日'] = df[0].at[7,1]
        content_dict['予算'] = df[0].at[8,1]
        content_dict['予算（口コミ集計）'] = df[0].at[9,1]
        content_dict['支払い方法'] = df[0].at[10,1]
        content_dict['席数'] = df[1].at[0,1]
        content_dict['個室'] = df[1].at[1,1]
        content_dict['貸切'] = df[1].at[2,1]
        content_dict['禁煙・喫煙'] = df[1].at[3,1]
        content_dict['駐車場'] = df[1].at[4,1]
        content_dict['空間・設備'] = df[1].at[5,1]
        content_dict['携帯電話'] = df[1].at[6,1]
        content_dict['利用シーン'] = df[3].at[0,1]
        content_dict['サービス'] = df[3].at[1,1]
        content_dict['お子様連れ'] = df[3].at[2,1]
        content_dict['ホームページ'] = df[3].at[3,1]
        content_dict['公式アカウント'] = df[3].at[3,1]
        content_dict['オープン日'] = df[3].at[3,1]
        content_dict['ホームページ'] = df[3].at[3,1]


        try:
            content_dict['サービス料・チャージ'] = df[0].at[11,1]

        except KeyError:
            pass
            print('No 11 is none')
            content_dict['サービス料・チャージ'] = ""

        content_list.append(content_dict)
        dfs = pd.DataFrame(content_list,columns=['時間','店名','ジャンル','予約・お問い合わせ','予約可否','住所','交通手段','営業時間','定休日','予算','予算（口コミ集計）','支払い方法','サービス料・チャージ','席数','個室','貸切','禁煙・喫煙','駐車場','空間・設備','携帯電話','飲み放題コース','コース','ドリンク','料理'])
        dfs.to_csv("tabelog.csv")

        url_no +=1

        if url_no == stop:
            break






test()

