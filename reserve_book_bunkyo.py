from selenium import webdriver
import random
import inspect
import time
import datetime
import sys
import pandas as pd
import re
import os

ID='1036505'
PASSWORD='zk2ec6'

listdir='list'
reservebook_max=18
longwaitreservenum_max=11
shortwaitreservenum_max=7
sleeptime=1 ## sleeping time [sec]
#reservebook_max=10
#longwaitreservenum_max=7
#shortwaitreservenum_max=3

### read now reading & reserving dataframe
nowreading_df=pd.read_csv('list/nowreading.csv')
current_renting_num=len(nowreading_df[nowreading_df['status']=='借用中'])
current_reserving_num=len(nowreading_df[nowreading_df['status']=='予約中'])
preparednum=len(nowreading_df[(nowreading_df['status']=='予約中') & (nowreading_df['waitnum']==0)])
shortwaitreservenum=len(nowreading_df[(nowreading_df['status']=='予約中') & (nowreading_df['waitnum']==1)])
longwaitreservenum=len(nowreading_df[(nowreading_df['status']=='予約中') & (nowreading_df['waitnum']>=2)])
print ("prepared=%d, shortwait=%d, longwait=%d, max=%d" % (preparednum,shortwaitreservenum,longwaitreservenum,reservebook_max))

def get_linenum(depth=0):
    frame = inspect.currentframe().f_back
    return frame.f_lineno

## login library user page
_nowtime=datetime.datetime.today()
print ('currenttime=%s.' % _nowtime.strftime('%Y/%m/%d %H:%M:%S'))
print ('program start!')
dirpath=os.path.abspath(os.path.dirname(sys.argv[0])) ## get directory of this program                                 
print ('directory=%s' % dirpath)
browser = webdriver.Chrome('%s/../chromedriver' % dirpath)
browser.get('https://www.lib.city.bunkyo.tokyo.jp/opw/OPW/OPWUSERCONF.CSP')
time.sleep(sleeptime);
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
browser.find_element_by_name('usercardno').send_keys(ID)
browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
browser.find_element_by_name('Login').click()

### 何らかの理由でうまくユーザーページに入れなかった場合はもう一度実行
time.sleep(sleeptime);
pagetitle=browser.find_elements_by_tag_name('strong')[0].text
if (pagetitle=='ログイン認証'):
    browser.find_element_by_name('usercardno').send_keys(ID)
    browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
    browser.find_element_by_name('Login').click()


### read dataframe
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
shortwait_df = pd.read_csv('%s/available.csv' % listdir)
shortwait_df = shortwait_df.reset_index(drop=True) ## indexの振り直し
longwait_df  = pd.read_csv('%s/longwait.csv' % listdir)
longwait_df  = longwait_df.reset_index(drop=True) ## indexの振り直し

#############################################################
### longwaitの方は、予約いっぱいになるまでどんどん予約する
### longwait割り当て冊数から、すでに予約できた冊数を引いた数だけ予約する
print('longwaint reservation start ==============')
longwait_book_availablenum=longwaitreservenum_max-preparednum-longwaitreservenum
longwait_booklistnum=len(longwait_df)

### もし、longwaitの本を借り過ぎていた場合は,longwaitの本はもう借りない
if (longwait_book_availablenum<0):
    print("longwait reserve num = %d-%d-%d = %d<0" % (longwaitreservenum_max,preparednum,longwaitreservenum,longwait_book_availablenum))
    print("longwait book will not be reserved today")
    longwait_booknumlist=range(0)
### 候補の本の数が予約可能冊数に満たない時は全て予約する
elif (longwait_booklistnum<longwait_book_availablenum):
    longwait_booknumlist=range(longwait_booklistnum)
### 候補の本の数が予約可能冊数より多い場合、ランダムに選んで予約する
else:
    ## random.sample([**],3): [**]のリストの中からrandomで3こ重複を許さずに取得
    longwait_booknumlist=random.sample(range(longwait_booklistnum), longwait_book_availablenum)
