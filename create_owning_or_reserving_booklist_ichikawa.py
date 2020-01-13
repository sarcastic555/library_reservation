# /usr/local/bin/python
# -*- coding: utf-8 -*-
import tool_ichikawa
import pandas as pd

module = tool_ichikawa.IchikawaModule()
module.set_debug_mode(True)
module.set_sleep_time(3) ##sleep time [sec]
print("executing module.get_mypage_book_df('lend')")
df_lend=module.get_mypage_book_df('lend') ## 'lend' or 'reserve'
print("executing module.get_mypage_book_df('reserve')")
df_reserve=module.get_mypage_book_df('reserve') ## 'lend' or 'reserve'
df = pd.concat([df_lend,df_reserve])
df.to_csv('list/nowreading.csv')

