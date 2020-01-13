# /usr/local/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import sys
import os
import json
import platform
import pandas as pd
import re

ID='1036505'
PASSWORD='zk2ec6'
sleeptime=10 ## sleeping time [sec]

## login library user page
_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('program start!')
dirpath=os.path.abspath(os.path.dirname(sys.argv[0])) ## get directory of this program

print ('directory=%s' % dirpath)
browser = webdriver.Chrome('%s/../chromedriver' % dirpath)
browser.get('https://www.lib.city.bunkyo.tokyo.jp/opw/OPW/OPWUSERCONF.CSP')
time.sleep(sleeptime)
browser.find_element_by_name('usercardno').send_keys(ID)
browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
browser.find_element_by_name('Login').click()

### 何らかの理由でうまくユーザーページに入れなかった場合はもう一度実行
time.sleep(sleeptime)
pagetitle=browser.find_elements_by_tag_name('strong')[0].text
if (pagetitle=='ログイン認証'):
    browser.find_element_by_name('usercardno').send_keys(ID)
    browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
    browser.find_element_by_name('Login').click()

## 現在の貸し出し冊数と予約冊数およびその本の情報を取得
columnname=['title','author','ISBN','status','waitnum']
currentbooklist_df=pd.DataFrame(index=[],columns=columnname)
### 貸し出し中資料
time.sleep(sleeptime)
rentaltext=browser.find_elements_by_xpath('/html/body/form[1]/table[2]/tbody/tr/td/dd')[0].text
rentalnum=int(re.match('\d*',rentaltext[3:]).group())
print ('rentalnum=%d' % rentalnum)
for i in range(rentalnum):
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('/html/body/form[1]/table[3]/tbody/tr[%d]/td[4]/a' % (2*i+3))[0].click()
    tbody=browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td[2]/table[1]/tbody')[0]
    tr=tbody.find_elements_by_tag_name('tr')
    for thistr in tr:
        if (re.split(' ',thistr.text)[0] == 'タイトル'):
            title=re.split(' ',thistr.text)[1] 
        elif (re.split(' ',thistr.text)[0] == '著者'):
            author=re.split(' ',thistr.text)[1]
            author=re.split(r'／',author)[0] ## '東野圭吾／著' -> '東野圭吾'
        elif (re.split(' ',thistr.text)[0] == 'ISBN'):
            ISBN=re.split(' ',thistr.text)[1]
            ISBN=re.sub(r'-','',ISBN) ## ハイフン（'-'）を削除
    currentbooklist_df=currentbooklist_df.append(pd.Series([title,author,ISBN,'借用中',0],index=columnname), ignore_index=True)
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[3]/strong/a/strong')[0].click() ## go back to user page
    
### 予約中資料
time.sleep(sleeptime)
reservetext=browser.find_elements_by_xpath('/html/body/form[2]/dd[2]/table/tbody/tr/td')[0].text
reservenum=int(re.match('\d*',reservetext[2:]).group())
print ('reserve=%d' % reservenum)
for i in range(reservenum):
    time.sleep(sleeptime)
    waittext=browser.find_elements_by_xpath('/html/body/form[2]/table[1]/tbody/tr[%d]/td[9]' % (i+2))[0].text
    waitnum=re.match('\d*',waittext[0:]).group()
    if (waitnum==''):
        waitnum=0
    else:
        waitnum=int(waitnum)

    time.sleep(sleeptime)
    browser.find_elements_by_xpath('/html/body/form[2]/table[1]/tbody/tr[%d]/td[4]/a' % (i+2))[0].click()    
    tbody=browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td[2]/table[1]/tbody')[0]
    tr=tbody.find_elements_by_tag_name('tr')
    for thistr in tr:
        if (re.split(' ',thistr.text)[0] == 'タイトル'):
            title=re.split(' ',thistr.text)[1] 
        elif (re.split(' ',thistr.text)[0] == '著者'):
            author=re.split(' ',thistr.text)[1]
            author=re.split(r'／',author)[0] ## '東野圭吾／著' -> '東野圭吾'
        elif (re.split(' ',thistr.text)[0] == 'ISBN'):
            ISBN=re.split(' ',thistr.text)[1]
            ISBN=re.sub(r'-','',ISBN) ## ハイフン（'-'）を削除
    currentbooklist_df=currentbooklist_df.append(pd.Series([title,author,ISBN,'予約中',waitnum],index=columnname), ignore_index=True)
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[3]/strong/a/strong')[0].click() ## go back to user page

print (currentbooklist_df)
currentbooklist_df.to_csv('list/nowreading.csv')
time.sleep(sleeptime)
browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a')[0].click() ## logout
browser.close()
