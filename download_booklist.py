# -*- coding: utf-8 -*-                                                                                                
import bs4
import re
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
export_URL='https://booklog.jp/export'
download_url='https://download.booklog.jp/shelf/csv?signature={}'
## delete old csv files
if os.path.exists("list/alllist.csv"):
    os.system('rm list/alllist.csv')
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

## create session ID
## php_session_idは同じものを複数使うと（かつそのセッションをクローズしないと？未確認）
## 2回目以降ログインできなくなるため現在時刻を代入し重複が発生しないようにする
php_session_id = str(int(_nowtime.timestamp()))
print("php_session_id")
print(php_session_id)

## ログイン
r = session.get(login_URL)
r = session.post(login_URL, headers={'cookie': 'PHPSESSID='+php_session_id, 'referer': login_URL}, data=data_login, allow_redirects=True) ## cookie(ハードコードで良さそう)とrefererが必須
with open('out1.html', mode='w', encoding = 'utf-8') as fw:
    fw.write(r.text)

## signature取得(ボタンにリンクとして埋め込まれている)
r = session.get(export_URL)
soup = bs4.BeautifulSoup(r.text, 'html.parser')
button = soup.find(class_='buttons')
signature = re.search('.*signature=(.*)', button.find('a')['href'])[1]
print(signature)

## csvダウンロード
r = session.get(download_url.format(signature))
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
