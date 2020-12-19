import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from download_booklist import BooklogManager


def test_succeed_download() -> None:
  booklog_manager = BooklogManager(sleep_time=3)
  booklog_manager.download_csv_file("temp.csv")
