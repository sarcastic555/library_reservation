# /usr/local/bin/python
# -*- coding: utf-8 -*-
import os

import pandas as pd
import requests

line_api_url = 'https://notify-api.line.me/api/notify'
notify_day_threshold = 3  # days


def send_line_notify(notification_message):
  line_notify_token = os.environ["LINE_TOKEN_PERSONAL"]
  line_notify_api = line_api_url
  headers = {'Authorization': f'Bearer {line_notify_token}'}
  data = {'message': f'message: {notification_message}'}
  requests.post(line_notify_api, headers=headers, data=data)


def main():
  # dateframeの読み込み
  df = pd.read_csv('list/nowreading.csv')
  df = df[df["status"] == "lend"]  # 借用中書籍のみ抽出

  # 返却日が迫っていて延長不可能な本が存在する場合は通知
  notify_flag = False
  remainday_min = df['remainday'].min()
  if (remainday_min < notify_day_threshold):
    notify_flag = True
  if (notify_flag):
    send_line_notify(f"市川図書館返却日まであと{remainday_min}日")


if __name__ == "__main__":
  main()
