# /usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import sys
sys.path.append('../utility')
import mailsend ## utility/mailsend モジュールを使用

### dateframeの読み込み
df = pd.read_csv('list/nowreading.csv')
print(df)

### 返却日が迫っている & 延長不可能　の場合はメール送信
mailsend_flag=False
remainday_min = df['remainday'].min()
print("remainday_min=%d"%remainday_min)
if (remainday_min<3):
    mailsend_flag=True
if (mailsend_flag): mailsend.send_mail(filepath='list/nowreading.csv',title='返却日まであと%d日!'%remainday_min)
