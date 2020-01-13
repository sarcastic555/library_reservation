import tool_culil
import pandas as pd
import datetime
import time
import numpy as np

sleeptime=1 ## [sec]

columnname=['サービスID','アイテムID','13桁ISBN','カテゴリ','評価','読書状況','レビュー','タグ','読書メモ(非公開)','登録日時','読了日','タイトル','作者名','出版社名','発行年','ジャンル','ページ数','価格']
alldf = pd.read_csv('list/alllist.csv',encoding="utf-8",header=None, names=columnname)
#alldf = pd.read_csv('list/alllist.csv',encoding="shift-jis",header=None, names=columnname)
notread_df = alldf[alldf['読書状況']=='読みたい'] ## 読みたい本だけリストにする
notread_df=notread_df.drop(['サービスID','アイテムID','カテゴリ','評価','レビュー','タグ','読書メモ(非公開)','登録日時','読了日','出版社名','発行年','ジャンル','ページ数','価格'], axis=1) ## 不要な列を削除
notread_df['waitstatus']='Nan'
notread_df=notread_df.reset_index(drop=True) ## indexの振り直し

_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('program start!')

### read now renting & booking book list
try:
    nowreading=pd.read_csv('list/nowreading.csv')
except:
    nowreading=pd.DataFrame(columns=['ISBN'])
    print("Warning! list/nowreading.csv not found.")
    
### get book status
for i in range(len(notread_df)):
    if (i+1)%10==0:
        print("%d/%d"%(i+1,len(notread_df)))
    #print('#'*20)
    time.sleep(sleeptime)
    ## ISBNがない本(電子書籍など)の場合は蔵書なしとする
    #print(notread_df.iloc[i]['13桁ISBN'])
    if(np.isnan(notread_df.iloc[i]['13桁ISBN'])):
        notread_df.loc[i,['waitstatus']]='蔵書なし'
        continue
    
    ## 現在借りてる本、予約してる本に含まれていた場合は強制終了
    if (len(nowreading[nowreading['ISBN']==int(notread_df.iloc[i]['13桁ISBN'])]) != 0):
        notread_df.loc[i,['waitstatus']]='借用中または予約中'
        #print('%s: 借用中または予約中')
        continue

    ## その他の本
    module = tool_culil.CulilModule()
    module.set_sleep_time(sleeptime)
    renting_possible_flag, renting_soon_flag = module.check_existence_in_library(str(notread_df.iloc[i]['13桁ISBN']))
    if (renting_possible_flag and renting_soon_flag):
        notread_df.loc[i,['waitstatus']]='予約なし'
        #print('予約なし')
    elif (renting_possible_flag and not renting_soon_flag):
        notread_df.loc[i,['waitstatus']]='予約あり'
        #print('予約あり')
    else:
        notread_df.loc[i,['waitstatus']]='蔵書なし'
        #print('蔵書なし')   
notread_df[notread_df['waitstatus']=='蔵書なし'].to_csv("list/notfound.csv")
notread_df[notread_df['waitstatus']=='予約なし'].to_csv("list/shortwait.csv")
notread_df[notread_df['waitstatus']=='予約あり'].to_csv("list/longwait.csv")

print("ブクログ登録済み本: %d冊"%len(alldf))
print("読みたいラベルの本: %d冊"%len(notread_df))
print("-- 現在借用中or予約中: %d冊"%len(nowreading))
print("-- 蔵書なし: %d冊"%len(notread_df[notread_df['waitstatus']=='蔵書なし']))
print("-- 予約なし: %d冊"%len(notread_df[notread_df['waitstatus']=='予約なし']))
print("-- 予約あり: %d冊"%len(notread_df[notread_df['waitstatus']=='予約あり']))
print("注:読みたいラベルの本から借りてるとは限らないので、下4つの冊数を合計しても読みたいラベルの冊数に一致しない可能性がある")
