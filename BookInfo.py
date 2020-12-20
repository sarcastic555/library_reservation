import datetime


class BookInfo:
  book_id = ""
  title = ""
  isbn = ""

class RentalBookInfo(BookInfo):
  can_rental_extension = False
  return_datetime_before_extension = datetime.date(2001, 1, 1)
  return_datetime_after_extension = datetime.date(2001, 1, 1)

class ReserveBookInfo(BookInfo):
  reserve_status = ""
  waitnum = 0
