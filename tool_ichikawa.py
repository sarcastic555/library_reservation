# /usr/local/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import logging
import sys
import os
import re
import random
import requests
import bs4
import codecs
import pandas as pd
import numpy as np
import html5lib

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s : %(asctime)s : %(message)s')


class IchikawaModule:
    def __init__(self):
        self.debug=False
        self.ID='7093281'
        self.password='ngkrnok555'
        self.sleeptime=3 ## sleeping time [sec]
        self.cookie={}
        self.URL_booklist='https://www.library.city.ichikawa.lg.jp/winj/opac/'
        self.URL_entrance='https://www.library.city.ichikawa.lg.jp/winj/opac/top.do'
        self.URL_loginpage='https://www.library.city.ichikawa.lg.jp/winj/opac/login.do'
        self.URL_toppage='https://www.library.city.ichikawa.lg.jp/winj/opac/login.do'
        self.URL_search='https://www.library.city.ichikawa.lg.jp/winj/opac/search-detail.do'
        self.URL_reserve='https://www.library.city.ichikawa.lg.jp/winj/opac/search-list.do'
        self.URL_lend='https://www.library.city.ichikawa.lg.jp/winj/opac/lend-list.do'
        self.URL_basket='https://www.library.city.ichikawa.lg.jp/winj/opac/reserve-basket.do'
        self.URL_basket_delete='https://www.library.city.ichikawa.lg.jp/winj/opac/reserve-basket-delete.do'
        self.URL_confirm='https://www.library.city.ichikawa.lg.jp/winj/opac/reserve-confirm.do'
        self.URL_logout='https://www.library.city.ichikawa.lg.jp/winj/opac/logout.do'
        self.URL_extend='https://www.library.city.ichikawa.lg.jp/winj/opac/lend-extension-confirm.do'
        self.header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.library.city.ichikawa.lg.jp',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.search_params={
            'chk_catph': '11 31','chk_catph': '13 33','chk_catph': '14 34','chk_catph': '15 35','chk_catph': '17 37','cmb_column1': 'title','txt_word1': '','cmb_like1': '2','cmb_unit1': '0','cmb_column2': 'author','txt_word2': '','cmb_like2': '2','cmb_unit2': '0','cmb_column3': 'publisher','txt_word3': '','cmb_like3': '2','cmb_unit3': '0','cmb_column4': 'subject','txt_word4': '','cmb_like4': '2','cmb_unit4': '0','cmb_column5': 'ndc','txt_word5': '','cmb_like5': '1','cmb_unit5': '0','cmb_column6': 'p_title','txt_word6': '','cmb_like6': '2','cmb_unit6': '0','cmb_column7': 'p_publisher','txt_word7': '','cmb_like7': '2','cmb_unit7': '0','chk_hol1tp': '00','chk_hol1tp': '80','chk_hol1tp': '20','chk_hol1tp': '50','chk_hol1tp': '90','chk_hol1tp': '30','chk_hol1tp': '40','chk_hol1tp': '10','chk_hol1tp': '11','chk_hol1tp': '12','chk_hol1tp': '13','chk_hol1tp': '70','chk_hol1tp': '72','chk_hol1tp': '75','chk_hol1tp': '76','chk_hol1tp': '61','chk_hol1tp': '62','chk_hol1tp': '63','chk_hol1tp': '64','chk_hol1tp': '65','chk_hol1tp': '66','chk_hol1tp': '67','chk_hol1tp': '68','chk_hol1tp': '69','chk_hol1tp': '60','chk_hol1tp': '71','chk_hol1tp': '73','chk_hol1tp': '74','chk_hol1tp': '77','txt_stpubdate': '','txt_edpubdate': '','cmb_volume_column': 'volume','txt_stvolume': '','txt_edvolume': '','cmb_code_column': 'isbn','txt_code': '0000000000000','txt_lom': '','txt_cln1': '','txt_cln2': '','txt_cln3': '','chk_area': '01','chk_area': '02','chk_area': '03','chk_area': '04','chk_area': '05','chk_area': '06','chk_area': '07','chk_area': '11','chk_area': '41','chk_area': '42','cmb_order': 'crtdt','opt_order': '1','opt_pagesize': '10','submit_btn_searchDetailSelAr': '所蔵検索'
        }
        self.reserve_params={
            "hid_session": "0000000","chk_rsvbib": "","submit_btn_rsv_basket": "予約かご","cmb_oder": "title","opt_oder": "1","opt_pagesize": "10","chk_check": "0","cmb_oder": "title","opt_oder": "1","opt_pagesize": "10"
        }
        self.basket_submit_params={
            "hid_session": "00000000","hid_aplph": "W","cmb_area": "02","view-title": "T170P68001","txt_year": "9999","cmb_month": "12","cmb_day": "31","chk_check": "1101897016","submit_btn_reservation": "通常予約する"
        }
        self.basket_delete_params={
            "hid_session": "00000000","hid_aplph": "W","cmb_area": "02","view-title": "T170P68001","txt_year": "9999","cmb_month": "12","cmb_day": "31","submit_btn_delete": "削除"
        }
        self.basket_delete_confirm_params={
            "hid_session": "00000000", "submit_btn_delete": "削除"
        }
        self.confirm_params={
            "hid_session": "00000000","hid_aplph": "W","submit_btn_confirm": "予約する"
        }
        self.mypage_params={
            "dispatch": "/opac/mylibrary.do", "every": "1"
        }
        self.extend_params={
            "hid_session": "00000000","idx": "0","submit_btn_extend": "/T170P11011","opt_pagesize": "10","opt_pagesize": "10"
        }
        self.extend_confirm_params={
            "hid_session": "00000000","hid_lenid": "0001501174","submit_btn_confirm": "貸出延長する"
        }
        
    def set_debug_mode(self, mode):
        self.debug = mode ## True or False

    def set_sleep_time(self, sleeptime):
        self.sleeptime=sleeptime

    def register_sessionID(self, sessionID_string):
        #print(self.URL_loginpage)
        #print(sessionID_string)
        self.URL_loginpage='%s;JSESSIONID=%s'%(self.URL_loginpage,sessionID_string)
        self.URL_toppage='%s;JSESSIONID=%s'%(self.URL_toppage,sessionID_string)
        self.header['Cookie']='JSESSIONID=%s'%sessionID_string
        self.reserve_params['hid_session']=sessionID_string
        self.basket_submit_params['hid_session']=sessionID_string
        self.basket_delete_params['hid_session']=sessionID_string
        self.basket_delete_confirm_params['hid_session']=sessionID_string
        self.confirm_params['hid_session']=sessionID_string
        self.extend_params['hid_session']=sessionID_string
        self.extend_confirm_params['hid_session']=sessionID_string

    ## マイページのHTMLを読み込んで、bookIDに対応する本が貸出延長可能かどうか判定する関数
    ## 各資料の詳細ページからは判定できないので、貸し出し一覧ページから情報を取得する
    def get_extension_status_per_book(self, bookid):
      logging.info(f"IchikawaModule::get_extension_status_per_book (bookid={bookid}) called")
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_lend, headers=self.header, cookies=self.cookie)
      soup = bs4.BeautifulSoup(r.text, "html5lib")
      extendbutton_content = soup.find('ol', class_='list-book result hook-check-all').find_all('div', class_='info')
      ### class='column info'(本の詳細情報)とclass='info'(延長ボタン情報)の2つが取られてしまうので、あとで2*i+1番目を指定するようにする
      ### 貸出延長可能かチェック(延長ボタンがないと、rightbutton=Noneとなる)
      rightbutton = extendbutton_content[2*bookid+1].find('a')
      enableextension = False
      if rightbutton is not None:
        enableextension = True
      return enableextension

    ### マイページのHTMLを読み込んで、bookIDに対応する返却日をdatetimeで返す関数
    def get_return_date_datetime_per_book(self, bookid):
      logging.info(f"IchikawaModule::get_return_date_datetime_per_book (bookid={bookid}) called")
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_lend, headers=self.header, cookies=self.cookie)
      soup = bs4.BeautifulSoup(r.text, "html5lib")
      detail_content=soup.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')
      info = detail_content[bookid].find('div', class_='column info').find_all('p')[3].find('b').text.strip()
      year  = int(re.search('([0-9]+)/[0-9]+/[0-9]+',info)[1])
      month = int(re.search('[0-9]+/([0-9]+)/[0-9]+',info)[1])
      day   = int(re.search('[0-9]+/[0-9]+/([0-9]+)',info)[1])
      return datetime.date(year,month,day)

    ## マイページの予約一覧のHTMLを読み込んで、本のstatus(予約順位とか)を返す関数
    def get_book_reserve_status_per_book(self, bookid):
      logging.info(f"IchikawaModule::get_book_status_per_book (bookid={bookid}) called")
      if (bookid <= 9):
        time.sleep(self.sleeptime)
        r = self.session.get('%s/-list.do'%(self.URL_booklist,"reserve"), headers=self.header, cookies=self.cookie)
      elif (bookid >= 10):
        ## ページが変わる場合は次ページ情報を読み込む
        page = str(int(bookid / 10) + 1)
        time.sleep(self.sleeptime)
        r = self.session.get('%s/%s-list.do'%(self.URL_booklist,listtype), headers=self.header, params={'page': page})
      soup_list = bs4.BeautifulSoup(r.text, "html5lib")
      hoge = soup_list.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')[bookid%10]
      for i, ho in enumerate(hoge):
        print('#'*20)
        print(i)
        print(ho)
      print(soup_list.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')[bookid%10])
      try:
        status = soup_list.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')[bookid%10].find('div', class_='column info').find_all('p')[2].text.strip()
        status = "error" if status == "" else status
      except:        
        status = "error"
      return status

    def register_cookie(self, cookie):
        self.cookie=cookie
        
    def get_sessionid_from_header(self, headers):
        return headers['Set-Cookie'].split(";")[0][11:] ## 頭の"JSESSIONID="を削除する

    def get_cookie_from_header(self, cookies):
        return dict(JSESSIONID=cookies.get('JSESSIONID'))

    def set_isbn_to_params(self, isbn):
        self.search_params['txt_code']=isbn

    def execute_login_procedure(self):
        self.session = requests.session()

        ### 0. 図書館トップ画面に移動
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_entrance)
        self.header["Cookie"] = r.headers["Set-Cookie"]
        
        ### 1. ログイン画面に入る
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_loginpage, headers=self.header)

        ## 2. ログイン処理
        data={
            'txt_usercd': self.ID,
            'txt_password': self.password,
            'submit_btn_login': 'ログイン(認証)'
        }
        ### allow_redirects=Falseのオプションをつけないとヘッダからクッキーが取得できない
        time.sleep(self.sleeptime)
        r = self.session.post(self.URL_loginpage, headers=self.header, data=data, allow_redirects=False)
        with open('login_manip.html', 'w') as file:
            file.write(r.text)
        self.header["Cookie"] = r.headers["Set-Cookie"]

    def get_num_of_total_books(self, listtype) -> int:
      logging.info(f"IchikawaModule::get_num_of_total_books ({listtype}) called")
      time.sleep(self.sleeptime)
      r = self.session.get('%s/%s-list.do'%(self.URL_booklist,listtype), headers=self.header)
      soup_list = bs4.BeautifulSoup(r.text, "html5lib")
      h2_in_soup = soup_list.find('h2', class_='nav-hdg')
      if h2_in_soup == None:
        return 0
      totalnum_text = h2_in_soup.text
      logging.debug(f"totalnum_text = {totalnum_text}")
      totalnum = int(re.search('（全([0-9]+) 件）',totalnum_text)[1])
      return totalnum

    def get_title_and_isbn_from_book_info(self, bookid, listtype):
      logging.info(f"IchikawaModule::get_title_and_isbn_from_book_info (bookid={bookid}, listtype={listtype}) called")
      time.sleep(self.sleeptime)
      r = self.session.get('%s/%s-detail.do'%(self.URL_booklist,listtype),headers=self.header,cookies=self.cookie, params={'idx':'%d'%(bookid%10)})
      time.sleep(self.sleeptime)
      ## switch-detailの画面には常に本が1冊しか表示されないので、idx=0でOK
      r = self.session.get('%s/switch-detail.do'%self.URL_booklist, headers=self.header, cookies=self.cookie, params={'idx':'0'})
      soup = bs4.BeautifulSoup(r.text, "html.parser")
      table_contents = soup.find('table', class_='tbl-04').find_all('tr')
      isbn10 = None
      title = None
      isbn13 = None
      for table_content in table_contents:
        if table_content.find('th').text.strip() == "ISBN":
          isbn10 = table_content.find('td').text.strip().replace('-','')
        elif table_content.find('th').text.strip() == "ISBN(13桁)":
          isbn13 = table_content.find('td').text.strip().replace('-','')
        elif table_content.find('th').text.strip() == "本タイトル":
          title = table_content.find('td').text.strip().replace('-','')
      ## タイトルが見つからないか、ISBNが10桁も13桁も見つからない場合はエラー
      if (title is None) or (isbn10 is None and isbn13 is None):
        raise Exception("Error. Cannot get book infomation (title={title}, isbn10={isbn10}, isbn13={isbn13})")
      else:
        ## ISBNの10桁と13桁が両方存在する場合は13桁の方を選択する
        isbn = isbn10 if isbn13 is None else isbn13
      return title, isbn
    
    def get_each_book_info(self, bookid : int, listtype : str) -> str:
      logging.info(f"IchikawaModule::get_each_book_info (bookid={bookid}, listtype={listtype}) called")
      time.sleep(self.sleeptime)
      r = self.session.get('%s/%s-detail.do'%(self.URL_booklist,listtype),headers=self.header,cookies=self.cookie, params={'idx':'%d'%(bookid%10)})
      time.sleep(self.sleeptime)
      r = self.session.get('%s/switch-detail.do'%self.URL_booklist, headers=self.header, cookies=self.cookie, params={'idx':'0'}) ## switch-detailの画面には常に本が1冊しか表示されないので、idx=0でOK
      return r.text
    
    def close_session(self):
      logging.info("IchikawaModule::close_session called")
      ### ログアウトして、sessionを終了して終わる
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_logout, headers=self.header, cookies=self.cookie)
      self.session.close()

    def reserve_book(self, ISBNlist=[]):

        print("reserve_book start")
        print(ISBNlist)
        ## 0~2. ログイン処理
        self.session = self.execute_login_procedure()
        
        ## 3. 詳細検索ページに移動
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_search, headers=self.header, cookies=self.cookie)

        ## 4. 資料の検索
        for isbn in ISBNlist:
            time.sleep(self.sleeptime)
            self.set_isbn_to_params(isbn)
            r = self.session.get(self.URL_search, headers=self.header, cookies=self.cookie, params=self.search_params)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            searchlistnum_text = soup.find(id='main').find(class_='nav-hdg').text
            ### 検索した本がない場合はエラーを返して終了
            if searchlistnum_text.strip() == '該当するリストが存在しません。':
                print("Error. Target book not found in the library database.")
                sys.exit()
            searchlistnum=int(re.search('（全([0-9]+) 件）' ,searchlistnum_text.strip())[1])
            ##  1 ～ 1 件（全1 件）-> 1
            
            ## 5. 予約画面に遷移
            time.sleep(self.sleeptime)
            self.header['Referer']='https://www.library.city.ichikawa.lg.jp/winj/opac/search-detail.do'
            r = self.session.get(self.URL_reserve, headers=self.header, cookies=self.cookie, params=self.reserve_params)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            chunkvalue=soup.find(class_='list-book result hook-check-all').find('input')['value'] ## ex.'1102535405'

            ## 6. 予約バスケット画面に遷移
            time.sleep(self.sleeptime)
            self.basket_submit_params['chk_check']=chunkvalue
            r = self.session.post(self.URL_basket, headers=self.header, cookies=self.cookie, data=self.basket_submit_params)
                
            ## 7. 予約完了
            time.sleep(self.sleeptime)
            r = self.session.post(self.URL_confirm, headers=self.header, cookies=self.cookie, data=self.confirm_params)

            self.session.close()

            ### 8. 予約できているか確認
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            result=soup.find('div', id='main').find('form').find('p').text
            if (self.debug): print(result)
            if (result=='以下のタイトルについて予約を行いました。'):
                print('Reservation succeeded!')
            else:
                for f in soup.find('div', class_='report').find_all('p'):
                    if( re.search('理由',f.text) is not None):
                        reasontext=f.text ## ex. '理由:既に予約済です。'
                        break
                print('Reservation denied. (%s)'%reasontext)

            ### ログアウトして、sessionを終了して終わる
            r = self.session.get(self.URL_logout, headers=self.header, cookies=self.cookie)
            self.session.close()
            return

    ### 条件を満たした資料に関して予約延長申請を行う
    def extend_reservation_day_if_satisfied_condition(self):
        logging.info("extend_reservation_day_if_satisfied_condition called")
        ## 0~2. ログイン処理
        session = self.execute_login_procedure()
                
        ## 3. 貸し出し状況一覧のページに移動
        time.sleep(self.sleeptime)
        r = session.get(self.URL_lend, headers=self.header)
        soup = bs4.BeautifulSoup(r.text, "html5lib")
        with open('out.html', 'w') as file:
            file.write(r.text)
        h2_in_soup = soup.find('h2', class_='nav-hdg')
        if h2_in_soup == None:
            logging.info("No book was found as rental status. Skip the following process.")
            ### ログアウトして、sessionを終了して終わる
            r = session.get(self.URL_logout, headers=self.header, cookies=self.cookie)
            session.close()
            return
        
        totalnum_text = h2_in_soup.text
        if (self.debug): print('totalnum_text=%s'%totalnum_text)
        totalnum = int(re.search('（全([0-9]+) 件）',totalnum_text)[1])
        if (self.debug): print('totalnum=%d'%totalnum)

        ## 予約延長申請をすると本の順番が変わってしまうことへの対策として
        ## 予約延長申請した場合はbookid = 0に戻してループを繰り返す
        bookid = 0
        while bookid < totalnum:
            print('============')
            if (self.debug): print('bookID=%d'%bookid)
            time.sleep(self.sleeptime)

            ### 返却日時を取得
            returndatetime = get_return_date_datetime_per_book(soup,bookid)
            ### 返却日までの日数を計算
            todaydatetime = datetime.date.today()
            remainday = (returndatetime - todaydatetime).days
            if (self.debug): print("remain day = %d days"%(remainday))
            ### 貸出延長可能か確認
            enableextension = get_extension_status_per_book(soup,bookid)
            if (self.debug): print("enableextension=%d"%enableextension)
            
            ### 返却日当日 & 貸出延長可能 の場合は、貸出延長ボタンを押す
            if (remainday==0 and enableextension):
                print('bookdID=%d return day will be extended.'%bookid)
                self.extend_params['idx']='%d'%bookid
                time.sleep(self.sleeptime)
                r = session.get(self.URL_lend, headers=self.header, cookies=self.cookie, params=self.extend_params) ## 貸出延長ボタンを押す
                time.sleep(self.sleeptime)
                ### hid_lenid (ex. 0001691493) を取得しparamに詰める
                inputlist=bs4.BeautifulSoup(r.text, "html5lib").find('div', id='main').find_all('input')
                hid_lenid=[ilist['value'] for ilist in inputlist if ilist['name']=='hid_lenid'][0]
                if (self.debug): print(hid_lenid)
                self.extend_confirm_params['hid_lenid']=hid_lenid
                r = session.get(self.URL_extend,headers=self.header, cookies=self.cookie, params=self.extend_confirm_params) ## 貸出延長承認を確認
                result=bs4.BeautifulSoup(r.text, "html5lib").find('div', id='main').text
                if (self.debug): print(result)
                if (re.search('貸出延長申込が完了しました',result) is not None):
                    print('Lending day extenstion succeeded!')
                else:
                    print('Error. Lending day extension failed.')
                    bookid += 1 ## エラーが起きた場合は次に進む
                    time.sleep(self.sleeptime)

            else:
                bookid += 1
            ## 貸出一覧ページに戻る
            r = session.get(self.URL_lend, headers=self.header, cookies=self.cookie)
                
        ### ログアウトして、sessionを終了して終わる
        r = session.get(self.URL_logout, headers=self.header, cookies=self.cookie)
        session.close()
        return

    ### 予約カゴを空にする
    def clean_reserve_busket(self):

        ## 0~2. ログイン処理
        session = self.execute_login_procedure()
                
        ## 3. 予約カゴページに移動
        time.sleep(self.sleeptime)
        r = session.get(self.URL_basket, headers=self.header, cookies=self.cookie)
        soup = bs4.BeautifulSoup(r.text, "html5lib")

        
        ## 予約カゴに入っている書籍冊数を取得
        totalnum_basket_text = soup.find_all("form")[1].find_all('font', attrs={'color':'red'})[0].text
        if (self.debug): print('totalnum_basket_text=%s'%totalnum_basket_text)
        totalnum_basket = int(re.search('該当件数は([0-9]+)件です',totalnum_basket_text).group(1))
        if (self.debug): print('totalnum_basket=%d'%totalnum_basket)

        ## 予約カゴに入っている書籍冊数が0であれば以降の処理をスキップ
        if totalnum_basket==0:
            if (self.debug): print("No book is found in reserve book basket")

        else:
            if (self.debug):
                print("Some books are found in reserve book basket")
                print("Try to delete books from basket")
            
            ## 予約カゴに入っている書籍のchunk_valueを取得
            chunk_value_list = []
            chunk_value_string = ""
            for i in range(totalnum_basket):
                chunk_value = soup.find('ol', class_="list-book result hook-check-all").find_all('label')[i].find('input')['value']
                chunk_value_list.append(chunk_value)
                chunk_value_string += "%s "%chunk_value_string
            self.basket_delete_params['chk_check']=chunk_value_list
            chunk_value_string = chunk_value_string.rstrip(" ") ## 最後のスペースを削除
            self.basket_delete_confirm_params['hid_idlist']=chunk_value_string

            ## 4. 予約カゴを空にする
            time.sleep(self.sleeptime)
            r = session.post(self.URL_basket, headers=self.header, cookies=self.cookie, data=self.basket_delete_params)

            ## 5. 予約カゴ削除の確認ボタンを押す
            time.sleep(self.sleeptime)
            r = session.post(self.URL_basket_delete, headers=self.header, cookies=self.cookie, data=self.basket_delete_confirm_params)
            print("Reserve basket cleared")
            
            ## 6. 予約カゴページに移動
            time.sleep(self.sleeptime)
            r = session.get(self.URL_basket, headers=self.header, cookies=self.cookie)
            soup = bs4.BeautifulSoup(r.text, "html5lib")
        
            ## 予約カゴに入っている書籍冊数を取得
            totalnum_basket_text = soup.find_all("form")[1].find_all('font', attrs={'color':'red'})[0].text
            if (self.debug): print('totalnum_basket_text=%s'%totalnum_basket_text)
            totalnum_basket = int(re.search('該当件数は([0-9]+)件です',totalnum_basket_text).group(1))
            if (self.debug): print('totalnum_basket=%d'%totalnum_basket)

        ### 7. ログアウトして、sessionを終了して終わる
        time.sleep(self.sleeptime)
        r = session.get(self.URL_logout, headers=self.header, cookies=self.cookie)
        session.close()
        return
