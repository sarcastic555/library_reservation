import argparse
from logic import notify_return_date_approach, push_extension_button

def options() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=str, required=True, help='Library user ID')
    parser.add_argument('--user_password', type=str, required=True, help='Library user password')
    parser.add_argument('--line_token', type=str, required=True, help='LINE token to post message')
    parser.add_argument('--line_group_id', type=str, required=True, help='LINE group ID to post message')
    return parser.parse_args()

def main(user_id: str, user_password: str, line_token: str, line_group_id: str) -> None:
    push_extension_button.main(user_id, user_password)
    notify_return_date_approach.main(user_id, user_password, line_token, line_group_id)

if __name__ == "__main__":
    options = options()
    main(options.user_id, options.user_password, options.line_token, options.line_group_id)
