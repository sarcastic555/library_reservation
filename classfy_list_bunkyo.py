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

sleeptime=10 ## sleepign time [sec]

### read booklist
columnname=['サービスID','アイテムID','13桁ISBN','カテゴリ','評価','読書状況','レビュー','タグ','読書メモ(非公開)','登録日時','読了日','タイトル','作者名','出版社名','発行年','ジャンル','ページ数','価格']
alldf = pd.read_csv('list/alllist.csv',encoding="shift-jis",header=None, names=columnname)
notread_df = alldf[alldf['読書状況']=='読みたい'] ## 読みたい本だけリストにする
notread_df=notread_df.drop(['サービスID','アイテムID','カテゴリ','評価','レビュー','タグ','読書メモ(非公開)','登録日時','読了日','出版社名','発行年','ジャンル','ページ数','価格'], axis=1) ## 不要な列を削除
notread_df=notread_df.dropna(axis = 0, how = 'any')  ## ISBNがない本(電子書籍など)はリストから除く
notread_df['listnum']=0
notread_df['waitstatus']='Nan'
notread_df=notread_df.reset_index(drop=True) ## indexの振り直し

_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('program start!')
dirpath=os.path.abspath(os.path.dirname(sys.argv[0])) ## get directory of this program                                 
print ('directory=%s' % dirpath)
browser = webdriver.Chrome('%s/../chromedriver' % dirpath)

### read now renting & booking book list
nowreading=pd.read_csv('list/nowreading.csv')

### get book status
for i in range(len(notread_df)):

    time.sleep(sleeptime)
    ## 現在借りてる本、予約してる本に含まれていた場合は強制終了
    if (len(nowreading[nowreading['ISBN']==int(notread_df.iloc[i]['13桁ISBN'])]) != 0):
        notread_df.loc[i, ['listnum']]=0
        notread_df.loc[i,['waitstatus']]='借用中または予約中'
        continue

    ## go to search page
    browser.get('https://www.lib.city.bunkyo.tokyo.jp/')
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('//*[@id="globalMenu"]/ul/li[1]/a')[0].click() ## go to detailed search page

    ## move to detailed search page
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/nobr[2]/a/span/strong')[0].click()
    ## type 13-digit ISBN
    time.sleep(sleeptime)
    browser.find_elements_by_xpath('//*[@id="text5"]')[0].send_keys(int(notread_df.iloc[i]['13桁ISBN']))
    browser.find_elements_by_xpath('/html/body/dl/dd/form/input[7]')[0].click()

    ## moved to search list page
    time.sleep(sleeptime)
    searchresulttext=browser.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[1]/nobr')[0].text
    searchnumtext=re.split(' ',searchresulttext)[1]
    searchnum=re.match('\d*',searchnumtext).group()
    searchnum=int(re.match('\d*',searchnumtext).group())
    notread_df.loc[i, ['listnum']]=searchnum

    ### もし候補の本が1冊以上あれば貸し出し可否情報を取得
    if (searchnum>=1):
        time.sleep(sleeptime)
        browser.find_elements_by_xpath('/html/body/table[6]/tbody/tr[2]/td[3]/strong/a')[0].click() ## click first book
        time.sleep(sleeptime)
        waitresulttext=browser.find_elements_by_xpath('/html/body/table[5]/tbody/tr/td[1]')[0].text ## get number of books and reservation
        #print ('waitresult = %s' % waitresulttext)
        if (waitresulttext.find('予約')!=-1):  ## 予約が入っている場合
            notread_df.loc[i,['waitstatus']]='予約あり'
        else:
            notread_df.loc[i,['waitstatus']]='予約なし'

print (notread_df)
notread_df[notread_df['listnum']==0].to_csv("list/notfound.csv")
notread_df[(notread_df['listnum']!=0) & (notread_df['waitstatus']=='予約なし')].to_csv("list/available.csv")
notread_df[(notread_df['listnum']!=0) & (notread_df['waitstatus']=='予約あり')].to_csv("list/longwait.csv")
browser.close()
