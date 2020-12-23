import argparse
import logging
from typing import List
import pandas as pd
import random
import os

def options() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser()
  parser.add_argument('--no_reservation_booklist_file', help='Input path to no reservation book list.', default='list/no_reservation.csv')
  parser.add_argument('--has_reservation_booklist_file', help='Input path to with reservation book list.', default='list/has_reservation.csv')
  parser.add_argument('--shortwait_reserve_book_num_file', help='Input path to file where shortwait reserve book number info is recorded.', default='result/shortwait_reserve_size.csv')
  parser.add_argument('--longwait_reserve_book_num_file', help='Input path to file where longwait reserve book number info is recorded.', default='result/longwait_reserve_size.csv')
  parser.add_argument('--lend_file', help='Input path to lend book list.', default='list/lend.csv')
  parser.add_argument('--output_shortwait_reserve_list', help='Output path to shortwait reserve book list.', default='list/shortwait_reserve_list.csv')
  parser.add_argument('--output_longwait_reserve_list', help='Output path to longwait reserve book list.', default='list/longwait_reserve_list.csv')

  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args

def get_reserve_isbn_list(want_reserve_list_df: pd.DataFrame,
                          nowlending_df: pd.DataFrame,
                            reserve_num: int) -> List[str]:
    if (reserve_num==0): return []
    assert reserve_num > 0
    booklist_num = len(want_reserve_list_df)
    isbn_list = []
    # [0, 1, ... N-1]をシャッフルしたものをインデックスとして使用して探索する
    search_index_list = list(range(booklist_num))
    random.shuffle(search_index_list)
    for i in search_index_list:
      reserve_book_isbn = int(float(want_reserve_list_df.iloc[i]['13桁ISBN']))
      matched = False
      for j in range(len(nowlending_df)):
        lend_book_isbn = int(nowlending_df.iloc[j]['ISBN'])
        if reserve_book_isbn == lend_book_isbn:
          matched = True
          break
        j += 1
      if not matched:
        isbn_list.append(str(int(want_reserve_list_df.iloc[i]['13桁ISBN'])))
        if (len(isbn_list) >= reserve_num): break
    return isbn_list

def main(options) -> None:
    lend_df = pd.read_csv(options.lend_file)

    # reserve shortwait books
    booklist_df = pd.read_csv(options.no_reservation_booklist_file)
    reserve_num = int(open(options.shortwait_reserve_book_num_file, 'r').read())
    reservelist = get_reserve_isbn_list(booklist_df, lend_df, reserve_num)
    os.makedirs(os.path.dirname(options.output_shortwait_reserve_list), exist_ok=True)
    with open(options.output_shortwait_reserve_list, 'w') as f:
      for reserve_isbn in reservelist:
        f.write(str(reserve_isbn) + '\n')

    # reserve longwait books
    booklist_df = pd.read_csv(options.has_reservation_booklist_file)
    reserve_num = int(open(options.longwait_reserve_book_num_file, 'r').read())
    reservelist = get_reserve_isbn_list(booklist_df, lend_df, reserve_num)
    os.makedirs(os.path.dirname(options.output_longwait_reserve_list), exist_ok=True)
    with open(options.output_longwait_reserve_list, 'w') as f:
      for reserve_isbn in reservelist:
        f.write(str(reserve_isbn) + '\n')


if __name__ == '__main__':
    options = options()
    main(options=options)