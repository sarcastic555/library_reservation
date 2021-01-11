# /usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging
import os
import re
import time
import warnings
from typing import Dict, Tuple

import bs4
import requests

from tools.book_info import RentalBookInfo, ReserveBookInfo
from tools.ichikawa_data.header_param_info import HeaderParamInfo
from tools.ichikawa_data.ichikawa_url import IchikawaURL

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


class IchikawaModule:

  def __init__(self, sleep=3):
    self.ID = os.environ["ICHIKAWA_LIBRARY_ID"]
    self.password = os.environ["ICHIKAWA_LIBRARY_PASSWORD"]
    self.sleeptime = sleep  ## sleeping time [sec]

    # ヘッダーやパラム情報は（ログインデータ以外は）データファイルから読み出す
    self.login_data = {
        'txt_usercd': self.ID,
        'txt_password': self.password,
        'submit_btn_login': 'ログイン(認証)'
    }
    self.header = HeaderParamInfo.header
    self.search_params = HeaderParamInfo.search_params
    self.reserve_params = HeaderParamInfo.reserve_params
    self.basket_submit_params = HeaderParamInfo.basket_submit_params
    self.basket_delete_params = HeaderParamInfo.basket_delete_confirm_params
    self.basket_delete_confirm_params = HeaderParamInfo.basket_delete_confirm_params
    self.confirm_params = HeaderParamInfo.confirm_params
    self.mypage_params = HeaderParamInfo.mypage_params
    self.extend_params = HeaderParamInfo.extend_params
    self.extend_confirm_params = HeaderParamInfo.extend_params

    ## ログイン処理はコンストラクタで実行
    self.execute_login_procedure()

  def register_sessionID(self, sessionID_string: str) -> None:
    self.header['Cookie'] = f"JSESSIONID={sessionID_string}"
    self.reserve_params['hid_session'] = sessionID_string
    self.basket_submit_params['hid_session'] = sessionID_string
    self.basket_delete_params['hid_session'] = sessionID_string
    self.basket_delete_confirm_params['hid_session'] = sessionID_string
    self.confirm_params['hid_session'] = sessionID_string
    self.extend_params['hid_session'] = sessionID_string
    self.extend_confirm_params['hid_session'] = sessionID_string

  ## 貸し出し中の本の情報を取得する
  def get_rental_book_information(self, bookid: int) -> RentalBookInfo:
    logging.info(f"IchikawaModule::get_rental_book_information (bookid = {bookid}) called")
    info = RentalBookInfo()
    info.book_id = bookid
    info.title, info.isbn = self.get_title_and_isbn_from_book_info(bookid, "lend")
    info.can_rental_extension = self.get_extension_status_per_book(bookid)
    info.return_datetime_before_extension = self.get_return_date_datetime_per_book(bookid)
    if info.can_rental_extension:
      info.return_datetime_after_extension = info.return_datetime_before_extension + datetime.timedelta(
          days=14)
    else:
      info.return_datetime_after_extension = info.return_datetime_before_extension
    return info

  ## 予約中の本の情報を取得する
  def get_under_reservation_book_information(self, bookid: int) -> ReserveBookInfo:
    logging.info(
        f"IchikawaModule::get_under_reservation_book_information (bookid = {bookid}) called")
    info = ReserveBookInfo()
    info.title, info.isbn = self.get_title_and_isbn_from_book_info(bookid, "reserve")
    info.reserve_status = self.get_book_reserve_status_per_book(bookid)
    return info

  ## マイページのHTMLを読み込んで、bookIDに対応する本が貸出延長可能かどうか判定する関数
  ## 各資料の詳細ページからは判定できないので、貸し出し一覧ページから情報を取得する
  def get_extension_status_per_book(self, bookid: int) -> bool:
    logging.info(f"IchikawaModule::get_extension_status_per_book (bookid = {bookid}) called")
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.lend_list, headers=self.header)
    soup = bs4.BeautifulSoup(r.text, "html5lib")
    extendbutton_content = soup.find('ol', class_='list-book result hook-check-all').find_all(
        'div', class_='info')
    ### class='column info'(本の詳細情報)とclass='info'(延長ボタン情報)の2つが取られてしまうので、あとで2*i+1番目を指定するようにする
    ### 貸出延長可能かチェック(延長ボタンがないと、rightbutton=Noneとなる)
    rightbutton = extendbutton_content[2 * bookid + 1].find('a')
    enableextension = False
    if rightbutton is not None:
      enableextension = True
    return enableextension

  ### マイページのHTMLを読み込んで、bookIDに対応する返却日をdatetimeで返す関数
  def get_return_date_datetime_per_book(self, bookid: int) -> datetime:
    logging.info(f"IchikawaModule::get_return_date_datetime_per_book (bookid = {bookid}) called")
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.lend_list, headers=self.header)
    soup = bs4.BeautifulSoup(r.text, "html5lib")
    detail_content = soup.find('ol', class_='list-book result hook-check-all').find_all(
        'div', class_='lyt-image image-small')
    info = detail_content[bookid].find(
        'div', class_='column info').find_all('p')[3].find('b').text.strip()
    year = int(re.search('([0-9]+)/[0-9]+/[0-9]+', info)[1])
    month = int(re.search('[0-9]+/([0-9]+)/[0-9]+', info)[1])
    day = int(re.search('[0-9]+/[0-9]+/([0-9]+)', info)[1])
    return datetime.date(year, month, day)

  ## マイページの予約一覧のHTMLを読み込んで、本のstatus(予約順位とか)を返す関数
  def get_book_reserve_status_per_book(self, bookid: int) -> str:
    logging.info(f"IchikawaModule::get_book_reserve_status_per_book (bookid={bookid}) called")
    if (bookid <= 9):
      time.sleep(self.sleeptime)
      r = self.session.get(IchikawaURL.reserve_list, headers=self.header)
    elif (bookid >= 10):
      ## ページが変わる場合は次ページ情報を読み込む
      page = str(int(bookid / 10) + 1)
      time.sleep(self.sleeptime)
      r = self.session.get(IchikawaURL.reserve_list, headers=self.header, params={'page': page})
    soup_list = bs4.BeautifulSoup(r.text, "html5lib")
    try:
      status = soup_list.find('ol', class_='list-book result hook-check-all').find_all(
          'div', class_='lyt-image image-small')[bookid % 10].find(
              'div', class_='column info').find_all('p')[2].text.strip()
      status = "error" if status == "" else status
    except:
      status = "error"
    return status

  def get_sessionid_from_header(self, headers: Dict) -> str:
    return headers['Set-Cookie'].split(";")[0][11:]  ## 頭の"JSESSIONID="を削除する

  def set_isbn_to_params(self, isbn: str) -> None:
    self.search_params['txt_code'] = isbn

  def execute_login_procedure(self) -> None:
    self.session = requests.session()

    ### 図書館トップ画面に移動
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.entrance)
    self.header['Referer'] = IchikawaURL.entrance
    sessionid_string = self.get_sessionid_from_header(r.headers)
    self.register_sessionID(sessionid_string)

    ### ログイン画面に入る
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.loginpage, headers=self.header)
    self.header['Referer'] = IchikawaURL.loginpage

    ## ログイン処理
    time.sleep(self.sleeptime)
    ### allow_redirects=Falseのオプションをつけないとヘッダからクッキーが取得できない
    r = self.session.post(IchikawaURL.loginpage,
                          headers=self.header,
                          data=self.login_data,
                          allow_redirects=False)
    self.header['Referer'] = IchikawaURL.loginpage
    sessionid_string = self.get_sessionid_from_header(r.headers)
    self.register_sessionID(sessionid_string)

  def apply_reserve_extension(self, bookid: int) -> bool:
    logging.info(f"IchikawaModule::apply_reserve_extension (bookid = {bookid}) called")
    self.extend_params['idx'] = '%d' % bookid
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.lend_list, headers=self.header,
                         params=self.extend_params)  ## 貸出延長ボタンを押す
    ### hid_lenid (ex. 0001691493) を取得しparamに詰める
    inputlist = bs4.BeautifulSoup(r.text, "html5lib").find('div', id='main').find_all('input')
    hid_lenid = [ilist['value'] for ilist in inputlist if ilist['name'] == 'hid_lenid'][0]
    logging.debug(f"hid_lenid={hid_lenid}")
    self.extend_confirm_params['hid_lenid'] = hid_lenid
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.extend, headers=self.header,
                         params=self.extend_confirm_params)  ## 貸出延長承認を確認
    result = bs4.BeautifulSoup(r.text, "html5lib").find('div', id='main').text
    if (re.search('貸出延長申込が完了しました', result) is not None):
      return True  ## 成功
    else:
      return False  ## 失敗

  def get_num_of_total_books(self, listtype: str) -> int:
    logging.info(f"IchikawaModule::get_num_of_total_books ({listtype}) called")
    time.sleep(self.sleeptime)
    r = self.session.get('%s/%s-list.do' % (IchikawaURL.booklist, listtype), headers=self.header)
    soup_list = bs4.BeautifulSoup(r.text, "html5lib")
    h2_in_soup = soup_list.find('h2', class_='nav-hdg')
    if h2_in_soup == None:
      return 0
    totalnum_text = h2_in_soup.text
    logging.debug(f"totalnum_text = {totalnum_text}")
    totalnum = int(re.search('（全([0-9]+) 件）', totalnum_text)[1])
    return totalnum

  def get_num_of_reserve_basket_books(self) -> int:
    logging.info("IchikawaModule::get_num_of_reserve_basket_books called")
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.basket, headers=self.header)
    soup = bs4.BeautifulSoup(r.text, "html5lib")

    ## 予約カゴに入っている書籍冊数を取得
    totalnum_text = soup.find_all("form")[1].find_all('font', attrs={'color': 'red'})[0].text
    logging.debug(f'totalnum_basket_text = {totalnum_text}')
    totalnum = int(re.search('該当件数は([0-9]+)件です', totalnum_text).group(1))
    return totalnum

  def clear_reserve_basket(self) -> bool:
    logging.info("IchikawaModule::clear_reserve_basket called")
    ## 予約カゴに入っている本の冊数を取得
    totalnum_basket = self.get_num_of_reserve_basket_books()
    ## 予約カゴに入っている書籍冊数が0であれば終了
    if totalnum_basket == 0:
      logging.info("No book is found in reserve book basket.")
      logging.info("Skip process of clearing reserve basket.")
      return True
    logging.info(f"{totalnum_basket} books are found in reserve book basket.")
    logging.info("Clear reserve book basket.")
    time.sleep(self.sleeptime)
    # 予約カゴに入っている書籍のchunk_valueを取得
    chunk_value_list = []
    chunk_value_string = ""
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.basket, headers=self.header)
    soup = bs4.BeautifulSoup(r.text, "html5lib")
    for i in range(totalnum_basket):
      chunk_value = soup.find(
          'ol',
          class_="list-book result hook-check-all").find_all('label')[i].find('input')['value']
      chunk_value_list.append(chunk_value)
      chunk_value_string += "%s " % chunk_value_string
    self.basket_delete_params['chk_check'] = chunk_value_list
    chunk_value_string = chunk_value_string.rstrip(" ")  ## 最後のスペースを削除
    self.basket_delete_confirm_params['hid_idlist'] = chunk_value_string
    ## 予約カゴを空にする
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.basket, headers=self.header, data=self.basket_delete_params)
    ## 予約カゴ削除の確認ボタンを押す
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.basket_delete,
                          headers=self.header,
                          data=self.basket_delete_confirm_params)

    # 最後に確認のため予約カゴに入っている本の冊数を取得
    totalnum_basket = self.get_num_of_reserve_basket_books()
    if totalnum_basket == 0:
      return True  # 成功
    else:
      return True  # 失敗

  def get_title_and_isbn_from_book_info(self, bookid: int, listtype: str) -> Tuple[str, str]:
    logging.info(
        f"IchikawaModule::get_title_and_isbn_from_book_info (bookid={bookid}, listtype={listtype}) called"
    )
    time.sleep(self.sleeptime)
    r = self.session.get('%s/%s-detail.do' % (IchikawaURL.booklist, listtype),
                         headers=self.header,
                         params={'idx': '%d' % (bookid % 10)})
    time.sleep(self.sleeptime)
    ## switch-detailの画面には常に本が1冊しか表示されないので、idx=0でOK
    r = self.session.get('%s/switch-detail.do' % IchikawaURL.booklist,
                         headers=self.header,
                         params={'idx': '0'})
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    table_contents = soup.find('table', class_='tbl-04').find_all('tr')
    isbn10 = None
    title = None
    isbn13 = None
    for table_content in table_contents:
      if table_content.find('th').text.strip() == "ISBN":
        isbn10 = table_content.find('td').text.strip().replace('-', '')
      elif table_content.find('th').text.strip() == "ISBN(13桁)":
        isbn13 = table_content.find('td').text.strip().replace('-', '')
      elif table_content.find('th').text.strip() == "本タイトル":
        title = table_content.find('td').text.strip().replace('-', '')
    ## タイトルが見つからないか、ISBNが10桁も13桁も見つからない場合はエラー
    if (title is None) or (isbn10 is None and isbn13 is None):
      raise Exception(
          "Error. Cannot get book infomation (title={title}, isbn10={isbn10}, isbn13={isbn13})")
    else:
      ## ISBNの10桁と13桁が両方存在する場合は13桁の方を選択する
      isbn = isbn10 if isbn13 is None else isbn13
    return title, isbn

  def reserve_book(self, isbn: str) -> bool:
    logging.info(f"IchikawaModule: reserve_book (isbn = {isbn}) called")
    if (type(isbn) != str):
      warnings.warn("str is expected as type of isbn, but it is %s" % type(isbn))
      return False
    # 検索システムが完全一致ではなく部分一致で出力してしまうため13桁未満が入力されても結果が出力されることを防ぐ
    if (len(isbn) != 13):
      warnings.warn(f"ISBN (={isbn}) is not 13 digit")
      return False
    ## 詳細検索ページに移動
    time.sleep(self.sleeptime)
    r = self.session.get(IchikawaURL.search, headers=self.header)
    self.header['Referer'] = IchikawaURL.search
    self.search_params['txt_code'] = isbn

    # 検索処理を実行
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.search, headers=self.header, params=self.search_params)
    self.header['Referer'] = IchikawaURL.search
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    searchlistnum_text = soup.find(id='main').find(class_='nav-hdg').text
    ### 検索した本がない場合はエラーを返して終了
    if searchlistnum_text.strip() == '該当するリストが存在しません。':
      warnings.warn(f"Target book (isbn = {isbn}) not found in the library database.")
      return False
    ##  1 ～ 1 件（全1 件）-> 1
    searchlistnum = int(re.search('（全([0-9]+) 件）', searchlistnum_text.strip())[1])
    logging.info(f"{searchlistnum} books are found in total.")

    # 予約画面に遷移
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.reserve, headers=self.header, params=self.reserve_params)
    self.header['Referer'] = IchikawaURL.reserve
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    chunkvalue = soup.find(
        class_='list-book result hook-check-all').find('input')['value']  ## ex.'1102535405'

    # 予約バスケット画面に遷移
    self.basket_submit_params['chk_check'] = chunkvalue
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.basket, headers=self.header, data=self.basket_submit_params)
    self.header['Referer'] = IchikawaURL.basket

    ## 予約実施
    time.sleep(self.sleeptime)
    r = self.session.post(IchikawaURL.confirm, headers=self.header, data=self.confirm_params)

    ### 結果の確認
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    result = soup.find('div', id='main').find('form').find('p').text
    if (result == '以下のタイトルについて予約を行いました。'):
      logging.info(f'Reservation succeeded for book {isbn}!')
      return True
    else:
      for f in soup.find('div', class_='report').find_all('p'):
        if (re.search('理由', f.text) is not None):
          reasontext = f.text  ## ex. '理由:既に予約済です。'
          warnings.warn(f"Reservation denied: {reasontext}")
          break
      return False

  def close_session(self) -> None:
    logging.info("IchikawaModule::close_session called")
    ### ログアウトして、sessionを終了して終わる
    time.sleep(self.sleeptime)
    self.session.get(IchikawaURL.logout, headers=self.header)
    self.session.close()

  def __del__(self):
    self.close_session()
