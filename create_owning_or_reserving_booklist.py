# /usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging

import pandas as pd

from tool_ichikawa import *


class RentalBookInfo:

  def __init__(self):
    self.title = ""
    self.isbn = ""
    self.listtype = ""
    self.waitnum = 0
    self.returndate = ""
    self.statsu = ""


def get_return_info_for_lending_book(bookid, tool):
  contents = tool.get_each_book_info(bookid=bookid, listtype="lend")
  soup_list = bs4.BeautifulSoup(contents, "html5lib")
  ### 延長可能かどうか確認
  enable_extension = tool.get_extension_status_per_book(bookid)
  returndatedatetime = tool.get_return_date_datetime_per_book(bookid)
  logging.info(returndatedatetime)
  returndate = returndatedatetime.strftime("%Y/%m/%d")
  ### 返却日までの日数を計算(延長可能な場合は14を足す)
  todaydatetime = datetime.date.today()
  remainday = (returndatedatetime - todaydatetime).days
  remainday = remainday + 14 if enable_extension else remainday
  return enable_extension, returndate, remainday


def get_return_info_for_reserve_book():
  enable_extension = False
  returndatedatetime = datetime.date(2001, 1, 1)
  returndate = returndatedatetime.strftime("%Y/%m/%d")
  remainday = 99
  return enable_extension, returndate, remainday


def get_waitnum_from_status(book_status):
  print(f"book status = {book_status}")
  ## "利用可能", "準備中", "配送中"の時は予約待ちを0と定義する
  if book_status == '利用可能':
    waitnum = 0
  elif book_status == '準備中':
    waitnum = 0
  elif book_status == '配送中':
    waitnum = 0
  else:
    try:
      waitnum = int(re.search('([0-9]+)位', book_status)[1])  ## 予約順位を取得
    except:
      waitnum = 99
  return waitnum


def get_mypage_book_df(listtype='lend', sleep=3):  ## listtype='lend' or 'reserve'
  logging.info(f"get_mypage_book_df (listtype={listtype}) is called")
  if (listtype != 'lend' and listtype != 'reserve'):
    raise ValueError(f"Error! lend or reserve is expected as listtype, but input is {listtype}")
  tool = IchikawaModule()
  tool.set_sleep_time(sleep)

  columnname = ['title', 'ISBN', 'status', 'waitnum', 'returndate', 'remainday', 'enableextension']
  df = pd.DataFrame(index=[], columns=columnname)

  ## ログイン処理
  tool.execute_login_procedure()

  ## 合計冊数情報を取得
  total_num = tool.get_num_of_total_books(listtype)
  logging.info(f"Total number of {listtype} books = {total_num}")

  ## 各資料の情報を取得
  for bookid in range(total_num):
    logging.info(f"checking information of bookid {bookid}")

    rental_reserve_book_info = RentalBookInfo()
    ## タイトルとISBNを取得
    rental_reserve_book_info.title, rental_reserve_book_info.isbn \
      = tool.get_title_and_isbn_from_book_info(bookid, listtype)
    if (listtype == 'lend'):
      ## statusを設定
      rental_reserve_book_info.status = "lending"
      ## 返却関連情報を取得
      rental_reserve_book_info.enable_extension, rental_reserve_book_info.returndate, rental_reserve_book_info.remainday \
        = get_return_info_for_lending_book(bookid, tool)
      ## 予約待ち情報を設定
      rental_reserve_book_info.waitnum = np.nan
    elif (listtype == "reserve"):
      ## statusを取得
      rental_reserve_book_info.status = tool.get_book_reserve_status_per_book(bookid)
      ## statusが"本人取消"である場合は無視する
      if (re.search('本人取消', rental_reserve_book_info.status) is not None):
        logging.info("Skip bookid = {bookid} manipulation because the status is 本人取消")
        continue
      ## 返却関連情報を取得
      rental_reserve_book_info.enable_extension, rental_reserve_book_info.returndate, rental_reserve_book_info.remainday \
      = get_return_info_for_reserve_book()
      ## 予約待ち情報を設定
      rental_reserve_book_info.waitnum = get_waitnum_from_status(rental_reserve_book_info.status)

    # dataframeに情報を登録
    df = df.append(pd.Series([
        rental_reserve_book_info.title, rental_reserve_book_info.isbn, listtype,
        rental_reserve_book_info.waitnum, rental_reserve_book_info.returndate,
        rental_reserve_book_info.remainday, rental_reserve_book_info.enable_extension
    ],
                             index=columnname),
                   ignore_index=True)

  # 終了処理
  tool.close_session()

  return df


def main():
  df_lend = get_mypage_book_df(listtype='lend')
  print(df_lend)
  df_reserve = get_mypage_book_df(listtype='reserve')
  print(df_reserve)
  df = pd.concat([df_lend, df_reserve])
  print(df)
  df.to_csv('list/nowreading.csv')


if __name__ == "__main__":
  main()
