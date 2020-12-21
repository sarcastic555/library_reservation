import os
import sys
import numpy as np
import pandas as pd
from mock import MagicMock, Mock
from unittest import mock
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from src.book_classifier import BookClassifier

test_data_path = os.path.join(os.path.dirname(__file__), 'data')

# 読み終わった本が2冊、読みたい本が2冊（うち1冊の13桁ISBNは無効）を入力するので
# 1冊のみ抽出されることが期待値
def test_get_want_read_book_list() -> None:
  bc = BookClassifier(sleep=0)
  df = bc.get_want_read_book_list(os.path.join(test_data_path, 'booklog_list.csv'))
  assert(len(df) == 1)

# 貸し出し中資料のデータを正しく読めるか
def test_get_now_reading_book_list1() -> None:
  bc = BookClassifier(sleep=0)
  df = bc.get_now_reading_book_list(os.path.join(test_data_path, 'lend.csv'))
  assert(len(df) == 1)
  assert(df['title'].iloc[0] == 'dummy_title')

# 存在しないパスが指定された場合は警告を出した上で空のdataframeを返す
def test_get_now_reading_book_list2() -> None:
  bc = BookClassifier(sleep=0)
  with pytest.warns(UserWarning):
    df = bc.get_now_reading_book_list('not_exist_path')
  assert(len(df) == 0)

# 書籍が貸し出し中であることの判定
def test_book_is_rental1() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 111111})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  result = bc.book_is_rental_or_reserving(book_info=book_info, nowreading_df=rental_df)
  assert (result)

# 書籍が貸し出し中でないことの判定
def test_book_is_rental2() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 333333})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  result = bc.book_is_rental_or_reserving(book_info=book_info, nowreading_df=rental_df)
  assert (not result)

# 書籍が貸し出し中でないことの判定
def test_book_is_rental3() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 111111})
  result = bc.book_is_rental_or_reserving(book_info=book_info, nowreading_df=None)
  assert (not result)

# 13桁ISBNが無効の書籍はnot_foundと判定される
def test_evaluate_book_status1() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': np.nan})
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=None)
  assert (status == 'not_found')

# 貸し出し中の書籍であることの判定
def test_evaluate_book_status2() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 111111})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=rental_df)
  assert (status == 'rental_or_reserving')

# 貸し出し中の書籍ではないことの判定(No.1)
def test_evaluate_book_status3() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 9784103526810})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=rental_df)
  assert (status == 'has_reservation' or status == 'no_reservation')

# 貸し出し中の書籍ではないことの判定(No.2)
def test_evaluate_book_status4() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 9784000052092})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=rental_df)
  assert (status == 'has_reservation' or status == 'no_reservation')

# 見つからない書籍の判定
def test_evaluate_book_status5() -> None:
  bc = BookClassifier(sleep=0)
  book_info = pd.Series({'13桁ISBN': 333333})
  rental_df = pd.DataFrame({'ISBN': [111111, 222222]})
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=rental_df)
  assert (status == 'not_found')