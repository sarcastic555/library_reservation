# /usr/local/bin/python
# -*- coding: utf-8 -*-
import argparse
import logging
import os

import numpy as np
import pandas as pd
import requests

line_api_url = 'https://notify-api.line.me/api/notify'
notify_day_threshold = 4  # days


def options():
  parser = argparse.ArgumentParser()
  parser.add_argument('--lend_file', help='Path to lend book list.', default='list/lend.csv')
  args = parser.parse_args()
  logging.debug(f'options={args}')
  return args


def send_line_notify(notification_message) -> bool:
  line_notify_token = os.environ["LINE_TOKEN_PERSONAL"]
  print("line_notify_token=", line_notify_token)
  line_notify_api = line_api_url
  headers = {'Authorization': f'Bearer {line_notify_token}'}
  data = {'message': f'message: {notification_message}'}
  r = requests.post(line_notify_api, headers=headers, data=data)
  return r.ok


# 最も返却日が近い書籍の返却日までの日数を返す
def get_minimun_remain_day(df: pd.DataFrame) -> int:
  return df['remainday'].min() if len(df) > 0 else np.nan


# 返却日が迫っていて延長不可能な本が存在する場合は通知
def need_to_send_notification(remainday: int) -> bool:
  if np.isnan(remainday):
    return False
  return (remainday < notify_day_threshold)


def main(options: argparse):
  df = pd.read_csv(options.lend_file)
  remainday = get_minimun_remain_day(df)
  if need_to_send_notification(remainday):
    send_line_notify(f"市川図書館返却日まであと{remainday}日")


if __name__ == "__main__":
  options = options()
  main(options=options)
