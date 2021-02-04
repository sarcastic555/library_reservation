import argparse
import logging.config
import warnings

from tools.tool_ichikawa import IchikawaModule

logging.config.fileConfig("log.conf")


def options() -> argparse:
  parser = argparse.ArgumentParser()
  parser.add_argument('--shortwait_reserve_list',
                      help='Input path to booklog data file.',
                      default='list/shortwait_reserve_list.csv')
  parser.add_argument('--longwait_reserve_list',
                      help='Input path to lend book list.',
                      default='list/longwait_reserve_list.csv')
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args


def main(options=options):

  # 予約予定の本のISBNリストの取得
  shortwait_isbn_list = []
  with open(options.shortwait_reserve_list, 'r') as f:
    line = f.readline()
    while line:
      isbn = str(int(line))  # デフォルトだと改行が含まれるので一度intに変換した後に文字列に戻す
      shortwait_isbn_list.append(isbn)
      line = f.readline()
  longwait_isbn_list = []
  with open(options.longwait_reserve_list, 'r') as f:
    line = f.readline()
    while line:
      isbn = str(int(line))  # デフォルトだと改行が含まれるので一度intに変換した後に文字列に戻す
      longwait_isbn_list.append(isbn)
      line = f.readline()

  # 予約APIの準備
  tool = IchikawaModule(sleep=3)
  # 待ち時間小の初期の予約処理を実施
  logging.info("%d books will be reserved as shortwait" % len(shortwait_isbn_list))
  for isbn in shortwait_isbn_list:
    result = tool.reserve_book(isbn)
    if (result):
      logging.info(f"{isbn} was successfully reserved.")
    else:
      warnings.warn(f"{isbn} was not reserved.")

  # 待ち時間大の初期の予約処理を実施
  logging.info("%d books will be reserved as longwait" % len(longwait_isbn_list))
  for isbn in longwait_isbn_list:
    result = tool.reserve_book(isbn)
    if (result):
      logging.info(f"{isbn} was successfully reserved.")
    else:
      warnings.warn(f"{isbn} was not reserved.")


if __name__ == "__main__":
  options = options()
  main(options=options)
