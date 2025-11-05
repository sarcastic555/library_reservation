import requests
import time
import os
from enum import Enum

class BookStatus(Enum):
    borrow_available = "貸出可"
    borrow_unavailable = "貸出不可"

def get_book_status(isbn: str, systemid: str) -> dict:
    """
    Fetch the book status from the Calil API.

    :param isbn: 13-digit ISBN of the book
    :param systemid: Library system ID
    :return: Dictionary with library status
    """
    appkey = os.environ.get("CULIL_API_KEY")
    if not appkey:
        raise EnvironmentError("CULIL_API_KEY environment variable is not set.")

    url = "https://api.calil.jp/check"
    params = {
        "appkey": appkey,
        "isbn": isbn,
        "systemid": systemid,
        "format": "json",
        "callback": "no",
    }

    for _ in range(5):
      time.sleep(3)  # Add a delay before making the request
      response = requests.get(url, params=params)
      data = response.json()
      book_data = data["books"][isbn][systemid]
      if book_data["status"] == "OK" or book_data["status"] == "Cache":
        if "libkey" not in book_data:
            print("L36 not found")
            return {}

        status_dict = {}
        for library, status in book_data["libkey"].items():
            if status == "貸出可":
                status_dict[library] = BookStatus.borrow_available
            else:
                status_dict[library] = BookStatus.borrow_unavailable

        return status_dict
    print(f"L45 not found: {book_data=}")
    return {}