import logging.config

import pandas as pd


class BooklogDataHandler:

  def __init__(self, booklog_data_path: str):
    columns = [
        'サービスID', 'アイテムID', '13桁ISBN', 'カテゴリ', '評価', '読書状況', 'レビュー', 'タグ', '読書メモ(非公開)', '登録日時',
        '読了日', 'タイトル', '作者名', '出版社名', '発行年', 'ジャンル', 'ページ数', '価格'
    ]
    # 桁数が多い数はintではなくfloatで扱われてしまう問題があるためstrで扱うことにする
    self.df = pd.read_csv(booklog_data_path,
                          encoding="utf-8",
                          header=None,
                          names=columns,
                          dtype=object)

  def read_completed(self, isbn: str) -> bool:
    logging.debug(f"Try to check book reading status of ISBN={isbn}")
    # isbnは通常13桁("13桁ISBN")と一致するものが入力される想定だが、まれに10桁ISBN("アイテムID")に
    # 一致するものが入力されることがあるのでそのケースも取り扱えるようにする (e.g. 深夜特急  3)
    df = self.df[(self.df['13桁ISBN'] == isbn) | (self.df['アイテムID'] == isbn)]
    if len(df) > 1:
      logging.info(f"Multiple books exist for ISBN={isbn} book in Booklog data.")
      return False
    elif len(df) == 0:
      logging.info(f"ISBN={isbn} book is not found in Booklog list.")
      return False
    else:
      logging.info(f"ISBN={isbn} book is found in Booklog list.")
      status = df['読書状況'].iloc[0]
      return status == '読み終わった'
