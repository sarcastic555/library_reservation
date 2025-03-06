import api.koto
import line.send

import datetime
import argparse

def options() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=str, required=True, help='Library user ID')
    parser.add_argument('--user_password', type=str, required=True, help='Library user password')
    parser.add_argument('--line_token', type=str, required=True, help='LINE token to post message')
    parser.add_argument('--line_group_id', type=str, required=True, help='LINE group ID to post message')
    return parser.parse_args()

def main(user_id: str, user_password: str, line_token: str, line_group_id: str) -> None:
    library_api = api.koto.Koto(user_id=user_id, user_password=user_password)
    borrow_list = library_api.get_borrow_list()
    if len(borrow_list) == 0:
        return

    not_extention_list = borrow_list[borrow_list["extension_available"] != "再貸出"]
    if len(not_extention_list) == 0:
        return

    not_extention_list["return_date_datetime"] = not_extention_list.apply(lambda x: datetime.datetime.strptime(x["return_date"], "%Y/%m/%d"), axis=1)
    now = datetime.datetime.now()
    not_extention_list["remaining_date"] = not_extention_list.apply(lambda x: (x["return_date_datetime"] - now).days, axis=1)
    print(f"{not_extention_list=}")

    remaining_date_min = int(not_extention_list["remaining_date"].min())
    print(f"{remaining_date_min=}")
    if remaining_date_min < 12:
        print("Send LINE")
        message = f"返却日まであと{remaining_date_min}日"
        line.send.send_line_message(message=message, token=line_token, group_id=line_group_id)

if __name__ == "__main__":
    options = options()
    main(options.user_id, options.user_password, options.line_token, options.line_group_id)
