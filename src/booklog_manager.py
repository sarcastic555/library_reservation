# -*- coding: utf-8 -*-
import datetime
import logging.config
import os
import re
import time

import bs4
import requests

logging.config.fileConfig("../log.conf")


class BooklogManager:
  login_URL = 'https://booklog.jp/login'
  export_URL = 'https://booklog.jp/export'
  download_URL = 'https://download.booklog.jp/shelf/csv?signature={}'
  logout_URL = 'https://booklog.jp/logout'

  def __init__(self, sleep_time=3):
    logging.debug("BooklogManager constructore called")
    self.sleep_time = sleep_time  # [sec]
    self.booklog_id = os.environ['BOOKLOG_ID']
    self.booklog_pass = os.environ['BOOKLOG_PASSWORD']

    self.session = requests.session()
    ## create session ID
    ## php_session_idは同じものを複数使うと（かつそのセッションをクローズしないと？未確認）
    ## 2回目以降ログインできなくなるため現在時刻を代入し重複が発生しないようにする
    now = datetime.datetime.now()
    self.session_id = str(int(now.timestamp()))
    logging.debug(f"session_id = {self.session_id}")

    self.login_header = self.generate_login_header(self.session_id)
    self.login_data = self.generate_login_data(self.booklog_id, self.booklog_pass)

    self.login()

  def generate_login_header(self, session_id) -> dict:
    header = {}
    header['cookie'] = f"PHPSESSID={session_id}"
    header['referer'] = self.__class__.login_URL
    return header

  def generate_login_data(self, account, password) -> dict:
    data = {}
    data['service'] = 'booklog'
    data['ref'] = ''
    data['account'] = account
    data['password'] = password
    return data

  def login(self) -> None:
    logging.debug("BooklogManager::login called")
    time.sleep(self.sleep_time)
    self.session.get(self.__class__.login_URL)
    time.sleep(self.sleep_time)
    self.session.post(self.__class__.login_URL,
                      headers=self.login_header,
                      data=self.login_data,
                      allow_redirects=True)

  def get_signature(self) -> str:
    logging.debug("BooklogManager::get_signature called")
    time.sleep(self.sleep_time)
    r = self.session.get(self.__class__.export_URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    button = soup.find(class_='buttons')
    ## signatureを返す(ボタンにリンクとして埋め込まれている)
    signature = re.search('.*signature=(.*)', button.find('a')['href'])[1]
    logging.debug(f"signature={signature}")
    return signature

  def download_csv_file(self) -> str:
    logging.debug("BooklogManager::download_csv_file called")
    signature = self.get_signature()
    ## csvデータとして取得
    time.sleep(self.sleep_time)
    r = self.session.get(self.__class__.download_URL.format(signature))
    r.encoding = 'Shift_JIS'  ## これがないと文字化けする
    return r.text

  def logout(self) -> None:
    logging.debug("BooklogManager::logout called")
    ## ログアウト
    time.sleep(self.sleep_time)
    r = self.session.get(self.__class__.logout_URL,
                         headers={'cookie': 'PHPSESSID=' + self.session_id})
    r.close()

  def __del__(self):
    self.logout()
