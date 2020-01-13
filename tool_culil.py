# /usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import json
import sys

class CulilModule():
    def __init__(self):
        self.app_key='0969d68ad9bcd0e5c3f5119a7342933b'
        self.URL_culil='http://api.calil.jp/check'
        self.systemid='Chiba_Ichikawa'
        self.format='json'
        self.sleeptime=3 ## [sec]
        
    def set_sleep_time(self,sleeptime):
        self.sleeptime=sleeptime ## [sec]

    def check_existence_in_library(self,ISBN): ## ISBN[str]
        time.sleep(self.sleeptime)
        param={'appkey':self.app_key,
               'isbn':ISBN,
               'systemid':self.systemid,
               'format':self.format
        }
        continue_flag=1

        try:
            while(continue_flag==1): ### continueフラグが1の場合はget操作を繰り返す
                r = requests.get(self.URL_culil, params=param)
                time.sleep(self.sleeptime)
                try:
                    json_data = json.loads(r.text[9:-2]) ## jsonデータがcallback()で囲まれてしまっているので、[9:-2]でcallbackを削除する
                except:
                    print("Error occured at check_existence_in_library in tool_culil.py !")
                    print("ISBN=%s !"%ISBN)
                    print(r.text)
                    sys.exit()
                continue_flag=int(json_data['continue'])
                #print(continue_flag)

            existlist=json_data['books'][ISBN][self.systemid]['libkey']
            existlibnum=len(existlist)
            renting_possible_flag=False ## 本が蔵書しているかを表すフラグ
            renting_soon_flag=False     ## 本がすぐに予約可能かを表すフラグ
            for ilib in existlist:
                if (existlist[ilib]=='蔵書なし' or existlist[ilib]=='休館中' or
                    existlist[ilib]=='準備中' or existlist[ilib]=='館内のみ' or
                    existlist[ilib]=='蔵書あり'):
                    continue
                elif (existlist[ilib]=='貸出中' or existlist[ilib]=='予約中'):
                    renting_possible_flag=True
                elif (existlist[ilib]=='貸出可'):
                    renting_possible_flag=True
                    renting_soon_flag=True
                else:
                    print("Error. API return status error.")

        except: ## エラーが出た場合はその旨をprintして処理を続ける
            print("Error occured at seraching book ID = %s"%ISBN)
            renting_possible_flag = False
            renting_soon_flag = False
        #print("renting_possible_flag=%d"%renting_possible_flag)
        #print("renting_soon_flag=%d"%renting_soon_flag)
        return renting_possible_flag, renting_soon_flag
