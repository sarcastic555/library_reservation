# /usr/local/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
import codecs

sleeptime=3 ## sleeping time [sec]
ID='7093281'
PASSWORD='ngkrnok555'

## login library user page
_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('program start!')

### 0. 市川市立図書館トップ画面
URL='https://www.library.city.ichikawa.lg.jp/winj/opac/top.do'
header={
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
session = requests.session()
time.sleep(sleeptime)
r = session.get(URL, headers=header)
mycookie = dict(JSESSIONID=r.cookies.get('JSESSIONID'))
sessionid_string=r.headers['Set-Cookie'].split(";")[0] ### ex. JSESSIONID=029F281FC7088253A80164DDC579644F
print("sessionid_string=%s"%sessionid_string)
print("======= 0. enter login page start ========")
print(r.text, file=codecs.open('tmp/dump0.html', 'w', 'utf-8'))
print("======= 0. enter login page end ==========")

### 1. ログイン画面に入る
URL='https://www.library.city.ichikawa.lg.jp/winj/opac/login.do;%s'%sessionid_string
header={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
#    "Cookie": "JSESSIONID=9004CF29BF5A0CD20606ECD19A9A7D33; _ga=GA1.3.665443413.1553500376",
    "Cookie": sessionid_string,
    "Host": "www.library.city.ichikawa.lg.jp",
    "Referer": "http://www.city.ichikawa.lg.jp/library/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.3"
}
time.sleep(sleeptime)
r = session.get(URL, headers=header, cookies=mycookie)
mycookie = dict(JSESSIONID=r.cookies.get('JSESSIONID'))
print("======= 1. enter login page start ========")
print(r.text, file=codecs.open('tmp/dump1.html', 'w', 'utf-8'))
print("======= 1. enter login page end ==========")


## 2. ログイン処理
URL="https://www.library.city.ichikawa.lg.jp/winj/opac/login.do;%s"%sessionid_string
header={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    #"Cookie": "JSESSIONID=29F7CC7920F9418BCCE7199961EF9DF5; _ga=GA1.3.665443413.1553500376",
    "Cookie": sessionid_string,
    "Host": "www.library.city.ichikawa.lg.jp",
    "Origin": "https://www.library.city.ichikawa.lg.jp",
    "Referer": "https://www.library.city.ichikawa.lg.jp/winj/opac/login.do?lang=ja",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
data={
    'txt_usercd': ID,
    'txt_password': PASSWORD,
    'submit_btn_login': 'ログイン(認証)'
}
time.sleep(sleeptime)
session = requests.session()
r = session.post(URL, headers=header, data=data, cookies=mycookie, allow_redirects=False)
### allow_redirects=Falseのオプションをつけると、ページ遷移(HTTPステータス302)の場合に勝手に遷移しない
print("======= 2. login start ========")
print(r.status_code)
print(r.text, file=codecs.open('tmp/dump2.html', 'w', 'utf-8'))
#mycookie = r.cookies
mycookie = dict(JSESSIONID=r.cookies.get('JSESSIONID'),_ga='GA1.3.665443413.1553500376')
print(r.history)
print(r.headers)
print(r.headers['Set-Cookie'])
sessionid_string=r.headers['Set-Cookie'].split(";")[0] ### ex. JSESSIONID=029F281FC7088253A80164DDC579644F
print("sessionid_string=%s"%sessionid_string)
print(mycookie)
print("======= 2. login end ==========")


## 3. 貸し出し状況一覧のページに移動
#URL="https://www.library.city.ichikawa.lg.jp/winj/opac/login.do?dispatch=/opac/mylibrary.do&every=1"
URL="https://www.library.city.ichikawa.lg.jp/winj/opac/lend-list.do"
header={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": sessionid_string,
    "Host": "www.library.city.ichikawa.lg.jp",
    "Referer": "https://www.library.city.ichikawa.lg.jp/winj/opac/top.do",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
time.sleep(sleeptime)
r = session.get(URL, headers=header, cookies=mycookie)
print(r.status_code)
print(r.text, file=codecs.open('tmp/dump3.html', 'w', 'utf-8'))
