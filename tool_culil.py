# /usr/local/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import warnings

import requests


class CulilModule():

  def __init__(self, sleep=3):
    self.app_key = os.environ["CULIL_API_KEY"]
    self.app_key = '0969d68ad9bcd0e5c3f5119a7342933b'
    self.URL_culil = 'http://api.calil.jp/check'
    self.systemid = 'Chiba_Ichikawa'
    self.format = 'json'
    self.sleeptime = sleep  ## [sec]

  def check_existence_in_library(self, ISBN):  ## ISBN[str]
    if type(ISBN) is not str:
      raise TypeError("type of ISBN is %s, but str is expected" % type(ISBN))
    time.sleep(self.sleeptime)
    param = {'appkey': self.app_key, 'isbn': ISBN, 'systemid': self.systemid, 'format': self.format}
    continue_flag = 1

    try:
      while (continue_flag == 1):  ### continueフラグが1の場合はget操作を繰り返す
        r = requests.get(self.URL_culil, params=param)
        time.sleep(self.sleeptime)
        try:
          json_data = json.loads(
              r.text[9:-2])  ## jsonデータがcallback()で囲まれてしまっているので、[9:-2]でcallbackを削除する
        except:
          warnings.warn(f"Cannot get book (ISBN = {ISBN}) information. Skip the process.")
        continue_flag = int(json_data['continue'])

      existlist = json_data['books'][ISBN][self.systemid]['libkey']
      existlibnum = len(existlist)
      renting_possible_flag = False  ## 本が蔵書しているかを表すフラグ
      renting_soon_flag = False  ## 本がすぐに予約可能かを表すフラグ
      for ilib in existlist:
        if (existlist[ilib] == '蔵書なし' or existlist[ilib] == '休館中' or existlist[ilib] == '準備中' or
            existlist[ilib] == '館内のみ' or existlist[ilib] == '蔵書あり'):
          continue
        elif (existlist[ilib] == '貸出中' or existlist[ilib] == '予約中'):
          renting_possible_flag = True
        elif (existlist[ilib] == '貸出可'):
          renting_possible_flag = True
          renting_soon_flag = True
        else:
          print("Error. API return status error.")

    except:  ## エラーが出た場合はその旨をprintして処理を続ける
      warnings.warn(f"Cannot get book (ISBN = {ISBN}) information. Skip the process.")
      renting_possible_flag = False
      renting_soon_flag = False
    return renting_possible_flag, renting_soon_flag
