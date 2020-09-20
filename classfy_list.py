import argparse
import datetime
import logging
import os
import time
import warnings

import numpy as np
import pandas as pd

import tool_culil


class BookClassifier:
  columnname = [
      'サービスID', 'アイテムID', '13桁ISBN', 'カテゴリ', '評価', '読書状況', 'レビュー', 'タグ', '読書メモ(非公開)', '登録日時', '読了日',
      'タイトル', '作者名', '出版社名', '発行年', 'ジャンル', 'ページ数', '価格'
  ]

  def __init__(self, sleep=1):
    logging.info("BookClassifier constructor called")
    self.sleeptime = sleep  # [sec]
    logging.info(f"sleep time = {self.sleeptime} sec")

  def get_want_read_book_list(self, booklist_file):
    logging.info("BookClassifier::get_want_read_book_list called")
    logging.info(f"reading {booklist_file} as all book list file")
    df = pd.read_csv(booklist_file, encoding="utf-8", header=None, names=self.__class__.columnname)
    df = df[df['読書状況'] == '読みたい']
    df = df.dropna(subset=['13桁ISBN'])  ## 13桁ISBNが無効値である書籍は対象外とする
    df = df.astype({'13桁ISBN': int})
    df = df.drop([
        'サービスID', 'アイテムID', 'カテゴリ', '評価', 'レビュー', 'タグ', '読書メモ(非公開)', '登録日時', '読了日', '出版社名', '発行年',
        'ジャンル', 'ページ数', '価格'
    ],
                 axis=1)  ## 不要な列を削除
    df['waitstatus'] = 'Nan'
    df = df.reset_index(drop=True)
    logging.info("Number of want read book = %d" % len(df))
    return df

  def get_now_reading_book_list(self, booklist_file):
    logging.info("BookClassifier::get_now_reading_book_list called")
    logging.info(f"reading {booklist_file} as now reading list file")
    if not os.path.exists(booklist_file):
      warnings.warn(f"{booklist_file} not found. Skip reading the file")
      return pd.DataFrame(columns=['ISBN'])
    df = pd.read_csv(booklist_file)
    logging.info("Number of reading book = %d" % len(df))
    return df

  def book_is_rental_or_reserving(self, book_info, nowreading_df):
    return len(nowreading_df[nowreading_df['ISBN'] == int(book_info['13桁ISBN'])]) != 0

  def evaluate_book_status(self, book_info, nowreading_df):
    if (np.isnan(book_info['13桁ISBN'])):
      return 'not_found'
    if self.book_is_rental_or_reserving(book_info, nowreading_df):
      return 'rental_or_reserving'
    ## その他の本
    module = tool_culil.CulilModule()
    renting_possible_flag, renting_soon_flag = module.check_existence_in_library(
        str(book_info['13桁ISBN']))
    if (renting_possible_flag and renting_soon_flag):
      return 'no_reservation'
    elif (renting_possible_flag and not renting_soon_flag):
      return 'has_reservation'
    else:
      return 'not_found'

  def create_all_book_status(self, notread_df, nowreading_df, short=False):
    logging.info(f"BookClassifier::create_all_book_status (short={short}) called")
    book_status_list = []
    # decrease target book num in short execution version
    target_booknum = 8 if short else len(notread_df)
    for i in range(target_booknum):
      if (i + 1) % 10 == 0:
        logging.info("Classfying book %d/%d" % (i + 1, target_booknum))
      time.sleep(self.sleeptime)
      book_info = notread_df.iloc[i]
      status = self.evaluate_book_status(book_info, nowreading_df)
      book_status_list.append(status)
    return pd.Series(book_status_list)

  def output_book_based_on_status(self, df, output_dir):
    logging.info("BookClassifier::output_book_based_on_status called")
    for status in ["not_found", "no_reservation", "has_reservation"]:
      df_target = df[df['waitstatus'] == status]
      logging.info("Number of %s book = %d" % (status, len(df_target)))
      df_target.to_csv(f"{output_dir}/{status}.csv")
    # 注: 現在借りている本が読みたいラベルの本リストに存在しているとは限らないので、
    # 「現在借用中or予約中」「蔵書なし」「予約なし」「予約あり」を足したものと
    # 「読みたいラベルの本」は一致しない可能性がある


def main(short=False):
  logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')
  logging.info("classfy_list_ichikawa.py start")
  bc = BookClassifier(sleep=1)
  df_not_read = bc.get_want_read_book_list("list/alllist.csv")
  df_reading = bc.get_now_reading_book_list("list/nowreading.csv")
  status_series = bc.create_all_book_status(df_not_read, df_reading, short=short)
  df_not_read['waitstatus'] = status_series
  bc.output_book_based_on_status(df_not_read, output_dir="list")
  logging.info("classfy_list_ichikawa.py end")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--short", action='store_true', help="short execution version if true")
  args = parser.parse_args()
  main(short=args.short)
