import os
import sys
from unittest import mock

import pandas as pd

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from send_line_message import *


def test_send_line_notify() -> None:
  # テスト用に送信トークンを変更
  # 環境変数の書き換えはこの関数の中でのみ有効
  os.environ["LINE_TOKEN_PERSONAL"] = os.environ["LINE_TOKEN_FOR_TEST"]
  result = send_line_notify(notification_message='test')
  assert (result)


# 借りている本が存在しない時は通知不要と判定する
def test_need_to_send_notification1() -> None:
  df = pd.DataFrame()
  result = need_to_send_notification(df=df)
  assert (not result)


# 借りている本が存在し残り日数が十分あるときは通知不要と判定
def test_need_to_send_notification2() -> None:
  df = pd.DataFrame({'remainday': [10, 12]})
  result = need_to_send_notification(df=df)
  assert (not result)


# 借りている本が存在し1冊でも残り日数が不十分なときは通知判定
def test_need_to_send_notification3() -> None:
  df = pd.DataFrame({'remainday': [1, 12]})
  result = need_to_send_notification(df=df)
  assert (result)


# 借りている本が存在し全ての本の残り日数が不十分なときも通知判定
def test_need_to_send_notification4() -> None:
  df = pd.DataFrame({'remainday': [1, 0]})
  result = need_to_send_notification(df=df)
  assert (result)
