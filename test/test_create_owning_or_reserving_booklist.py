import os
import sys
from unittest import mock

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from create_owning_or_reserving_booklist import (get_rental_book_df, get_reserving_book_df,
                                                 get_waitnum_from_status)
#from tools.tool_ichikawa import *
from tools.book_info import RentalBookInfo, ReserveBookInfo


def test_get_waitnum_from_status1() -> None:
  waitnum = get_waitnum_from_status('利用可能')
  assert (waitnum == 0)


def test_get_waitnum_from_status2() -> None:
  waitnum = get_waitnum_from_status('準備中')
  assert (waitnum == 0)


def test_get_waitnum_from_status3() -> None:
  waitnum = get_waitnum_from_status('配送中')
  assert (waitnum == 0)


def test_get_waitnum_from_status4() -> None:
  waitnum = get_waitnum_from_status('順番待ち (37位)')
  assert (waitnum == 37)


def test_get_waitnum_from_status5() -> None:
  waitnum = get_waitnum_from_status('順番待ち (7位)')
  assert (waitnum == 7)


def test_get_waitnum_from_status6() -> None:
  waitnum = get_waitnum_from_status('確認待ち (1位)')
  assert (waitnum == 1)


def test_get_waitnum_from_status7() -> None:
  waitnum = get_waitnum_from_status('返却待ち (14位)')
  assert (waitnum == 14)


# リストサイズが0の時は出力dataframeのサイズも0であることのテスト
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
def test_get_lend_df1(mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 0
  df = get_rental_book_df(sleep=0)
  assert (len(df) == 0)


# リストサイズ1のデータを読んでdataframeに反映されることのテスト
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_rental_book_information')
def test_get_lend_df2(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = RentalBookInfo()
  book_info.title = 'book_title'
  book_info.isbn = '111111'
  mock_book_info.return_value = book_info
  booklog_sample_file = os.path.join(os.path.dirname(__file__), 'data/booklog_sample.csv')
  df = get_rental_book_df(sleep=0, booklog_file=booklog_sample_file)
  assert (df['title'].iloc[0] == 'book_title')


# 読書状況statusの確認1: ブクログデータリストにない本の読書完了状況は読み終わっていない判定されること
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_rental_book_information')
def test_get_lend_df3(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = RentalBookInfo()
  book_info.title = 'book_title'
  book_info.isbn = '1111'
  mock_book_info.return_value = book_info
  booklog_sample_file = os.path.join(os.path.dirname(__file__), 'data/booklog_sample.csv')
  df = get_rental_book_df(sleep=0, booklog_file=booklog_sample_file)
  read_completed = df['read_completed'].iloc[0]
  assert (read_completed == 0)  # 0: 読み終わっていない


# 読書状況statusの確認2: ブクログデータリストで読み終わった本の読書完了状況はTrueとなること
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_rental_book_information')
def test_get_lend_df4(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = RentalBookInfo()
  book_info.title = 'book_title'
  book_info.isbn = '9784022645241'
  mock_book_info.return_value = book_info
  booklog_sample_file = os.path.join(os.path.dirname(__file__), 'data/booklog_sample.csv')
  df = get_rental_book_df(sleep=0, booklog_file=booklog_sample_file)
  read_completed = df['read_completed'].iloc[0]
  assert (read_completed == 1)  # 1: 読み終わっている


# 読書状況statusの確認2: ブクログデータリストで読みたい本の読書完了状況はFalseとなること
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_rental_book_information')
def test_get_lend_df5(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = RentalBookInfo()
  book_info.title = 'book_title'
  book_info.isbn = '9784167110062'
  mock_book_info.return_value = book_info
  booklog_sample_file = os.path.join(os.path.dirname(__file__), 'data/booklog_sample.csv')
  df = get_rental_book_df(sleep=0, booklog_file=booklog_sample_file)
  read_completed = df['read_completed'].iloc[0]
  assert (read_completed == 0)  # 0: 読み終わっていない


@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_under_reservation_book_information')
def test_get_reserve_df1(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = ReserveBookInfo()
  book_info.title = 'book_title'
  book_info.reserve_status = '利用可能'
  mock_book_info.return_value = book_info
  df = get_reserving_book_df(sleep=0)
  assert (len(df) == 1)
  assert (df['title'].iloc[0] == 'book_title')


# 「本人取消」の資料がdataframeに登録されないことの確認
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_under_reservation_book_information')
def test_get_reserve_df2(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = ReserveBookInfo()
  book_info.title = 'book_title'
  book_info.reserve_status = '本人取消'
  mock_book_info.return_value = book_info
  df = get_reserving_book_df(sleep=0)
  assert (len(df) == 0)


# 「期限切れ」の資料がdataframeに登録されないことの確認
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_under_reservation_book_information')
def test_get_reserve_df3(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = ReserveBookInfo()
  book_info.title = 'book_title'
  book_info.reserve_status = '期限切れ'
  mock_book_info.return_value = book_info
  df = get_reserving_book_df(sleep=0)
  assert (len(df) == 0)


# 待ち順位が正しく判定されることの確認
@mock.patch('tools.tool_ichikawa.IchikawaModule.__init__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.__del__')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_num_of_total_books')
@mock.patch('tools.tool_ichikawa.IchikawaModule.get_under_reservation_book_information')
def test_get_reserve_df4(mock_book_info, mock_book_num, mock_del, mock_init) -> None:
  mock_init.return_value = None
  mock_del.return_value = None
  mock_book_num.return_value = 1
  book_info = ReserveBookInfo()
  book_info.title = 'book_title'
  book_info.reserve_status = '順番待ち (37位)'
  mock_book_info.return_value = book_info
  df = get_reserving_book_df(sleep=0)
  assert (len(df) == 1)
  assert (df['waitnum'].iloc[0] == 37)