print("%d books will be booked" % longwait_book_availablenum)
for i in longwait_booknumlist:
    time.sleep(sleeptime);

    ## 今回予約しようとしてる本が、今借りてるor予約してる本リストの中にないことを確認する
    readingreservingflag=False
    for j in range(len(nowreading_df)):
        ### nowreadingの方のISBNは10桁になっていることがあるので、その場合は処理をスキップ
        if (len(str(nowreading_df.iloc[j]['ISBN']))!=13):
            continue
        if (int(float(longwait_df.iloc[i]['13桁ISBN'])) == int(nowreading_df.iloc[j]['ISBN'])):
            readingreservingflag=True
    if (readingreservingflag):
        continue

    browser.get('https://www.lib.city.bunkyo.tokyo.jp/')
    time.sleep(sleeptime);
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    browser.find_elements_by_xpath('//*[@id="globalMenu"]/ul/li[1]/a')[0].click() ## go to detailed search page

    ## move to detailed search page
    time.sleep(sleeptime);
    browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/nobr[2]/a/span/strong')[0].click()    

    ## type ISBN
    print ('title=%s' % longwait_df.iloc[i]['タイトル'])
    browser.find_elements_by_xpath('//*[@id="text5"]')[0].send_keys(int(longwait_df.iloc[i]['13桁ISBN']))
    browser.find_elements_by_xpath('/html/body/dl/dd/form/input[7]')[0].click()

    ## moved to search list page
    time.sleep(sleeptime);
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    searchresulttext=browser.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[1]/nobr')[0].text
    searchnumtext=re.split(' ',searchresulttext)[1]
    searchnum=re.match('\d*',searchnumtext).group()
    searchnum=int(re.match('\d*',searchnumtext).group())
    
    time.sleep(sleeptime);
    browser.find_elements_by_xpath('/html/body/table[6]/tbody/tr[2]/td[3]/strong/a')[0].click() ## click first book
    time.sleep(sleeptime);
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td[3]/table/tbody/tr[1]/td/a/img')[0].click() ## click 「予約処理」 button
    time.sleep(sleeptime);
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    check=browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr[1]/td[2]/big/strong')

    ## move to reservation page
    time.sleep(sleeptime);
#    browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr[1]/td/form/p/table/tbody/tr[2]/td[1]/input[1]')[0].click()  ## activate check button
    browser.find_elements_by_xpath('//*[@id="library"]')[0].send_keys('7：千石図書館')

    ## move to final confirmation
    time.sleep(sleeptime);
    browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr[2]/td[1]/form/table/tbody/tr[6]/td/input[1]')[0].click()

    time.sleep(sleeptime);
    #browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td/form/p[2]/input[3]')[0].click() ## cancel
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td/form/p[2]/input[2]')[0].click() ## accept

print('longwaint reservation end =================')
#############################################################
print('shortwaint reservation start =============')
### shortwaitの方は、このプログラムで1冊だけ実行する
### 現在のshortwait予約数(shortwaitreservenum)がshorrtwait予約割り当て冊数(shortwaitreservenum_max)より小さくなければ終了
if (preparednum+shortwaitreservenum+longwaitreservenum>reservebook_max):
    print('preparednum(%d) + shortwaitreservenum(%d) + longwaitreservenum(%d) > reservebook_max(%d)' % (preparednum,shortwaitreservenum,longwaitreservenum,reservebook_max))
    sys.exit()

print('preparednum(%d) + shortwaitreservenum(%d) + longwaitreservenum(%d) <= reservebook_max(%d). 1 book will be booked.' % (preparednum,shortwaitreservenum,longwaitreservenum,reservebook_max))

