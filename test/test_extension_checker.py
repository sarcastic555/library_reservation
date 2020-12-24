import datetime
import os
import sys

from freezegun import freeze_time
from mock import Mock

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../"))
from extension_checker import *


# 処理可能時刻
@freeze_time("2020-01-01 15:00:00")
def test_time_ok() -> None:
  available = is_extension_available(margin=300)
  assert (available)


# 処理不可時刻
@freeze_time("2020-01-01 5:00:00")
def test_time_ng() -> None:
  available = is_extension_available(margin=300)
  assert (not available)


# 返却期限が先であり、かつその資料が延長不可の場合 -> 延長申請はしない
@freeze_time("2020-01-15")
def test_rental_extension1() -> None:
  return_date = datetime.date(2020, 1, 25)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=False)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (not extend)


# 返却期限が先であり、かつその資料が延長可能な場合 -> 延長申請はしない
@freeze_time("2020-01-15")
def test_rental_extension2() -> None:
  return_date = datetime.date(2020, 1, 25)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=True)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (not extend)


# 返却期限当日であり、かつその資料が延長不可の場合 -> 延長申請はしない
@freeze_time("2020-01-15")
def test_rental_extension3() -> None:
  return_date = datetime.date(2020, 1, 15)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=False)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (not extend)


# 返却期限が当日であり、かつその資料が延長可能な場合 -> 延長申請する
@freeze_time("2020-01-15")
def test_rental_extension4() -> None:
  return_date = datetime.date(2020, 1, 15)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=True)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (extend)


# 返却期限が先であり、かつその資料が延長不可な場合 -> 延長申請しない
@freeze_time("2020-01-15")
def test_rental_extension5() -> None:
  return_date = datetime.date(2020, 1, 5)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=False)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (not extend)


# 返却期限が先であり、かつその資料が延長可能な場合 -> 延長申請しない
@freeze_time("2020-01-15")
def test_rental_extension6() -> None:
  return_date = datetime.date(2020, 1, 5)
  tool = Mock()
  tool.get_return_date_datetime_per_book = Mock(return_value=return_date)
  tool.get_extension_status_per_book = Mock(return_value=True)
  extend = is_rental_extension_target(tool=tool, bookid=1)
  assert (not extend)
