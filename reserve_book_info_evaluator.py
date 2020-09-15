import logging
import os
import random
import warnings

import pandas as pd


class NowReadingListInfo:

  def __init__(self, filename):
    if not os.path.exists(filename):
      warnings.warn(f"{filename} not found. Skip reading nowreading file.")
      self.df = None
      self.nowreading_num = 0
      self.prepared_book_num = 0
      self.shortwait_book_num = 0
      self.longwait_book_num = 0
      self.minimum_remain_day = 5
      return
    self.df = pd.read_csv(filename)
    self.nowreading_num = len(self.df)
    self.prepared_book_num = len(self.df[self.df['waitnum'] == 0])
    self.shortwait_book_num = len(self.df[self.df['waitnum'] == 1])
    self.longwait_book_num = len(self.df[self.df['waitnum'] > 1])
    logging.info(f"Number of prepared book = {self.prepared_book_num}")
    logging.info(f"Number of shortwait book in reserve list = {self.shortwait_book_num}")
    logging.info(f"Number of longwait book in reserve list = {self.longwait_book_num}")
    self.minimum_remain_day = self.df['remainday'].min()


class ReserveListInfo:

  def __init__(self, shortwait_filename, longwait_filename):
    self.shortwait_reservelist_df = pd.read_csv(shortwait_filename)
    self.shortwait_reservelist_num = len(self.shortwait_reservelist_df)
    logging.info(f"Numger of shortwait reservelist = {self.shortwait_reservelist_num}")

    self.longwait_reservelist_df = pd.read_csv(longwait_filename)
    self.longwait_reservelist_num = len(self.longwait_reservelist_df)
    logging.info(f"Numger of longwait reservelist = {self.longwait_reservelist_num}")


class ReserveBookNumCalculator:
  reservenum_max = 10  ## 最大で予約できる冊数
  reservenum_per_day = 1  ## 1日にshortwaitとlongwaitをそれぞれ予約する冊数
  shortwait_reservenum_limit = 7  ## shortwait予約可能最大数
  longwait_reservenum_limit = 3  ## longwait予約可能最大数

  def __init__(self, nowreading_info, reserve_list_info):
    ### パラメータ設定
    self.prepared_book_num_in_reserved_list = nowreading_info.prepared_book_num  # 予約リスト内ですでに受け取り完了の本の冊数
    self.shortwait_book_num_in_reserved_list = nowreading_info.shortwait_book_num  # 予約リスト内で待ち時間小の本の冊数
    self.longwait_book_num_in_reserved_list = nowreading_info.longwait_book_num  # 予約リスト内で待ち時間大の本の冊数
    self.shortwait_num_in_want_reserve_list = reserve_list_info.shortwait_reservelist_num  # 待ち時間小の予約リスト冊数
    self.longwait_num_in_want_reserve_list = reserve_list_info.longwait_reservelist_num  # 待ち時間大の予約リスト冊数

    self.minimum_remain_day = nowreading_info.minimum_remain_day

    assert self.shortwait_book_num_in_reserved_list + self.longwait_book_num_in_reserved_list <= self.reservenum_max

  def calculate_maximum_reservation_num(self):
    logging.info("ReserveBookNumCalculator::calculate_maximum_reservation_num called")
    self.shortwait_reserve_book_num = min(
        self.__class__.shortwait_reservenum_limit - self.prepared_book_num_in_reserved_list -
        self.shortwait_book_num_in_reserved_list,
        self.__class__.reservenum_max - self.prepared_book_num_in_reserved_list -
        self.shortwait_book_num_in_reserved_list - self.longwait_reservenum_limit)
    self.longwait_reserve_book_num = min(
        self.__class__.longwait_reservenum_limit - self.longwait_book_num_in_reserved_list,
        self.__class__.reservenum_max - self.prepared_book_num_in_reserved_list -
        self.shortwait_book_num_in_reserved_list - self.longwait_book_num_in_reserved_list -
        self.shortwait_reserve_book_num)  ## longwaitは最大でも1日に1冊しか予約しない

  def consider_remaining_date_for_reserve_book_num(self):
    logging.info("consider_remaining_date_for_reserve_book_num called")
    if (self.minimum_remain_day < 2) or (self.minimum_remain_day > 8):
      logging.info(f"Minimum remain day (={self.minimum_remain_day}) is out of range")
      logging.info("Set shortwait reserve book num to 0")
      self.shortwait_reserve_book_num = 0

  def compare_reserve_num_to_reserve_list_size(self):
    logging.info("ReserveBookNumCalculator::compare_reserve_num_to_reserve_list_size called")
    self.shortwait_reserve_book_num = min(self.shortwait_reserve_book_num,
                                          self.shortwait_num_in_want_reserve_list)
    self.longwait_reserve_book_num = min(self.longwait_reserve_book_num,
                                         self.longwait_num_in_want_reserve_list)

  def consider_maximum_reserve_num_per_day(self):
    logging.info("ReserveBookNumCalculator::consider_maximum_reserve_num_per_day called")
    self.shortwait_reserve_book_num = min(self.shortwait_reserve_book_num,
                                          self.__class__.reservenum_per_day)
    self.longwait_reserve_book_num = min(self.longwait_reserve_book_num,
                                         self.__class__.reservenum_per_day)

  def calculate_reservation_num(self):
    logging.info("ReserveBookNumCalculator::calculate_reservation_num called")
    self.calculate_maximum_reservation_num()
    self.consider_remaining_date_for_reserve_book_num()
    self.compare_reserve_num_to_reserve_list_size()
    self.consider_maximum_reserve_num_per_day()


