import argparse
import logging
import os

import pandas as pd

from src.reserve_book_info_evaluator import (NowLendingListInfo, NowReservingListInfo,
                                             ReserveListInfo)


def options() -> argparse:
  parser = argparse.ArgumentParser()
  parser.add_argument('--now_lend_file',
                      help='Input path to lending book list.',
                      default='list/lend.csv')
  parser.add_argument('--now_reserve_file',
                      help='Input path to reserving book list.',
                      default='list/reserve.csv')
  parser.add_argument('--no_reservation_file',
                      help='Input path to no reservation book list.',
                      default='list/no_reservation.csv')
  parser.add_argument('--has_reservation_file',
                      help='Input path to reservation book list.',
                      default='list/has_reservation.csv')
  parser.add_argument('--output_shortwait_reserve_size_file',
                      help='Onput path to shortwait reservation book size.',
                      default='result/shortwait_reserve_size.csv')
  parser.add_argument('--output_longwait_reserve_size_file',
                      help='Onput path to longwait reservation book size.',
                      default='result/longwait_reserve_size.csv')
  parser.add_argument('--output_report_file',
                      help='Onput html to reserve number calculation report.',
                      default='result/report.html')
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args


def highlight_final_result(s, dfsize):
  final_result = s.index >= dfsize - 1  # highlight for last row
  return ['background-color: yellow' if v else '' for v in final_result]


def output_df_to_html(df, output_filename) -> None:
  styles = [
      dict(selector='.col3', props=[('min-width', '100px')]),
      dict(selector='.data', props=[('min-width', '2em')])
  ]
  html = df.style.apply(highlight_final_result, dfsize=len(df),
                        axis=0).hide_index().set_table_styles(styles).set_table_attributes(
                            'border=3 cellspacing=0').render()
  os.makedirs(os.path.dirname(output_filename), exist_ok=True)
  with open(output_filename, 'w') as f:
    f.write(html)


def output_num_to_file(num: int, output_filename) -> None:
  os.makedirs(os.path.dirname(output_filename), exist_ok=True)
  with open(output_filename, 'w') as f:
    f.write(str(num))


def calculate_reserve_book_num(options: argparse) -> pd.DataFrame:
  nowlend = NowLendingListInfo(options.now_lend_file)
  nowreserve = NowReservingListInfo(options.now_reserve_file)
  no_reservation = ReserveListInfo(options.no_reservation_file)
  has_reservation = ReserveListInfo(options.has_reservation_file)

  # パラメータ定義
  reservenum_max = 10  ## 最大で予約できる冊数
  reservenum_per_day = 1  ## 1日にshortwaitとlongwaitをそれぞれ予約する冊数
  shortwait_reservenum_limit = 7  ## shortwait予約可能最大数
  longwait_reservenum_limit = 3  ## longwait予約可能最大数

  # 現在の状況の整理
  df = pd.DataFrame([], columns=['index', 'column', 'common', 'shortwait', 'longwait'])
  df = df.append(
      {
          'index': 0,
          'column': 'reservation goal',
          'common': reservenum_max,
          'shortwait': shortwait_reservenum_limit,
          'longwait': longwait_reservenum_limit
      },
      ignore_index=True)
  # 準備済みの資料はshortwaitとして扱う
  df = df.append(
      {
          'index': 1,
          'column': 'prepared',
          'shortwait': nowreserve.prepared_book_num(),
          'longwait': 0
      },
      ignore_index=True)
  df = df.append(
      {
          'index': 2,
          'column': 'already reserved',
          'shortwait': nowreserve.shortwait_book_num(),
          'longwait': nowreserve.longwait_book_num()
      },
      ignore_index=True)

  # 1: 目標枠に対する不足冊数の算出
  shortwait_reserve = shortwait_reservenum_limit - nowreserve.prepared_book_num(
  ) - nowreserve.shortwait_book_num()
  shortwait_reserve = max(shortwait_reserve, 0)
  longwait_reserve = longwait_reservenum_limit - nowreserve.longwait_book_num()
  longwait_reserve = max(longwait_reserve, 0)
  df = df.append(
      {
          'index': 3,
          'column': 'candidate (0,1,2)',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)

  # 2: shortwaitとlongwaitの予約予定数が予約可能数を越えている場合はshortwaitの予約から削る
  reserve_remain = reservenum_max - nowreserve.prepared_book_num() - nowreserve.shortwait_book_num(
  ) - nowreserve.longwait_book_num()
  df = df.append({
      'index': 4,
      'column': 'reserve remain',
      'common': reserve_remain
  },
                 ignore_index=True)
  longwait_reserve = max(min(longwait_reserve, reserve_remain), 0)
  shortwait_reserve = max(min(shortwait_reserve, reserve_remain - longwait_reserve), 0)
  df = df.append(
      {
          'index': 5,
          'column': 'candidate (3,4)',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)

  # 2: 返却期限日が近づいていない場合はshortwaitの冊数を0にする
  # ただし返却期限日が近くなくても,読み終わっていない本が少ない場合はshortwaitの冊数を0にしない
  df = df.append(
      {
          'index': 6,
          'column': 'remain day for return',
          'common': "%d days" % nowlend.minimum_remain_day()
      },
      ignore_index=True)
  df = df.append(
      {
          'index': 7,
          'column': 'read uncompleted book',
          'common': nowlend.nowlending_num() - nowlend.read_comnplete_num()
      },
      ignore_index=True)
  if ((nowlend.minimum_remain_day() < 2) or (nowlend.minimum_remain_day() > 8)) and (
      nowlend.nowlending_num() - nowlend.read_comnplete_num() > 2):
    shortwait_reserve = 0
  df = df.append(
      {
          'index': 8,
          'column': 'candidate (5,6,7)',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)

  # 3: 予約したい本リストの登録冊数を越えて予約することを防ぐためのガード処理
  df = df.append(
      {
          'index': 9,
          'column': 'reservation candidate size',
          'shortwait': no_reservation.candidate_list_size(),
          'longwait': has_reservation.candidate_list_size()
      },
      ignore_index=True)
  shortwait_reserve = min(shortwait_reserve, no_reservation.candidate_list_size())
  longwait_reserve = min(longwait_reserve, has_reservation.candidate_list_size())
  df = df.append(
      {
          'index': 10,
          'column': 'candidate (8, 9)',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)

  # 4: 1日の予約冊数の上限をかける
  df = df.append({
      'index': 11,
      'column': 'max reserve per day',
      'shortwait': reservenum_per_day
  },
                 ignore_index=True)
  shortwait_reserve = min(shortwait_reserve, reservenum_per_day)
  df = df.append(
      {
          'index': 12,
          'column': 'candidate (10,11)',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)

  # 8: 最終結果
  df = df.append(
      {
          'index': 13,
          'column': 'final result',
          'shortwait': shortwait_reserve,
          'longwait': longwait_reserve
      },
      ignore_index=True)
  return df


def main(options) -> None:

  df = calculate_reserve_book_num(options=options)
  shortwait_reserve = df.iloc[-1]['shortwait']
  longwait_reserve = df.iloc[-1]['longwait']
  logging.info(f"Result: shortwait reserve book num = {shortwait_reserve}")
  logging.info(f"Result: longwait reserve book num = {longwait_reserve}")

  # 数字の遷移をhtmlとして出力
  output_df_to_html(df, options.output_report_file)

  # 最終結果をファイルとして出力
  output_num_to_file(shortwait_reserve, options.output_shortwait_reserve_size_file)
  output_num_to_file(longwait_reserve, options.output_longwait_reserve_size_file)


if __name__ == "__main__":
  options = options()
  main(options)
