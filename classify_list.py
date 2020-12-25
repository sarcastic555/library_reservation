import argparse
import logging

import pandas as pd

from src.book_classifier import BookClassifier


def options() -> argparse:
  parser = argparse.ArgumentParser()
  parser.add_argument('--booklog_data_file',
                      help='Input path to booklog data file.',
                      default='list/booklog_data.csv')
  parser.add_argument('--lend_file', help='Input path to lend book list.', default='list/lend.csv')
  parser.add_argument('--reserve_file',
                      help='Input path to reserving book list.',
                      default='list/reserve.csv')
  parser.add_argument('--output_not_found_file',
                      help='Output path to book list that is not found.',
                      default='list/not_found.csv')
  parser.add_argument('--output_no_reservation_file',
                      help='Output path to book list without reservation.',
                      default='list/no_reservation.csv')
  parser.add_argument('--output_has_reservation_file',
                      help='Output path to book list with reservation.',
                      default='list/has_reservation.csv')
  parser.add_argument("--short", action='store_true', help="short execution version if true")
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args


def main(options=options):
  logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')
  logging.info("classify_list_ichikawa.py start")
  bc = BookClassifier(sleep=1)
  # read booklog data, and rental and reserving book list
  df_not_read = bc.get_want_read_book_list(options.booklog_data_file)
  df_reading = bc.read_booklist(options.lend_file)
  df_reserving = bc.read_booklist(options.reserve_file)
  df_reading_or_reserving = pd.concat([df_reading, df_reserving])
  # get book status
  status_series = bc.create_all_book_status(df_not_read,
                                            df_reading_or_reserving,
                                            short=options.short)
  df_not_read['waitstatus'] = status_series
  # output dataframe to file
  # 注: 現在借りている本が読みたいラベルの本リストに存在しているとは限らないので、
  # 「現在借用中or予約中」「蔵書なし」「予約なし」「予約あり」を足したものと
  # 「読みたいラベルの本」は一致しない可能性がある
  ## not_found
  df_not_found = df_not_read[df_not_read['waitstatus'] == 'not_found']
  df_not_found.to_csv(options.output_not_found_file)
  ## no_reservation
  df_not_found = df_not_read[df_not_read['waitstatus'] == 'no_reservation']
  df_not_found.to_csv(options.output_no_reservation_file)
  ## no_reservation
  df_not_found = df_not_read[df_not_read['waitstatus'] == 'has_reservation']
  df_not_found.to_csv(options.output_has_reservation_file)

  logging.info("classfy_list_ichikawa.py end")


if __name__ == "__main__":
  options = options()
  main(options=options)
