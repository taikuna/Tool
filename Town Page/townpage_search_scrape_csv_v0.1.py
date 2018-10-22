import re
from time import sleep
from requests import get
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
def scan():
    content_list=[]
    file_path = 'Docs/'

    page = 1
    stop = 1500
    while True:

        print("Page "+ str(page)+' Scan start....')

        location = 'tokyo'
        genre = 'realestate'

        csv_name = location + '_' + genre + '_scan.csv'

        link = 'https://itp.ne.jp/'+ location +'/genre_dir/'+genre+'/pg/'
        link2 = '/?ngr=1&nad=1&sr=1&sr=1&sr=1&sr=1&sr=1&evdc=1&sr=1&num=50'
        url = link + str(page) +link2
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        hit = soup.find('span',text=re.compile('件/')).text
        paget = soup.find(class_="searchResultHeader").text
        print(paget)
        print(hit)

        for clearfix in soup.find_all(class_='clearfix'):
            for info in clearfix.find_all('a',href=re.compile('/info/'),text=True):
                company_name = info.text
                company_url = info.get('href').split('/')[2]

                content_dict ={}
                content_dict['time'] = datetime.now()
                content_dict['hit'] = hit
                content_dict['page title'] = paget
                content_dict['name'] = company_name
                content_dict['id'] = company_url
                content_list.append(content_dict)

                df = pd.DataFrame(content_list,columns=['time','page title','hit','name','id'])
                df.to_csv(file_path+csv_name)
        print('Page '+ str(page) + 'done')
        page+=1

        sleep(2)
        if page == stop:
            break

