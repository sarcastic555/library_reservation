import argparse
import os
import sys
from unittest import mock

import pandas as pd
from mock import MagicMock, Mock

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from reserve_book_selector import *


# 予約冊数が0の場合は空の予約リストが出力される
def test_get_reserve_isbn_list1() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222']})
  df_lend = pd.DataFrame({'ISBN': ['333333', '444444']})
  reserve_num = 0
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == [])


# 貸し出し中資料と一致しない予約リストが作成される
def test_get_reserve_isbn_list2() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222']})
  df_lend = pd.DataFrame({'ISBN': ['222222', '333333']})
  reserve_num = 1
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == ['111111'])


# 貸し出し中資料と一致しない予約リストが作成される
def test_get_reserve_isbn_list3() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222']})
  df_lend = pd.DataFrame({'ISBN': ['111111', '333333']})
  reserve_num = 1
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == ['222222'])


# 貸し出し中資料と一致しない予約リストが作成される
def test_get_reserve_isbn_list4() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333']})
  df_lend = pd.DataFrame({'ISBN': ['222222', '444444']})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (set(reservelist) == set(['111111', '333333']))


# 貸し出し中資料と一致しない資料の数が不十分の場合は選べる分だけ選ぶ
def test_get_reserve_isbn_list5() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333']})
  df_lend = pd.DataFrame({'ISBN': ['222222', '333333']})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == ['111111'])


# 貸し出し中資料と一致しない資料の数が不十分の場合は選べる分だけ選ぶ
def test_get_reserve_isbn_list6() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333', '444444']})
  df_lend = pd.DataFrame({'ISBN': ['111111', '222222', '333333']})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == ['444444'])


# 貸し出し中資料と一致しない資料の数が不十分の場合は選べる分だけ選ぶ
def test_get_reserve_isbn_list7() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333', '444444']})
  df_lend = pd.DataFrame({'ISBN': ['111111', '222222', '333333', '444444']})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (reservelist == [])


# 貸し出し中資料と一致するものがないときは好きに選んで良い
def test_get_reserve_isbn_list8() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333', '444444']})
  df_lend = pd.DataFrame({'ISBN': ['555555', '666666', '777777']})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (len(reservelist) == 2)
  assert (set(reservelist).issubset(set(df_reserve_list['13桁ISBN'])))


# 貸し出し中資料がないときは好きに選んで良い
def test_get_reserve_isbn_list9() -> None:
  df_reserve_list = pd.DataFrame({'13桁ISBN': ['111111', '222222', '333333', '444444']})
  df_lend = pd.DataFrame({'ISBN': []})
  reserve_num = 2
  reservelist = get_reserve_isbn_list(df_reserve_list, df_lend, reserve_num)
  assert (len(reservelist) == 2)
  assert (set(reservelist).issubset(set(df_reserve_list['13桁ISBN'])))