## 今回予約しようとしてる本が、今借りてるor予約してる本リストの中にないことを確認する
readingreservingflag=True ## initialize
while (readingreservingflag): ## 今借りてるor予約してる本リストの中にある限りloopを続ける
    shortwait_bookID=random.randrange(len(shortwait_df)) ## randomで1つのIDを選択
    time.sleep(sleeptime);
    readingreservingflag=False
    for j in range(len(nowreading_df)):
        ### nowreadingの方のISBNは10桁になっていることがあるので、その場合は処理をスキップ
        if (len(str(nowreading_df.iloc[j]['ISBN']))!=13):
            continue
        if (int(float(shortwait_df.iloc[shortwait_bookID]['13桁ISBN'])) == int(nowreading_df.iloc[j]['ISBN'])):
            readingreservingflag=True


browser.get('https://www.lib.city.bunkyo.tokyo.jp/')
time.sleep(sleeptime);
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
browser.find_elements_by_xpath('//*[@id="globalMenu"]/ul/li[1]/a')[0].click() ## go to detailed search page

## move to detailed search page
time.sleep(sleeptime);
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/nobr[2]/a/span/strong')[0].click()
## type ISBN
print ('title=%s' % shortwait_df.iloc[shortwait_bookID]['タイトル'])
browser.find_elements_by_xpath('//*[@id="text5"]')[0].send_keys(int(shortwait_df.iloc[shortwait_bookID]['13桁ISBN']))
browser.find_elements_by_xpath('/html/body/dl/dd/form/input[7]')[0].click()

## moved to search list page
time.sleep(sleeptime);
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
searchresulttext=browser.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[1]/nobr')[0].text
searchnumtext=re.split(' ',searchresulttext)[1]
searchnum=re.match('\d*',searchnumtext).group()
searchnum=int(re.match('\d*',searchnumtext).group())
    
time.sleep(sleeptime);
browser.find_elements_by_xpath('/html/body/table[6]/tbody/tr[2]/td[3]/strong/a')[0].click() ## click first book
browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td[3]/table/tbody/tr[1]/td/a/img')[0].click() ## click 「予約処理」 button
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
check=browser.find_elements_by_xpath('/html/body/table[1]/tbody/tr[1]/td[2]/big/strong')

### ユーザー認証を要求されたらIDとpasswordを入力
pagetitle=browser.find_elements_by_tag_name('strong')[0].text
if (pagetitle=='ログイン認証'):
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    browser.find_element_by_name('usercardno').send_keys(ID)
    browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
    time.sleep(sleeptime);
    browser.find_element_by_name('Login').click()

## move to reservation page
time.sleep(sleeptime);
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
browser.find_elements_by_xpath('//*[@id="library"]')[0].send_keys('7：千石図書館')
time.sleep(sleeptime);
browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr[2]/td[1]/form/table/tbody/tr[6]/td/input[1]')[0].click() ##clicl「登録する」ボタン
time.sleep(sleeptime);

### ユーザー認証を要求されたらIDとpasswordを入力
pagetitle=browser.find_elements_by_tag_name('strong')[0].text
if (pagetitle=='ログイン認証'):
    with open("html/line%d.txt"%get_linenum(), "w") as file:
        print(browser.page_source, file=file)
    browser.save_screenshot('picture/line%d.png'%get_linenum())
    browser.find_element_by_name('usercardno').send_keys(ID)
    browser.find_element_by_name('userpasswd').send_keys(PASSWORD)
    browser.find_element_by_name('Login').click()

#browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td/form/p[2]/input[3]')[0].click() ## cancel
with open("html/line%d.txt"%get_linenum(), "w") as file:
    print(browser.page_source, file=file)
browser.save_screenshot('picture/line%d.png'%get_linenum())
browser.find_elements_by_xpath('/html/body/table[4]/tbody/tr/td/form/p[2]/input[2]')[0].click() ## accept

print('shortwaint reservation end ==============')

##########################################################################################
time.sleep(sleeptime);
browser.close()
print("finished.")
