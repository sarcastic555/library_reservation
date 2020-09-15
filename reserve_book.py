import logging
import os
import random
import warnings
from reserve_book_info_evaluator import ReserveBookInfoEvaluator
import pandas as pd

from tool_ichikawa import IchikawaModule


def main(sleep=3):
  reserve_calculator = ReserveBookInfoEvaluator(nowreading_filename="list/nowreading.csv",
                                                shortwait_filename="list/no_reservation.csv",
                                                longwait_filename="list/has_reservation.csv")
  # 予約予定冊数の計算
  reserve_calculator.calculate_reserve_book_num()
  # 計算結果の出力
  reserve_calculator.print_info()
  # 予約予定の本のISBNリストの取得
  shortwait_isbn_list = reserve_calculator.get_reserve_isbn_list_shortwait(
      reserve_calculator.calc.shortwait_reserve_book_num)
  longwait_isbn_list = reserve_calculator.get_reserve_isbn_list_longwait(
      reserve_calculator.calc.longwait_reserve_book_num)

  # 予約APIの準備
  tool = IchikawaModule()
  tool.set_sleep_time(sleep)

  # ログイン
  tool.execute_login_procedure()

  # 待ち時間小の初期の予約処理を実施
  logging.info("%d books will be reserved as shortwait" % len(shortwait_isbn_list))
  for isbn in shortwait_isbn_list:
    result = tool.reserve_book(isbn)
    if (result):
      logging.info(f"{isbn} was successfully reserved.")
    else:
      warnings.warn(f"{isbn} was not reserved.")

  # 待ち時間大の初期の予約処理を実施
  logging.info("%d books will be reserved as longwait" % len(longwait_isbn_list))
  for isbn in longwait_isbn_list:
    result = tool.reserve_book(isbn)
    if (result):
      logging.info(f"{isbn} was successfully reserved.")
    else:
      warnings.warn(f"{isbn} was not reserved.")

  tool.close_session()


if __name__ == "__main__":
  main()
