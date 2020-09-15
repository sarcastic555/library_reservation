# /usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from tool_ichikawa import *
import sys


### 予約カゴを空にする
def clean_reserve_busket(sleep=3):
  tool = IchikawaModule()
  tool.set_sleep_time(sleep)

  ## ログイン処理
  tool.execute_login_procedure()

  ## 予約カゴに入っている本の冊数を取得
  totalnum_basket = tool.get_num_of_reserve_basket_books()

  ## 予約カゴに入っている書籍冊数が0であれば以降の処理をスキップ
  if totalnum_basket == 0:
    logging.info("No book is found in reserve book basket.")
    logging.info("Skip process of clearing reserve basket.")
    return
  logging.info(f"{totalnum_basket} books are found in reserve book basket.")
  logging.info("Clear reserve book basket.")

  ## 予約カゴに入っている書籍のchunk_valueを取得
  chunk_value_list = []
  chunk_value_string = ""
  for i in range(totalnum_basket):
    chunk_value = soup.find(
        'ol', class_="list-book result hook-check-all").find_all('label')[i].find('input')['value']
    chunk_value_list.append(chunk_value)
    chunk_value_string += "%s " % chunk_value_string
  self.basket_delete_params['chk_check'] = chunk_value_list
  chunk_value_string = chunk_value_string.rstrip(" ")  ## 最後のスペースを削除
  self.basket_delete_confirm_params['hid_idlist'] = chunk_value_string

  ## 予約カゴを空にする
  tool.clear_reserve_basket()
  totalnum_basket = tool.get_num_of_reserve_basket_books()
  logging.info(f"Number of books in reserve basket after clear process = {totalnum_basket}")

  ### ログアウトして、sessionを終了して終わる
  tool.close_session()


def main():
  clean_reserve_busket(sleep=3)


if __name__ == "__main__":
  main()
