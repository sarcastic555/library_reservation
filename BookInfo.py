import datetime


class BookInfo:
  book_id = ""
  title = ""
  isbn = ""
  status = ""
  can_rental_extension = False
  return_datetime_before_extension = datetime.date(2001, 1, 1)
  return_datetime_after_extension = datetime.date(2001, 1, 1)
  reserve_status = ""
