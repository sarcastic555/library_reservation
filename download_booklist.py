# -*- coding: utf-8 -*-                                                                                                
import codecs
import csv
import datetime
import logging
import os
import re
import sys
import time

import bs4
import requests


class BooklogManager:
    login_URL='https://booklog.jp/login'
    export_URL='https://booklog.jp/export'
    download_URL='https://download.booklog.jp/shelf/csv?signature={}'
    logout_URL='https://booklog.jp/logout'

    def __init__(self):
        logging.info("BooklogManager constructore called")
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
        self.signature = None

    def generate_login_header(self, session_id):
        header = {}
        header['cookie'] = f"PHPSESSID={session_id}"
        header['referer'] = self.__class__.login_URL
        return header

    def generate_login_data(self, account, password):
        data = {}
        data['service'] = 'booklog'
        data['ref'] = ''
        data['account'] = account
        data['password'] = password
        return data

    def login(self):
        logging.info("BooklogManager::login called")
        self.session.get(self.__class__.login_URL)
        self.session.post(self.__class__.login_URL, headers=self.login_header, data=self.login_data, allow_redirects=True)

    def set_signature(self):
        logging.info("BooklogManager::set_signature called")
        r = self.session.get(self.__class__.export_URL)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        button = soup.find(class_='buttons')
        ## signature取得(ボタンにリンクとして埋め込まれている)
        self.signature = re.search('.*signature=(.*)', button.find('a')['href'])[1]
        logging.debug(f"signature={self.signature}")

    def download_csv_file(self, outfile_name):
        logging.info("BooklogManager::download_csv_file called")
        ## csvダウンロード
        r = self.session.get(self.__class__.download_URL.format(self.signature))
        r.encoding = 'Shift_JIS' ## これがないと文字化けする
        logging.debug(r.text[:300]) ### 全て出力するとあふれるので最初の100文字だけ出力
        if os.path.exists(outfile_name):
            logging.info(f"rm {outfile_name}")
            os.remove(outfile_name)
        print(r.text, file=codecs.open(outfile_name, 'w', 'utf-8'))

    def logout(self):
        logging.info("BooklogManager::logout called")
        ## ログアウト
        r = self.session.get(self.__class__.logout_URL, headers={'cookie': 'PHPSESSID='+self.session_id})
        r.close()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s : %(asctime)s : %(message)s')

    logging.info('download_booklist.py start')
    booklog_manager = BooklogManager()
    booklog_manager.login()
    booklog_manager.set_signature()
    booklog_manager.download_csv_file("list/alllist.csv")
    booklog_manager.logout()
    logging.info('download_booklist.py end')

if __name__ == "__main__":
    main()
