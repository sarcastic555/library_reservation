import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from src.booklog_manager import BooklogManager


def test_download_data() -> None:
  booklog_manager = BooklogManager(sleep_time=3)
  data = booklog_manager.download_csv_file()
  assert (len(data) > 1000) # データサイズがあるかの確認
  assert ("9784022645241" in data[:300]) # 指定のISBNを含むか

