import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from classify_list import BookClassifier


def test_get_want_read() -> None:
  bc = BookClassifier(sleep=1)
  df = bc.get_want_read_book_list(os.path.join(os.path.dirname(__file__), "data/sample.csv"))
  assert (len(df) == 2)


def test_read_booklist() -> None:
  bc = BookClassifier(sleep=1)
  df = bc.read_booklist(os.path.join(os.path.dirname(__file__), "data/sample.csv"))
  assert (len(df) == 2)


def test_book_status_nan() -> None:
  bc = BookClassifier(sleep=1)
  book_info = pd.Series({'13桁ISBN': np.nan})
  nowreading_df = pd.DataFrame()
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=nowreading_df)
  assert (status == 'not_found')


def test_book_status_rental() -> None:
  bc = BookClassifier(sleep=1)
  book_info = pd.Series({'13桁ISBN': 333333})
  nowreading_df = pd.DataFrame([[333333, 'hoge'], [222222, 'aho']], columns=['ISBN', 'temp'])
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=nowreading_df)
  assert (status == 'rental_or_reserving')


def test_book_status_not_found() -> None:
  bc = BookClassifier(sleep=1)
  invalid_isbn = 444444
  book_info = pd.Series({'13桁ISBN': invalid_isbn})
  nowreading_df = pd.DataFrame([[333333, 'hoge'], [222222, 'aho']], columns=['ISBN', 'temp'])
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=nowreading_df)
  assert (status == 'not_found')


def test_book_status_found() -> None:
  bc = BookClassifier(sleep=1)
  valid_isbn = 9784101010137
  book_info = pd.Series({'13桁ISBN': valid_isbn})
  nowreading_df = pd.DataFrame([[333333, 'hoge'], [222222, 'aho']], columns=['ISBN', 'temp'])
  status = bc.evaluate_book_status(book_info=book_info, nowreading_df=nowreading_df)
  assert (status == 'no_reservation' or status == 'has_reservation')


def test_create_all_book_status() -> None:
  bc = BookClassifier(sleep=1)
  notread_df = pd.DataFrame([[333333, 'hoge'], [222222, 'aho']], columns=['13桁ISBN', 'temp'])
  ret_list = bc.create_all_book_status(notread_df=notread_df, nowreading_df=None)
  assert (len(ret_list) == 2)
