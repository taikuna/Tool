from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import requests
import time
import random
from tabulate import tabulate
import ssl
import subprocess
ssl._create_default_https_context = ssl._create_unverified_context

list_a =[]

port = 9229
proxies = {'https': "socks5://localhost:4007"}

time_out = 30
cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port="+str(port)+" --no-first-run --incognito -default-browser-check --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir') --proxy-server=socks5://localhost:4007"
#process = subprocess.Popen(cmd,shell=True)

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
chrome_driver = "/usr/local/bin/chromedriver"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+str(port))
driver = webdriver.Chrome(chrome_driver, options=chrome_options)


#url = 'https://www.lancers.jp/work/search/task'
#driver.get(url)

#table = soup.find_all(class_='table table-striped table-hover')[0]
#df = pd.read_html(str(table),index_col= 0)

#print( tabulate(df[0], headers='keys', tablefmt='grid') )
#location = df[0].loc['Location:']

list_a=[]
pg = 1

while True:
    url = 'https://www.lancers.jp/work/search/task?category=0&sort=client&page='+str(pg)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html5lib')
    for links in soup.find_all(class_='c-media__title'):
        link = 'https://www.lancers.jp' + links.get('href')
        dict_a={}
        dict_a['link'] = link
        list_a.append(dict_a)
    df = pd.DataFrame(list_a,columns=('time','link'))
    df2 = df.drop_duplicates('link',keep='last')
    df2.to_csv('lancers.csv')
    print(df2)
    sleep(1)
    pg+=1

