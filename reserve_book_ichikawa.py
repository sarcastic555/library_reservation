import logging
import os
import random
import warnings

import pandas as pd

import tool_ichikawa

def get_reserve_isbn_list(booklist_filename, reservenum, reservenum_per_day, nowreading_info):
    booklist_df = pd.read_csv(booklist_filename)
    print("start selecting ISBN list from booklist database")
    booklistnum=len(booklist_df)
    print("boolist num = %d"%booklistnum)
    nowreading_df = nowreading_info.df
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
            while j < len(nowreading_df):
                index_candidate=random.choice(range(booklistnum))
                if int(float(booklist_df.iloc[index_candidate]['13桁ISBN'])) == int(nowreading_df.iloc[j]['ISBN']):
                    continue
                j+=1
            ISBNlist.append(str(int(booklist_df.iloc[index_candidate]['13桁ISBN'])))
                
        print(ISBNlist)
        return ISBNlist


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
    self.prepared_book_num = len(self.df[self.df['waitnum']==0])
    self.shortwait_book_num = len(self.df[self.df['waitnum']==1])
    self.longwait_book_num = len(self.df[self.df['waitnum']>1])
    logging.info("Number of prepared book = {self.prepared_book_num}")
    logging.info("Number of shortwait book in reserve list = {self.shortwait_book_num}")
    logging.info("Number of longwait book in reserve list = {self.longwait_book_num}")
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
  reservenum_max = 10   ## 最大で予約できる冊数
  reservenum_per_day = 1 ## 1日にshortwaitとlongwaitをそれぞれ予約する冊数
  shortwait_reservenum_limit = 7 ## shortwait予約可能最大数
  longwait_reservenum_limit = 3 ## longwait予約可能最大数

  def __init__(self, nowreading_info, reserve_list_info):
    ### パラメータ設定
    self.prepared_book_num_in_reserved_list = nowreading_info.prepared_book_num # 予約リスト内ですでに受け取り完了の本の冊数
    self.shortwait_book_num_in_reserved_list = nowreading_info.shortwait_book_num # 予約リスト内で待ち時間小の本の冊数
    self.longwait_book_num_in_reserved_list = nowreading_info.longwait_book_num # 予約リスト内で待ち時間大の本の冊数

    self.minimum_remain_day = nowreading_info.minimum_remain_day

    assert self.shortwait_book_num_in_reserved_list + self.longwait_book_num_in_reserved_list <= self.reservenum_max

  def calculate_maximum_reservation_num(self):
    self.shortwait_reserve_book_num = min(
      self.__class__.shortwait_reservenum_limit - self.prepared_book_num_in_reserved_list - self.shortwait_book_num_in_reserved_list,
      self.__class__.reservenum_max - self.prepared_book_num_in_reserved_list - self.shortwait_book_num_in_reserved_list-self.longwait_reservenum_limit)
    self.longwait_reserve_book_num = min(
      self.__class__.longwait_reservenum_limit - self.longwait_book_num_in_reserved_list,
      self.__class__.reservenum_max - self.prepared_book_num_in_reserved_list - self.shortwait_book_num_in_reserved_list - self.longwait_book_num_in_reserved_list - self.shortwait_reserve_book_num) ## longwaitは最大でも1日に1冊しか予約しない

  def consider_remaining_date_for_reserve_book_num(self):
    if (self.minimum_remain_day < 2) or (self.minimum_remain_day > 8):
      self.shortwait_reserve_book_num = 0

  def compare_reserve_num_to_reserve_list_size(self):
    self.shortwait_reserve_book_num = min(self.shortwait_reserve_book_num, self.shortwait_book_num_in_reserved_list)
    self.longwait_reserve_book_num = min(self.longwait_reserve_book_num, self.longwait_book_num_in_reserved_list)

  def calculate_reservation_num(self):
    self.calculate_maximum_reservation_num()
    self.consider_remaining_date_for_reserve_book_num()
    self.compare_reserve_num_to_reserve_list_size()


def main():
  logging.basicConfig(level=logging.INFO,
                      format='%(levelname)s : %(asctime)s : %(message)s')
  # 現在貸し出し中/予約中の本のリストを取得
  reading_info = NowReadingListInfo("list/nowreading.csv")
  logging.info(f"Prepared book num in reserved list = {reading_info.prepared_book_num}")
  logging.info(f"Short wait book num in reserved list = {reading_info.shortwait_book_num}")
  logging.info(f"Long wait book num in reserved list = {reading_info.longwait_book_num}")

  # 予約したい本リストを取得
  reserved_info = ReserveListInfo(shortwait_filename="list/no_reservation.csv",
                                  longwait_filename="list/has_reservation.csv")
  logging.info(f"Shortwait reservation list size = {reserved_info.shortwait_reservelist_num}")
  logging.info(f"Longwait reservation list size = {reserved_info.longwait_reservelist_num}")

  # 予約予定冊数を導出
  calc = ReserveBookNumCalculator(reading_info, reserved_info)
  calc.calculate_reservation_num()
  logging.info(f"Target boook num of short wait = {calc.shortwait_reserve_book_num}")
  logging.info(f"Target boook num of long wait = {calc.longwait_reserve_book_num}")

  # 予約を実施
  ### 予約ISBNリストの作成
  logging.info('Create shortwait reserve book list start')
  ISBNlist_shortwait = get_reserve_isbn_list("list/no_reservation.csv",
                                             calc.shortwait_reserve_book_num,
                                             ReserveBookNumCalculator.reservenum_per_day,
                                             reading_info)
  logging.info('Number of ISBN list of short wait = %d' % len(ISBNlist_shortwait))
  logging.info('Create shortwait reserve book list end')
  logging.info('Create longwait reserve book list start')
  ISBNlist_longwait=get_reserve_isbn_list("list/has_reservation.csv",
                                          calc.longwait_reserve_book_num,
                                          ReserveBookNumCalculator.reservenum_per_day,
                                          reading_info)
  logging.info('Number of ISBN list of long wait = %d' % len(ISBNlist_longwait))
  logging.info('Create longwait reserve book list end')

  #### reserve books ###########
  logging.info("Book reservation start")
  reserver = tool_ichikawa.IchikawaModule()
  reserver.set_debug_mode(True)
  reserver.set_sleep_time(3)

  if len(ISBNlist_longwait) > 0:
    logging.info("Start reserving longwait book")
    reserver.reserve_book(ISBNlist_longwait)
    logging.info("End reserving longwait book")

  if len(ISBNlist_shortwait) > 0:
    logging.info("Start reserving shortwait book")
    reserver.reserve_book(ISBNlist_shortwait)
    print("end reserving shortwait book")

  logging.info("Book reservation end")

if __name__ == "__main__":
  main()
