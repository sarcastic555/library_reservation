import pandas as pd
import tool_ichikawa
import random

def get_reserve_isbn_list(booklist_df,reservenum,reservenum_per_day,nowreading_df):
    print("start selecting ISBN list from booklist database")
    booklistnum=len(booklist_df)
    print("boolist num = %d"%booklistnum)
    if (booklistnum==0):
        print("!!! Length of booklist num = 0. No book will be reserved.")
        return []
    elif (reservenum<=0):
        print("!!! reservenum (%d) <= 0. No book will be reserved."%reservenum)
        return []
    else:
        print("%d books will be chosen" % reservenum_per_day)
        ## 今回予約しようとしてる本が、今借りてるor予約してる本リストの中にないことが確認できるまでループを続ける
        ISBNlist=[]
        for i in range(reservenum_per_day):
            j=0
            while j<len(nowreading_df):
                index_candidate=random.choice(range(booklistnum))
                if int(float(booklist_df.iloc[index_candidate]['13桁ISBN'])) == int(nowreading_df.iloc[j]['ISBN']):
                    continue
                j+=1
            ISBNlist.append(str(int(booklist_df.iloc[index_candidate]['13桁ISBN'])))
                
        print(ISBNlist)
        return ISBNlist
   

### パラメータ設定
reservenum_max=10   ## 最大で予約できる冊数
reservenum_per_day=1 ## 1日にshortwaitとlongwaitをそれぞれ予約する冊数
shortwait_reservenum_limit=5 ## shortwait予約可能最大数
longwait_reservenum_limit=5 ## longwait予約可能最大数

## dataframeの読み込み
nowreading_df = pd.read_csv('list/nowreading.csv')
print(nowreading_df)
shortwait_reservelist_df = pd.read_csv('list/shortwait.csv')
print(shortwait_reservelist_df)
longwait_reservelist_df = pd.read_csv('list/longwait.csv')
print(longwait_reservelist_df)


### 現在の予約状況の確認
preparedbooknum_in_reservedlist=len(nowreading_df[nowreading_df['waitnum']==0]) ## 予約待ち人数が0のものは受け取り可能とする
shortwaitbooknum_in_reservedlist=len(nowreading_df[nowreading_df['waitnum']==1]) ## 予約待ち人数が1のものは待ち時間小とする
longwaitbooknum_in_reservedlist=len(nowreading_df[nowreading_df['waitnum']>1]) ## 予約待ち人数が1より大きいのものは待ち時間大とする

print('prepared book num in reserved list= %d'%preparedbooknum_in_reservedlist)
print('short wait book num in reserved list= %d'%shortwaitbooknum_in_reservedlist)
print('long wait book num in reserved list= %d'%longwaitbooknum_in_reservedlist)

## 予約冊数の導出
shortwait_reserve_book_num = min(shortwait_reservenum_limit-preparedbooknum_in_reservedlist-shortwaitbooknum_in_reservedlist, reservenum_max-preparedbooknum_in_reservedlist-shortwaitbooknum_in_reservedlist-longwaitbooknum_in_reservedlist)
longwait_reserve_book_num = min(1,min(longwait_reservenum_limit-longwaitbooknum_in_reservedlist, reservenum_max-preparedbooknum_in_reservedlist-shortwaitbooknum_in_reservedlist-longwaitbooknum_in_reservedlist-shortwait_reserve_book_num)) ## longwaitは最大でも1日に1冊しか予約しない
print("shortwait_reserve_book_num = %d"%shortwait_reserve_book_num)
print("longwait_reserve_book_num = %d"%longwait_reserve_book_num)

### 予約ISBNリストの作成
print('---- create shortwait reserve book list start ----')
ISBNlist_shortwait=get_reserve_isbn_list(shortwait_reservelist_df,
                                         shortwait_reserve_book_num,
                                         reservenum_per_day,
                                         nowreading_df)
print(ISBNlist_shortwait)
print('---- create shortwait reserve book list end ----')
print('---- create longwait reserve book list start ----')
ISBNlist_longwait=get_reserve_isbn_list(longwait_reservelist_df,
                                        longwait_reserve_book_num,
                                        reservenum_per_day,
                                        nowreading_df)
print(ISBNlist_longwait)
print('---- create longwait reserve book list end ----')

#### reserve books ###########
print("===== book reservation start ======")
reserver = tool_ichikawa.IchikawaModule()
reserver.set_debug_mode(True)
reserver.set_sleep_time(3)

if (len(ISBNlist_longwait)>0):
    print("start reserving longwait book")
    reserver.reserve_book(ISBNlist_longwait)
    print("end reserving longwait book")
else:
    print("longwait book will not be reserved")

### shortwaitの本は最も返却日が近い本の返却日までの日数が6~10日以内の場合に予約する
minimum_remain_day = nowreading_df['remainday'].min()
if (minimum_remain_day>=6 and minimum_remain_day<=10 and len(ISBNlist_shortwait)>0):
    print("shortwait book will be reserved")
    print("start reserving shortwait book")
    reserver.reserve_book(ISBNlist_shortwait)
    print("end reserving shortwait book")
else:
    print("shortwait book will not be reserved")
print("===== book reservation end ======")
