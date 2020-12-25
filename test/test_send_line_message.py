import os
import sys

import numpy as np

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from send_line_message import need_to_send_notification, send_line_notify


def test_send_line_notify() -> None:
  # テスト用に送信トークンを変更
  # 環境変数の書き換えはこの関数の中でのみ有効
  os.environ["LINE_TOKEN_PERSONAL"] = os.environ["LINE_TOKEN_FOR_TEST"]
  result = send_line_notify(notification_message='test')
  assert (result)


# 返却日までの残り日数が無効値（借りている書籍がない）の時は通知不要と判定する
def test_need_to_send_notification1() -> None:
  result = need_to_send_notification(remainday=np.nan)
  assert (not result)


# 残り日数が十分あるときは通知不要と判定
def test_need_to_send_notification2() -> None:
  result = need_to_send_notification(remainday=10)
  assert (not result)


# 残り日数が不十分なときは通知判定
def test_need_to_send_notification3() -> None:
  result = need_to_send_notification(remainday=1)
  assert (result)
