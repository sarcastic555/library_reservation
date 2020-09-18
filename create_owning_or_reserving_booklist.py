# /usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging

import pandas as pd

from tool_ichikawa import *


def get_waitnum_from_status(book_status):
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
  columnname = ['title', 'ISBN', 'status', 'waitnum', 'returndate', 'remainday', 'enableextension']
  df = pd.DataFrame(index=[], columns=columnname)

  ## 合計冊数情報を取得
  tool = IchikawaModule(sleep=sleep)
  total_num = tool.get_num_of_total_books(listtype)
  logging.info(f"Total number of {listtype} books = {total_num}")

  ## 各資料の情報を取得
  for bookid in range(total_num):
    logging.info(f"checking information of bookid {bookid}")
    info = tool.get_book_information(bookid, listtype)
    ## statusが"本人取消"である場合は無視する
    if (re.search('本人取消', info.status) is not None):
      logging.info("Skip bookid = {bookid} manipulation because the status is 本人取消")
      continue
    waitnum = get_waitnum_from_status(info.reserve_status) if listtype == "reserve" else np.nan
    todaydatetime = datetime.date.today()
    remain_day_for_return = (info.return_datetime_after_extension - todaydatetime).days
    df = df.append(pd.Series({
        "title": info.title,
        "ISBN": info.isbn,
        "status": info.status,
        "waitnum": waitnum,
        "returndate": info.return_datetime_before_extension.strftime("%Y/%m/%d"),
        "remainday": remain_day_for_return,
        "enableextension": info.can_rental_extension
    }),
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
