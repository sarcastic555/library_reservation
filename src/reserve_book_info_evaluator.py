import os
import warnings

import numpy as np
import pandas as pd


class NowLendingListInfo:

  def __init__(self, filename: str):
    if not os.path.exists(filename):
      warnings.warn(f"{filename} not found. Skip reading nowreading file.")
      self.__nowlending_num = 0
      self.__minimum_remain_day = np.nan
      self.__read_complete_num = 0
    else:
      df = pd.read_csv(filename)
      self.__nowlending_num = len(df)
      self.__minimum_remain_day = np.nan if len(df) == 0 else df['remainday'].min()
      self.__read_complete_num = 0 if len(df) == 0 else (df['read_completed'] == 1).sum()

  # 単体テストのためにgetterを作成する
  def nowlending_num(self) -> int:
    return self.__nowlending_num

  def minimum_remain_day(self) -> int:
    return self.__minimum_remain_day

  def read_complete_num(self) -> int:
    return self.__read_complete_num


class NowReservingListInfo:

  def __init__(self, filename):
    if not os.path.exists(filename):
      warnings.warn(f"{filename} not found. Skip reading nowreserving file.")
      self.__prepared_book_num = 0
      self.__shortwait_book_num = 0
      self.__longwait_book_num = 0
    else:
      df = pd.read_csv(filename)
      self.__prepared_book_num = len(df[df['waitnum'] == 0])
      self.__shortwait_book_num = len(df[df['waitnum'] == 1])
      self.__longwait_book_num = len(df[(df['waitnum'] > 1) & (df['waitnum'] != 99)])

  # 単体テストのためにgetterを作成する
  def prepared_book_num(self) -> int:
    return self.__prepared_book_num

  def shortwait_book_num(self) -> int:
    return self.__shortwait_book_num

  def longwait_book_num(self) -> int:
    return self.__longwait_book_num


class ReserveListInfo:

  def __init__(self, filename: str):
    df = pd.read_csv(filename)
    self.__candidate_list_size = len(df)

  # 単体テストのためにgetterを作成する
  def candidate_list_size(self) -> int:
    return self.__candidate_list_size
