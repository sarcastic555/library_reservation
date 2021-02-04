import logging.config

import pandas as pd

logging.config.fileConfig("../log.conf")


class BooklogDataHandler:

  def __init__(self, booklog_data_path: str):
    columns = [
        'サービスID', 'アイテムID', '13桁ISBN', 'カテゴリ', '評価', '読書状況', 'レビュー', 'タグ', '読書メモ(非公開)', '登録日時',
        '読了日', 'タイトル', '作者名', '出版社名', '発行年', 'ジャンル', 'ページ数', '価格'
    ]
    self.df = pd.read_csv(booklog_data_path, encoding="utf-8", header=None, names=columns)

  def read_completed(self, isbn: str) -> bool:
    logging.info(f"Try to check book reading status of ISBN={isbn}")
    df = self.df[self.df['13桁ISBN'] == int(isbn)]
    if len(df) > 1:
      logging.info(f"Multiple books exist for ISBN={isbn} book in Booklog data.")
      return False
    elif len(df) == 0:
      logging.info(f"ISBN={isbn} book not found in Booklog list.")
      return False
    else:
      status = df['読書状況'].iloc[0]
      return status == '読み終わった'
