import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))

from create_owning_or_reserving_booklist import *

def test_get_waitnum_from_status1() -> None:
  waitnum = get_waitnum_from_status('利用可能')
  assert (waitnum == 0)

def test_get_waitnum_from_status2() -> None:
  waitnum = get_waitnum_from_status('準備中')
  assert (waitnum == 0)

def test_get_waitnum_from_status3() -> None:
  waitnum = get_waitnum_from_status('配送中')
  assert (waitnum == 0)

def test_get_waitnum_from_status4() -> None:
  waitnum = get_waitnum_from_status('順番待ち (37位)')
  assert (waitnum == 37)

def test_get_waitnum_from_status5() -> None:
  waitnum = get_waitnum_from_status('順番待ち (7位)')
  assert (waitnum == 7)

def test_get_waitnum_from_status6() -> None:
  waitnum = get_waitnum_from_status('確認待ち (1位)')
  assert (waitnum == 1)

def test_get_waitnum_from_status7() -> None:
  waitnum = get_waitnum_from_status('返却待ち (14位)')
  assert (waitnum == 14)


