import api.koto

import datetime
import argparse

def options() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=str, required=True, help='Library user ID')
    parser.add_argument('--user_password', type=str, required=True, help='Library user password')
    return parser.parse_args()

def main(user_id: str, user_password: str) -> None:
    library_api = api.koto.Koto(user_id=user_id, user_password=user_password)
    borrow_list = library_api.get_borrow_list()
    if len(borrow_list) == 0:
        return

    borrow_list["extension_available_flag"] = borrow_list.apply(lambda x: x["extension_available"]=="再貸出", axis=1)
    borrow_list["return_date_datetime"] = borrow_list.apply(lambda x: datetime.datetime.strptime(x["return_date"], "%Y/%m/%d"), axis=1)
    borrow_list["remaining_date"] = borrow_list.apply(lambda x: (x["return_date_datetime"] - datetime.datetime.now()).days, axis=1)
    borrow_list["extension_execution_flag"] = borrow_list.apply(lambda x: x["remaining_date"]==0 and x["extension_available_flag"], axis=1)
    print(f"{borrow_list=}")

    extension_execution_list = borrow_list[borrow_list["extension_execution_flag"]]
    extension_execution_list.apply(lambda x: library_api.push_extension_button(x["book_id"]), axis=1)

if __name__ == "__main__":
    options = options()
    main(options.user_id, options.user_password)