class ReserveBookInfoEvaluator:

  def __init__(self, nowreading_filename, shortwait_filename, longwait_filename):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')
    self.nowreading_filename = nowreading_filename
    self.shortwait_filename = shortwait_filename
    self.longwait_filename = longwait_filename

    # 現在貸し出し中/予約中の本のリストを取得
    self.reading_info = NowReadingListInfo(self.nowreading_filename)
    self.want_reserve_list_info = ReserveListInfo(shortwait_filename=self.shortwait_filename,
                                                  longwait_filename=self.longwait_filename)

  def calculate_reserve_book_num(self):
    # 予約予定冊数を導出
    self.calc = ReserveBookNumCalculator(self.reading_info, self.want_reserve_list_info)
    self.calc.calculate_reservation_num()

  def print_info(self):
    print(f"Prepared book num in reserved list = {self.reading_info.prepared_book_num}")
    print(f"Short wait book num in reserved list = {self.reading_info.shortwait_book_num}")
    print(f"Long wait book num in reserved list = {self.reading_info.longwait_book_num}")
    print(
        f"Shortwait reservation list size = {self.want_reserve_list_info.shortwait_reservelist_num}"
    )
    print(
        f"Longwait reservation list size = {self.want_reserve_list_info.longwait_reservelist_num}")
    print(f"Target reservation book num of short wait = {self.calc.shortwait_reserve_book_num}")
    print(f"Target reservation book num of long wait = {self.calc.longwait_reserve_book_num}")

  def get_reserve_isbn_list(self, want_reserve_list_df, reserve_num):
    booklist_num = len(want_reserve_list_df)
    if (booklist_num == 0):
      logging.info("!!! Length of booklist num = 0. No book will be reserved.")
      return []
    elif (reserve_num <= 0):
      logging.info("!!! reservenum (%d) <= 0. No book will be reserved." % reserve_num)
      return []
    else:
      ## 今回予約しようとしてる本が、今借りてるor予約してる本リストの中にないことが確認できるまでループを続ける
      isbn_list = []
      for i in range(reserve_num):
        j = 0
        while j < self.reading_info.nowreading_num:
          index_candidate = random.choice(range(booklist_num))
          if int(float(want_reserve_list_df.iloc[index_candidate]['13桁ISBN'])) == int(
              self.reading_info.df.iloc[j]['ISBN']):
            continue
          j += 1
        isbn_list.append(str(int(want_reserve_list_df.iloc[index_candidate]['13桁ISBN'])))
      return isbn_list

  def get_reserve_isbn_list_shortwait(self, reserve_num):
    return self.get_reserve_isbn_list(self.want_reserve_list_info.shortwait_reservelist_df,
                                      reserve_num)

  def get_reserve_isbn_list_longwait(self, reserve_num):
    return self.get_reserve_isbn_list(self.want_reserve_list_info.longwait_reservelist_df,
                                      reserve_num)
