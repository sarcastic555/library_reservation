# -*- coding: utf-8 -*-
import argparse
import codecs
import logging.config
import os

from src.booklog_manager import BooklogManager

logging.config.fileConfig("log.conf")


def options():
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_file',
                      help='Path to output booklog data.',
                      default='list/booklog_data.csv')
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args


def main(options: argparse):
  logging.debug('download_booklist.py start')
  booklog_manager = BooklogManager(sleep_time=3)
  booklog_data = booklog_manager.download_csv_file()
  if os.path.exists(options.output_file):
    logging.info(f"remove {options.output_file}")
    os.remove(options.output_file)
  os.makedirs(os.path.dirname(options.output_file), exist_ok=True)
  print(booklog_data, file=codecs.open(options.output_file, 'w', 'utf-8'))
  logging.debug('download_booklist.py end')


if __name__ == "__main__":
  options = options()
  main(options=options)
