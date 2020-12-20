# /usr/local/bin/python
# -*- coding: utf-8 -*-
import argparse
import datetime
import logging
import warnings

import pandas as pd

from tools.tool_ichikawa import *

def options() -> argparse:
  parser = argparse.ArgumentParser()
  parser.add_argument('--lend_output_file', help='Path to output lend book list.', default='list/lendlist.csv')
  parser.add_argument('--reserve_output_file', help='Path to output reserving book list.', default='list/reservelist.csv')
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args

def get_waitnum_from_status(book_status) -> int:
  # book_statusには冗長なスペース等が含まれているため文字列の完全一致ではなく対象文字列が含まれているかで判定
  ## "利用可能", "準備中", "配送中"の時は予約待ちを0と定義する
  if (re.search('利用可能', book_status) is not None):
    waitnum = 0
  elif (re.search('準備中', book_status) is not None):
    waitnum = 0
  elif (re.search('配送中', book_status) is not None):
    waitnum = 0
  elif (re.search('順番待ち', book_status) is not None):
    waitnum = int(re.search('([0-9]+)位', book_status)[1])  ## 予約順位を取得
  elif (re.search('返却待ち', book_status) is not None):
    waitnum = int(re.search('([0-9]+)位', book_status)[1])  ## 予約順位を取得
  elif (re.search('確認待ち', book_status) is not None):
    waitnum = int(re.search('([0-9]+)位', book_status)[1])  ## 予約順位を取得
  else:
    warnings.warn(f"Cannot evaluate waitnum for {book_status}")
    waitnum = 99
  return waitnum

def get_rental_book_df(sleep=3) -> pd.DataFrame:
  columnname = ['title', 'ISBN', 'returndate', 'remainday', 'enableextension']
  df = pd.DataFrame(index=[], columns=columnname)
  ## 合計冊数情報を取得
  tool = IchikawaModule(sleep=sleep)
  total_num = tool.get_num_of_total_books("lend")
  logging.info(f"Total number of books = {total_num}")
  ## 各資料の情報を取得
  for bookid in range(total_num):
    logging.info(f"checking information of bookid {bookid}")
    info = tool.get_rental_book_information(bookid)
    todaydatetime = datetime.date.today()
    remain_day_for_return = (info.return_datetime_after_extension - todaydatetime).days
    df = df.append(pd.Series({
        "title": info.title,
        "ISBN": info.isbn,
        "returndate": info.return_datetime_before_extension.strftime("%Y/%m/%d"),
        "remainday": remain_day_for_return,
        "enableextension": info.can_rental_extension
    }),
                   ignore_index=True)
  return df

def get_reserving_book_df(sleep=3) -> pd.DataFrame:
  columnname = ['title', 'ISBN', 'returndate', 'remainday', 'enableextension']
  df = pd.DataFrame(index=[], columns=columnname)
  ## 合計冊数情報を取得
  tool = IchikawaModule(sleep=sleep)
  total_num = tool.get_num_of_total_books("reserve")
  logging.info(f"Total number of books = {total_num}")
  ## 各資料の情報を取得
  for bookid in range(total_num):
    logging.info(f"checking information of bookid {bookid}")
    info = tool.get_under_reservation_book_information(bookid)
    ## statusが"本人取消"である場合は無視する
    if (re.search('本人取消', info.reserve_status) is not None):
      logging.info(f"Skip bookid = {bookid} manipulation because the status is 本人取消")
      continue
    ## statusが"期限切れ"である場合は無視する
    if (re.search('期限切れ', info.reserve_status) is not None):
      logging.info(f"Skip bookid = {bookid} manipulation because the status is 期限切れ")
      continue
    waitnum = get_waitnum_from_status(info.reserve_status)
    # reserve_statusは文字列が複数行になってしまっているので出力しない
    df = df.append(pd.Series({
        "title": info.title,
        "ISBN": info.isbn,
        "waitnum": waitnum,
    }),
                   ignore_index=True)
  return df


def main(options: argparse):
  # 貸し出し中の資料リストの作成
  df_lend = get_rental_book_df()
  logging.info("rental book size = %d" % len(df_lend))
  os.makedirs(os.path.dirname(options.lend_output_file), exist_ok=True)
  df_lend.to_csv(options.lend_output_file)
  # 予約中の資料リストの作成
  df_reserve = get_reserving_book_df()
  logging.info("reserve book size = %d" % len(df_reserve))
  os.makedirs(os.path.dirname(options.reserve_output_file), exist_ok=True)
  df_reserve.to_csv(options.reserve_output_file)

if __name__ == "__main__":
  options = options()
  main(options=options)