def scrape():
    last_list=[]
    file_path = 'Docs/'

    input_file = 'tokyo_realestate_scan.csv'

    fsplit = input_file.split('_')[0]
    fsplit2 = input_file.split('_')[1]
    file_name = fsplit + '_'+ fsplit2

    header = '時間','ID','カテゴリー','件','掲載名','フリガナ','電話番号','FAX番号','住所','アクセス','駐車場','現金以外の支払い方法','ホームページ','E-mailアドレス','業種','営業時間','休業日','予約'

    url_no = 0
    stop = 0

    while True:
        print('No '+str(url_no)+ " start...")
        csv_input = pd.read_csv(filepath_or_buffer=file_path+input_file, sep=",")
        u_id = csv_input.values[url_no, 5]
        print('ID'+str(u_id))

        pg_cat = csv_input.values[url_no, 2]
        hit_co = csv_input.values[url_no, 3]

        link = 'https://itp.ne.jp/info/'
        link2 = '/shop/'
        url = link + str(u_id) + link2
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        p_type = soup.find('h1',text=re.compile('基本情報'))

        p_none = soup.find(text=re.compile('表示できる店舗がありません。'))
        if p_none is not None:
            pass
            print(p_type)
            last_d={}

            last_d['時間'] = datetime.now()
            last_d['ID'] = u_id
            last_d['掲載名'] = p_none

            last_list.append(last_d)

            dfs = pd.DataFrame(last_list,columns=header)
            dfs.to_csv(file_path + file_name + '.csv')
            del dfs

            print('Done!')

            url_no +=1

        elif p_type is None:
            print('It is old table')
            table = soup.find_all(class_='detailTable')[0]
            df = pd.read_html(str(table),index_col= 0)
            for nam in soup.find_all(class_="hgroup"):
                for name in nam.find('h1'):
                    print(name)

            last_d={}

            street = df[0].at['住所',1]
            phone = df[0].at['TEL',1]
            ind_type = df[0].at['業種',1]

            last_d['時間'] = datetime.now()
            last_d['カテゴリー'] = pg_cat
            last_d['件'] = hit_co
            last_d['ID'] = u_id
            last_d['住所'] = street
            last_d['掲載名'] = name
            last_d['電話番号'] = phone
            last_d['業種'] = ind_type

            try:
                website = df[0].at['ホームページ',1]
                last_d['ホームページ'] = website
            except KeyError:
                pass
                last_d['ホームページ'] = ''

            try:
                mail = df[0].at['E-mail',1]
                last_d['E-mailアドレス'] = mail
            except KeyError:
                pass
                last_d['E-mailアドレス'] = ''

            last_list.append(last_d)

            dfs = pd.DataFrame(last_list,columns=header)
            dfs.to_csv(file_path + file_name + '.csv')
            del dfs

            print('Done!')

            url_no +=1

        else:
            content_list=[]
            category_list=[]

            for info in soup.find_all(class_='item item-table'):
                for cont in info.find_all('dd'):
                    contents = cont.text.strip().replace('\n','')
                    info_dict = {}
                    info_dict['contents'] = contents
                    content_list.append(info_dict)
                df = pd.DataFrame(content_list)

            for info in soup.find_all(class_='item item-table'):
                for cat in info.find_all('dt'):
                    cate = cat.text.strip().replace('\n','')
                    cat_dict = {}
                    cat_dict['category'] = cate
                    category_list.append(cat_dict)
                dfc = pd.DataFrame(category_list)
            df_final = pd.concat([dfc, df], axis=1).set_index('category')

            last_d = {}
            n = 'contents'

            time = datetime.now()
            name = df_final.at['掲載名',n]
            ruby = df_final.at['フリガナ',n]
            cell_phone = df_final.at['電話番号',n]
            fax = df_final.at['FAX番号',n]
            street = df_final.at['住所',n]
            access = df_final.at['アクセス',n]
            website = df_final.at['ホームページ',n]
            email = df_final.at['E-mailアドレス',n]

            print(name)

            last_d['時間'] = time
            last_d['ID'] = u_id
            last_d['カテゴリー'] = pg_cat
            last_d['件'] = hit_co
            last_d['掲載名'] = name
            last_d['フリガナ'] = ruby
            last_d['電話番号'] = cell_phone
            last_d['FAX番号'] = fax
            last_d['住所'] = street
            last_d['アクセス'] = access
            last_d['ホームページ'] = website
            last_d['E-mailアドレス'] = email

            try:
                booking = df_final.at['予約',n]
                last_d['予約'] = booking
            except KeyError:
                pass
                last_d['予約'] = ''
                print('No 予約 found')

            try:
                payment = df_final.at['現金以外の支払い方法',n]
                last_d['現金以外の支払い方法'] = payment
            except KeyError:
                pass
                last_d['現金以外の支払い方法'] = ''
                print('No 現金以外の支払い方法 found')

            try:
                parking = df_final.at['駐車場',n]
                last_d['駐車場'] = parking
            except KeyError:
                pass
                last_d['駐車場'] = ''
                print('No 駐車場 found')

            try:
                day_off = df_final.at['休業日',n]
                last_d['休業日'] = day_off
            except KeyError:
                pass
                last_d['休業日'] = ''
                print('No 休業日 found')

            try:
                ind_type = df_final.at['業種',n]
                last_d['業種'] = ind_type
            except KeyError:
                pass
                last_d['業種'] = ''
                print('No 業種 found')

            try:
                w_hours = df_final.at['営業時間',n]
                last_d['営業時間'] = w_hours
            except KeyError:
                pass
                last_d['営業時間'] = ''
                print('No 営業時間 found')

            last_list.append(last_d)
            dfs = pd.DataFrame(last_list,columns=header)
            dfs.to_csv(file_path + file_name + '.csv')

            del df
            del dfc
            url_no +=1
            print('done !')
        if url_no == stop:
            break

def finder():
    url_no = 1

    while True:
        print(url_no)
        csv_input = pd.read_csv(filepath_or_buffer='townpage_scan.csv', sep=",")
        u_id = csv_input.values[url_no, 4]
        link = 'https://itp.ne.jp/info/'
        link2 = '/shop/'
        temp = 123291398100000899
        url = link + str(temp) + link2
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        for info in soup.find_all('dl'):
            for title in info.find_all(text=re.compile('掲載名')):
                print(info)



        url_no+=1
        if url_no == 2:
            break

scrape()