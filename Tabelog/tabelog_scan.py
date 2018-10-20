from bs4 import BeautifulSoup
import requests
from datetime import datetime
import cchardet
from requests import get
import pandas as pd
import numpy as np
import re
import sys
a = datetime.now()
from time import sleep



def scan():
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains

    _user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    url = 'https://tabelog.com/hokkaido/A0101/'

    driver.get(url)

    content_list = []
    page = 1
    stop =3

    while True:
        print('Page ' +str(page) + ' start....')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for shop in soup.find_all(class_='list-rst__rst-name-target cpy-rst-name'):
            time = datetime.now()
            title = shop.text
            link = shop.get('href')
            content_dict = {}
            content_dict['time'] = time
            content_dict['title'] = title
            content_dict['link'] = link
            content_list.append(content_dict)
            df = pd.DataFrame(content_list,columns=['time','title','link'])
            df.to_csv("tabelog_scan.csv")
            print(title)
            print(link)
        next = driver.find_element_by_xpath('//*[@class="c-pagination__arrow c-pagination__arrow--next"]')
        ActionChains(driver).move_to_element(next).click().perform()

        sleep(0)
        page +=1

        if page == stop:
            break


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

def scrape():
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
        df = pd.read_html(str(table),index_col= 0)


        print( tabulate(df[0], headers='keys', tablefmt='grid') )
        print( tabulate(df[1], headers='keys', tablefmt='psql') )
        print( tabulate(df[2], headers='keys', tablefmt='psql') )
        print( tabulate(df[3], headers='keys', tablefmt='psql') )

        content_dict['時間'] = datetime.now()
        content_dict['店名'] = df[0].at["店名",1]
        content_dict['ジャンル'] = df[0].at['ジャンル',1]
        content_dict['予約・  お問い合わせ'] = df[0].at['予約・  お問い合わせ',1]
        content_dict['予約可否'] = df[0].at['予約可否',1]
        content_dict['住所'] = df[0].at['住所',1]
        content_dict['交通手段'] = df[0].at['交通手段',1]
        content_dict['営業時間'] = df[0].at['営業時間',1]
        content_dict['定休日'] = df[0].at['定休日',1]
        content_dict['予算'] = df[0].at['予算',1]
        content_dict['予算（口コミ集計）'] = df[0].at['予算（口コミ集計）',1]
        content_dict['支払い方法'] = df[0].at['支払い方法',1]
        content_dict['席数'] = df[1].at['席数',1]
        content_dict['個室'] = df[1].at['個室',1]
        content_dict['貸切'] = df[1].at['貸切',1]
        content_dict['禁煙・喫煙'] = df[1].at['禁煙・喫煙',1]
        content_dict['駐車場'] = df[1].at['駐車場',1]
        content_dict['空間・設備'] = df[1].at['空間・設備',1]
        content_dict['携帯電話'] = df[1].at['携帯電話',1]
        content_dict['お子様連れ'] = df[3].at['お子様連れ',1]
        content_dict['電話番号'] = df[3].at['電話番号',1]
        content_dict['初投稿者'] = df[3].at['初投稿者',1]
        content_dict['URL'] = url

        try:
            content_dict['サービス料・チャージ'] = df[0].at['サービス料・チャージ',1]
        except KeyError:
            pass
            print('サービス料・チャージ is none')
            content_dict['サービス料・チャージ'] = ""
        try:
            content_dict['飲み放題コース'] = df[2].at['飲み放題',1]
        except KeyError:
            pass
            print('飲み放題コース is none')
            content_dict['飲み放題コース'] = ""
        try:
            content_dict['コース'] = df[2].at['コース',1]
        except KeyError:
            pass
            print('コース is none')
            content_dict['コース'] = ""
        try:
            content_dict['ドリンク'] = df[2].at['ドリンク',1]
        except KeyError:
            pass
            print('ドリンク is none')
            content_dict['ドリンク'] = ""
        try:
            content_dict['料理'] = df[2].at['料理',1]
        except KeyError:
            pass
            print('料理 is none')
            content_dict['料理'] = ""
        try:
            content_dict['利用シーン'] = df[3].at['利用シーン',1]
        except KeyError:
            pass
            print('利用シーン is none')
            content_dict['利用シーン'] = ""
        try:
            content_dict['サービス'] = df[3].at['サービス',1]
        except KeyError:
            pass
            print('サービス is none')
            content_dict['サービス'] = ""
        try:
            content_dict['ホームページ'] = df[3].at['ホームページ',1]
        except KeyError:
            pass
            print('ホームページ is none')
            content_dict['ホームページ'] = ""
        try:
            content_dict['公式アカウント'] = df[3].at['公式アカウント',1]
        except KeyError:
            pass
            print('公式アカウント is none')
            content_dict['公式アカウント'] = ""
        try:
            content_dict['オープン日'] = df[3].at['オープン日',1]
        except KeyError:
            pass
            print('オープン日 is none')
            content_dict['オープン日'] = ""



        content_list.append(content_dict)
        dfs = pd.DataFrame(content_list,columns=['時間','店名','ジャンル','予約・お問い合わせ','予約可否','住所','交通手段','営業時間','定休日','予算','予算（口コミ集計）','支払い方法','サービス料・チャージ','席数','個室','貸切','禁煙・喫煙','駐車場','空間・設備','携帯電話','利用シーン','飲み放題コース','コース','ドリンク','料理','サービス','お子様連れ','ホームページ','公式アカウント','電話番号','初投稿者','URL'])
        dfs.to_csv("tabelog.csv")

        url_no +=1

        if url_no == stop:
            break

scan()

