# -*- coding: utf-8 -*-
#import os
#os.chdir("/home/info1/Bloom/Spider/EC/yahoo/scan_yahoo.ipynb")
#os.getcwd()
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import requests
import time
import random
import ssl
import subprocess
from tabulate import tabulate
from fake_useragent import UserAgent
ssl._create_default_https_context = ssl._create_unverified_context

port = '4007'
proxies = {'https': "socks5://localhost:"+str(port)}

url = 'https://www.whatismyip.net/'

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
print(header)

r = requests.get(url,proxies=proxies,headers=header)
soup = BeautifulSoup(r.content,'html5lib')
table = soup.find_all(class_='table table-striped table-hover')[0]
df = pd.read_html(str(table),index_col= 0)
print( tabulate(df[0], headers='keys', tablefmt='grid') )

IP= df[0].at['IP Address:',1].split(' ')[0]+':'+str(port)
print(IP)

csv_input = pd.read_csv(filepath_or_buffer='Docs/cat_list_yh.csv', sep=",")
row = 17

while True:
    pg=1
    list_a = []
    new_c = 0
    while True:
        urls = csv_input.values[row,1]
        keyword= csv_input.values[row,2]
        url= urls+'?X=4&view=grid&ei=UTF-8&b='+str(pg)
        #url='https://shopping.yahoo.co.jp/search?p='+keyword+'&tab_ex=commerce&oq=&pf=&pt=&ei=UTF-8&b='+str(pg)
        start = time.time()
        r = requests.get(url,proxies=proxies)
        soup = BeautifulSoup(r.content,'html5lib')
        search = soup.find(class_='elTitle')
        search_t =search.get_text().split('（')[0]
        print(search_t)
        stop = time.time()
        req_time = round(stop-start,3)

        for info in soup.find_all(class_=['elStore']):
            for link in info.find_all('a',href=re.compile('https://store.shopping.yahoo.co.jp/')):
                shop = link.get_text()
                links = link.get('href')

            dict_a ={}
            dict_a['time'] = datetime.now()
            dict_a['category'] = search_t
            dict_a['page'] = pg
            dict_a['req_time']=req_time
            dict_a['IP']=IP

            try:
                link = links
                dict_a['link'] = link
            except AttributeError:
                pass
                dict_a['link'] = ''

            try:
                dict_a['shop'] = shop
            except AttributeError:
                pass
                dict_a['shop'] = ''

            list_a.append(dict_a)
        print(shop)

        prev = 'Docs/scan_yahoo.csv'
        dfo = pd.read_csv(prev)
        df = pd.DataFrame(list_a,columns=('time','shop','link','category','page','IP','req_time'))
        dft = pd.concat([df, dfo])
        dff = dft.drop_duplicates('link',keep='last')
        dff.to_csv('Docs/scan_yahoo.csv',columns=['time','shop','link','category','page','IP','req_time'],encoding='utf-8')
        print(search_t+' '+str(pg)+'件目完了')
        print('Loading time')
        print(stop-start)
        new_t = str(dff.shape).replace('(','').replace(')','').split(',')[0]
        inew_t = int(new_t)
        print(dff.shape)
        print(str(pg)+' 件目完了')
        print('新規'+str(inew_t-new_c)+'件')
        new_c = 0
        new_c +=inew_t
        print(url)
        pg+=100
        time.sleep(random.randint(4, 8))
        if pg >= 10000:
            row+=1
            break

