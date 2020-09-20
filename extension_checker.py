# /usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging
import warnings

import pandas as pd

from tool_ichikawa import *


## 対象書籍が貸し出し延長対象であるかを判定する
def is_rental_extension_target(tool, bookid):
  logging.info(f"is_rental_extension_target (bookid = {bookid}) called")
  ### 返却日時を取得
  returndatetime = tool.get_return_date_datetime_per_book(bookid)
  ### 返却日までの日数を計算
  todaydatetime = datetime.date.today()
  remainday = (returndatetime - todaydatetime).days
  logging.debug(f"remain day of bookid={bookid} = {remainday} days")
  ### 貸出延長可能か確認
  enableextension = tool.get_extension_status_per_book(bookid)
  logging.debug(f"enableextension of bookid={bookid} = {enableextension}")
  ### 返却日当日 & 貸出延長可能 の場合は、貸出延長条件が成立したとする
  return (remainday == 0 and enableextension)


### 条件を満たした資料に関して予約延長申請を行う
def extend_reservation_day_if_satisfied_condition(sleep=3) -> None:
  logging.info("extend_reservation_day_if_satisfied_condition called")
  tool = IchikawaModule(sleep=sleep)
  ## 貸し出し中冊数の取得
  total_lend_num = tool.get_num_of_total_books(listtype="lend")

  ## 延長予約申請チェック
  ## 予約延長申請をすると本の順番が変わってしまうことへの対策として
  ## 予約延長申請した場合はbookid = 0に戻してループを繰り返す
  bookid = 0
  num_of_reservation_extension = 0
  while bookid < total_lend_num:
    logging.debug(f"bookID = {bookid}")
    ### 条件を満たした資料は貸出延長ボタンを押す
    if is_rental_extension_target(tool, bookid):
      logging.info(f"bookdID={bookid} return day will be extended.")
      apply_succeed = tool.apply_reserve_extension(bookid)
      if (apply_succeed):
        logging.info('Return day extenstion succeeded!')
        num_of_reservation_extension += 1
      else:
        warnings.warn('Return day extension failed.')
        bookid += 1  ## 処理を続行
    else:
      bookid += 1

  logging.info(f"Reservation of {num_of_reservation_extension} books was extended.")


# マージンを考慮した上で現在時刻が0時から8時までの間ではないかを判定
def is_extension_available(margin: int = 300) -> bool:
  now = datetime.datetime.now()
  allow_start = datetime.datetime(now.year, now.month, now.day, 8, 0, 0)
  allow_end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
  allow_start += datetime.timedelta(seconds=margin)
  allow_end -= datetime.timedelta(seconds=margin)
  return (now >= allow_start) and (now <= allow_end)


def main():
  # 現在時刻をチェックし、図書館サイトの仕様上延長申請が許可されていない時間である場合はエラーとする
  if (is_extension_available(margin=300)):
    logging.info("Extension process can be allowed at this time")
    extend_reservation_day_if_satisfied_condition(sleep=3)
  else:
    warnings.warn("Extension process can be allowed at this time")


if __name__ == "__main__":
  main()
