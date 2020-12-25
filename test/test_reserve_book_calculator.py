import argparse
import os
import sys
from unittest import mock

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from reserve_book_calculator import calculate_reserve_book_num


# 予約枠が余っているときはshortwaitとlongwaitを1冊ずつ予約
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info1(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 0
  shortwait.return_value = 0
  prepared.return_value = 0
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 1)
  assert (longwait_reserve == 1)


# 受け取り待ちの資料が十分あるときはshortwaitは予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info2(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 1
  shortwait.return_value = 0
  prepared.return_value = 7
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 1)


# shortwaitの予約中の資料が十分あるときはshortwaitは予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info3(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 1
  shortwait.return_value = 8
  prepared.return_value = 0
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 1)


# shortwait+preparedの予約中の資料が十分あるときはshortwaitは予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info4(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 1
  shortwait.return_value = 4
  prepared.return_value = 4
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 1)


# shortwait+preparedの予約中の資料が多すぎる時はshortwaitだけでなくlongwaitも予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info5(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 0
  shortwait.return_value = 6
  prepared.return_value = 4
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 0)


# longwaitの予約中の資料が多すぎる時はlongwaitは予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info6(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 3
  shortwait.return_value = 2
  prepared.return_value = 3
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 1)
  assert (longwait_reserve == 0)


# shortwaitもlongwaitも多すぎる時はどちらもは予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info7(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 4
  shortwait.return_value = 8
  prepared.return_value = 0
  remainday.return_value = 5

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 0)


# 返却期限が遠い時はshortwaitのみ予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info8(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 1
  shortwait.return_value = 1
  prepared.return_value = 1
  remainday.return_value = 13

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 1)


# 返却期限が近すぎるはshortwaitのみ予約しない
@mock.patch('src.reserve_book_info_evaluator.NowLendingListInfo.minimum_remain_day')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.prepared_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.shortwait_book_num')
@mock.patch('src.reserve_book_info_evaluator.NowReservingListInfo.longwait_book_num')
def test_reserve_book_info9(longwait, shortwait, prepared, remainday) -> None:
  longwait.return_value = 1
  shortwait.return_value = 1
  prepared.return_value = 1
  remainday.return_value = 0

  options = argparse.ArgumentParser()
  options.now_lend_file = os.path.join(os.path.dirname(__file__), 'data/sample2.csv')
  options.now_reserve_file = options.now_lend_file
  options.no_reservation_file = options.now_lend_file
  options.has_reservation_file = options.now_lend_file
  df = calculate_reserve_book_num(options)

  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  assert (shortwait_reserve == 0)
  assert (longwait_reserve == 1)
