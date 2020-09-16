# /usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging

import pandas as pd

from tool_ichikawa import *


### 条件を満たした資料に関して予約延長申請を行う
def extend_reservation_day_if_satisfied_condition(sleep=3):
  logging.info("extend_reservation_day_if_satisfied_condition called")
  tool = IchikawaModule()
  tool.set_sleep_time(sleep)
  ## ログイン処理
  tool.execute_login_procedure()

  ## 貸し出し中冊数の取得
  total_lend_num = tool.get_num_of_total_books(listtype="lend")

  ## 延長予約申請チェック
  ## 予約延長申請をすると本の順番が変わってしまうことへの対策として
  ## 予約延長申請した場合はbookid = 0に戻してループを繰り返す
  bookid = 0
  num_of_reservation_extension = 0
  while bookid < total_lend_num:
    logging.debug(f"bookID = {bookid}")
    ### 返却日時を取得
    returndatetime = tool.get_return_date_datetime_per_book(bookid)
    ### 返却日までの日数を計算
    todaydatetime = datetime.date.today()
    remainday = (returndatetime - todaydatetime).days
    logging.debug(f"remain day = {remainday} days")
    ### 貸出延長可能か確認
    enableextension = tool.get_extension_status_per_book(bookid)
    logging.debug(f"enableextension = {enableextension}")
    ### 返却日当日 & 貸出延長可能 の場合は、貸出延長ボタンを押す
    if (remainday == 0 and enableextension):
      logging.info(f"bookdID={bookid} return day will be extended.")
      apply_succeed = tool.apply_reserve_extension(bookid)
      if (apply_succeed):
        logging.info('Lending day extenstion succeeded!')
        num_of_reservation_extension += 1
      else:
        warnings.warn('Lending day extension failed.')
        bookid += 1  ## 処理を続行
    else:
      bookid += 1

  logging.info(f"Reservation of {num_of_reservation_extension} books was extended.")

  ### ログアウトして、sessionを終了して終わる
  tool.close_session()


def main():
  extend_reservation_day_if_satisfied_condition(sleep=3)


if __name__ == "__main__":
  main()
