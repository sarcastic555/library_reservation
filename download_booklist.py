# -*- coding: utf-8 -*-                                                                                                
import time
import datetime
import sys
import os
import requests
import codecs
import csv

booklogID = "ngkqnok"
booklogPass = 'ngkqnok555'
login_URL='https://booklog.jp/login'
php_session_id = "35b71f9e203f0c9b87068a8d59a56514"

os.system('rm list/alllist.csv') ## delete old csv files
_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('download_booklist.py start!')

data_login={
    'service': 'booklog',
    'ref': '',
    'account': 'ngkqnok',
    'password': 'ngkqnok555'
}
session = requests.session()

## ログイン
r = session.get(login_URL)
r = session.post(login_URL, headers={'cookie': 'PHPSESSID='+php_session_id, 'referer': login_URL}, data=data_login, allow_redirects=False) ## cookie(ハードコードで良さそう)とrefererをつけないとcsvが取得できない

## csv取得
r = session.get('https://booklog.jp/export/csv')
#print(r.encoding)
r.encoding = 'Shift_JIS' ## これがないと文字化けする
print(r.text[:300]) ### 全て出力するとあふれるので最初の100文字だけ出力
print(r.text, file=codecs.open('list/alllist.csv', 'w', 'utf-8'))

## ログアウト
r = session.get('https://booklog.jp/logout', headers={'cookie': 'PHPSESSID='+php_session_id})
r.close()

## 結果出力
print ('download_booklist.py end!')
_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
