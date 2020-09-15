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
import warnings

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s : %(asctime)s : %(message)s')


class IchikawaModule:
    def __init__(self):
        self.debug=False
        self.ID='7093281'
        self.password='ngkrnok555'
        self.sleeptime=3 ## sleeping time [sec]
        self.URL_booklist='https://www.library.city.ichikawa.lg.jp/winj/opac/'
        self.URL_entrance='https://www.library.city.ichikawa.lg.jp/winj/opac/top.do'
        self.URL_loginpage='https://www.library.city.ichikawa.lg.jp/winj/opac/login.do'
        self.URL_toppage='https://www.library.city.ichikawa.lg.jp/winj/opac/login.do'
        self.URL_search='https://www.library.city.ichikawa.lg.jp/winj/opac/search-detail.do'
        self.URL_reserve='https://www.library.city.ichikawa.lg.jp/winj/opac/search-list.do'
        self.URL_lend_list='https://www.library.city.ichikawa.lg.jp/winj/opac/lend-list.do'
        self.URL_reserve_list='https://www.library.city.ichikawa.lg.jp/winj/opac/reserve-list.do'
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
            'Origin': 'https://www.library.city.ichikawa.lg.jp',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
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
      r = self.session.get(self.URL_lend_list, headers=self.header)
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
      r = self.session.get(self.URL_lend_list, headers=self.header)
      soup = bs4.BeautifulSoup(r.text, "html5lib")
      detail_content=soup.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')
      info = detail_content[bookid].find('div', class_='column info').find_all('p')[3].find('b').text.strip()
      year  = int(re.search('([0-9]+)/[0-9]+/[0-9]+',info)[1])
      month = int(re.search('[0-9]+/([0-9]+)/[0-9]+',info)[1])
      day   = int(re.search('[0-9]+/[0-9]+/([0-9]+)',info)[1])
      return datetime.date(year,month,day)

    ## マイページの予約一覧のHTMLを読み込んで、本のstatus(予約順位とか)を返す関数
    def get_book_reserve_status_per_book(self, bookid):
      logging.info(f"IchikawaModule::get_book_reserve_status_per_book (bookid={bookid}) called")
      if (bookid <= 9):
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_reserve_list, headers=self.header)
      elif (bookid >= 10):
        ## ページが変わる場合は次ページ情報を読み込む
        page = str(int(bookid / 10) + 1)
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_reserve_list, headers=self.header, params={'page': page})
      soup_list = bs4.BeautifulSoup(r.text, "html5lib")
      hoge = soup_list.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')[bookid%10]
      try:
        status = soup_list.find('ol', class_='list-book result hook-check-all').find_all('div', class_='lyt-image image-small')[bookid%10].find('div', class_='column info').find_all('p')[2].text.strip()
        status = "error" if status == "" else status
      except:        
        status = "error"
      return status
        
    def get_sessionid_from_header(self, headers):
        return headers['Set-Cookie'].split(";")[0][11:] ## 頭の"JSESSIONID="を削除する

    def set_isbn_to_params(self, isbn):
        self.search_params['txt_code']=isbn

    def execute_login_procedure(self):
        self.session = requests.session()

        ### 0. 図書館トップ画面に移動
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_entrance)
        self.header['Referer'] = self.URL_entrance
        sessionid_string = self.get_sessionid_from_header(r.headers)
        self.register_sessionID(sessionid_string)
        
        ### 1. ログイン画面に入る
        time.sleep(self.sleeptime)
        r = self.session.get(self.URL_loginpage, headers=self.header)
        self.header['Referer'] = self.URL_loginpage

        ## 2. ログイン処理
        data={
            'txt_usercd': self.ID,
            'txt_password': self.password,
            'submit_btn_login': 'ログイン(認証)'
        }
        ### allow_redirects=Falseのオプションをつけないとヘッダからクッキーが取得できない
        time.sleep(self.sleeptime)
        r = self.session.post(self.URL_loginpage, headers=self.header, data=data, allow_redirects=False)
        self.header['Referer'] = self.URL_loginpage
        sessionid_string = self.get_sessionid_from_header(r.headers)
        self.register_sessionID(sessionid_string)

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

    def get_num_of_reserve_basket_books(self) -> int:
      logging.info(f"IchikawaModule::get_num_of_reserve_basket_books called")
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_basket, headers=self.header)
      soup = bs4.BeautifulSoup(r.text, "html5lib")

      ## 予約カゴに入っている書籍冊数を取得
      totalnum_text = soup.find_all("form")[1].find_all('font', attrs={'color':'red'})[0].text
      logging.debug(f'totalnum_basket_text = {totalnum_text}')
      totalnum = int(re.search('該当件数は([0-9]+)件です',totalnum_text).group(1))
      return totalnum

    def clear_reserve_basket(self):
      logging.info("IchikawaModule::clear_reserve_basket called")
      time.sleep(self.sleeptime)
      r = session.post(self.URL_basket, headers=self.header, data=self.basket_delete_params)

    def get_title_and_isbn_from_book_info(self, bookid, listtype):
      logging.info(f"IchikawaModule::get_title_and_isbn_from_book_info (bookid={bookid}, listtype={listtype}) called")
      time.sleep(self.sleeptime)
      r = self.session.get('%s/%s-detail.do'%(self.URL_booklist,listtype),headers=self.header, params={'idx':'%d'%(bookid%10)})
      time.sleep(self.sleeptime)
      ## switch-detailの画面には常に本が1冊しか表示されないので、idx=0でOK
      r = self.session.get('%s/switch-detail.do'%self.URL_booklist, headers=self.header, params={'idx':'0'})
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
      r = self.session.get('%s/%s-detail.do'%(self.URL_booklist,listtype),headers=self.header, params={'idx':'%d'%(bookid%10)})
      time.sleep(self.sleeptime)
      r = self.session.get('%s/switch-detail.do'%self.URL_booklist, headers=self.header, params={'idx':'0'}) ## switch-detailの画面には常に本が1冊しか表示されないので、idx=0でOK
      return r.text

    def reserve_book(self, isbn : str) -> bool:
      logging.info(f"IchikawaModule: reserve_book (isbn = {isbn}) called")
      if (type(isbn) != str):
        raise TypeError("str is expected as type of isbn, but it is %s" % type(isbn))

      ## 詳細検索ページに移動
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_search, headers=self.header)
      self.header['Referer'] = self.URL_search
      self.search_params['txt_code'] = isbn

      # 検索処理を実行
      time.sleep(self.sleeptime)
      r = self.session.post(self.URL_search, headers=self.header, params=self.search_params)
      self.header['Referer'] = self.URL_search
      soup = bs4.BeautifulSoup(r.text, "html.parser")
      searchlistnum_text = soup.find(id='main').find(class_='nav-hdg').text
      ### 検索した本がない場合はエラーを返して終了
      if searchlistnum_text.strip() == '該当するリストが存在しません。':
        warnings.wanr(f"Target book (isbn = {isbn}) not found in the library database.")
        return False
      ##  1 ～ 1 件（全1 件）-> 1
      searchlistnum=int(re.search('（全([0-9]+) 件）' ,searchlistnum_text.strip())[1])

      # 予約画面に遷移
      time.sleep(self.sleeptime)
      r = self.session.post(self.URL_reserve, headers=self.header, params=self.reserve_params)
      self.header['Referer'] = self.URL_reserve
      soup = bs4.BeautifulSoup(r.text, "html.parser")
      chunkvalue=soup.find(class_='list-book result hook-check-all').find('input')['value'] ## ex.'1102535405'

      # 予約バスケット画面に遷移
      self.basket_submit_params['chk_check']=chunkvalue
      time.sleep(self.sleeptime)
      r = self.session.post(self.URL_basket, headers=self.header, data=self.basket_submit_params)
      self.header['Referer'] = self.URL_basket

      ## 予約実施
      time.sleep(self.sleeptime)
      r = self.session.post(self.URL_confirm, headers=self.header, data=self.confirm_params)

      ### 結果の確認
      soup = bs4.BeautifulSoup(r.text, "html.parser")
      #print(r.text)
      result = soup.find('div', id='main').find('form').find('p').text
      #print(result)
      if (result == '以下のタイトルについて予約を行いました。'):
        logging.info(f'Reservation succeeded for book {isbn}!')
        return True
      else:
        for f in soup.find('div', class_='report').find_all('p'):
          if( re.search('理由',f.text) is not None):
            reasontext=f.text ## ex. '理由:既に予約済です。'
            warnings.warn(f"Reservation denied: {reasontext}")
            break
        return False


    def close_session(self):
      logging.info("IchikawaModule::close_session called")
      ### ログアウトして、sessionを終了して終わる
      time.sleep(self.sleeptime)
      r = self.session.get(self.URL_logout, headers=self.header)
      self.session.close()

