import logging
import os
import random
import warnings
from typing import List

import numpy as np
import pandas as pd


class NowLendingListInfo:

  def __init__(self, filename: str):
    if not os.path.exists(filename):
      warnings.warn(f"{filename} not found. Skip reading nowreading file.")
      self.__nowlending_num = 0
      self.__minimum_remain_day = np.nan
    else:
      df = pd.read_csv(filename)
      self.__nowlending_num = len(df)
      self.__minimum_remain_day = np.nan if len(df) == 0 else df['remainday'].min()

  # 単体テストのためにgetterを作成する
  def nowlending_num(self):
    return self.__nowlending_num

  def minimum_remain_day(self):
    return self.__minimum_remain_day


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
  def prepared_book_num(self):
    return self.__prepared_book_num

  def shortwait_book_num(self):
    return self.__shortwait_book_num

  def longwait_book_num(self):
    return self.__longwait_book_num


class ReserveListInfo:

  def __init__(self, filename: str):
    df = pd.read_csv(filename)
    self.__candidate_list_size = len(df)

  def candidate_list_size(self):
    return self.__candidate_list_size
