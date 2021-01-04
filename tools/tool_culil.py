# /usr/local/bin/python
# -*- coding: utf-8 -*-
import json
import logging
import os
import time
from typing import Tuple

import requests
from retry import retry


class CulilException(Exception):
  pass


class CulilModule():

  def __init__(self, sleep=3):
    self.app_key = os.environ["CULIL_API_KEY"]
    self.URL_culil = 'http://api.calil.jp/check'
    self.systemid = 'Chiba_Ichikawa'
    self.format = 'json'
    self.sleeptime = sleep  ## [sec]
    self.param = {'appkey': self.app_key, 'systemid': self.systemid, 'format': self.format}

  @retry(CulilException, tries=5, delay=4)
  def get_book_status_info_retry(self, ISBN: str) -> dict:
    if type(ISBN) is not str:
      raise TypeError("type of ISBN is %s, but str is expected" % type(ISBN))
    self.param['isbn'] = ISBN
    time.sleep(self.sleeptime)
    r = requests.get(self.URL_culil, params=self.param)
    json_data = json.loads(r.text[9:-2])  ## jsonデータがcallback()で囲まれてしまっているので、[9:-2]でcallbackを削除する
    continue_flag = int(json_data['continue'])
    status = json_data['books'][ISBN][self.systemid]['status']
    # continueフラグが1 or statusがRunningの場合はAPIがまだ全ての取得が完了していないことを表すので再トライする
    if continue_flag == 1 or status == 'Running':
      raise CulilException
    # 稀にstatusとしてErrorが返ってくることがある。
    if status == 'Error':
      raise CulilException
    if 'libkey' not in json_data['books'][ISBN][self.systemid]:  # 図書館蔵書情報を表すキーが存在しない
      raise CulilException
    return json_data['books'][ISBN][self.systemid]['libkey']

  def get_book_status_info(self, ISBN: str) -> dict:
    try:
      info = self.get_book_status_info_retry(ISBN=ISBN)
    except CulilException:
      logging.warning(f'Cannot get book info (ISBN={ISBN}) through culil API!')
      info = {}
    return info

  def check_existence_in_library(self, ISBN: str) -> Tuple[bool, bool]:
    book_status_dict = self.get_book_status_info(ISBN=ISBN)
    renting_possible_flag = False  ## 本が蔵書しているかを表すフラグ
    renting_soon_flag = False  ## 本がすぐに予約可能かを表すフラグ
    for status in book_status_dict.values():
      if status in {'蔵書なし', '休館中', '準備中', '館内のみ', '蔵書あり'}:
        continue
      elif status in {'貸出中', '予約中'}:
        renting_possible_flag = True
      elif status == '貸出可':
        renting_possible_flag = True
        renting_soon_flag = True
      else:
        logging.error("Error. API return status error.")
    return renting_possible_flag, renting_soon_flag
