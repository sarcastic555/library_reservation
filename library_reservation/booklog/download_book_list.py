import datetime
import re
import time

import bs4
import requests

def download_book_list(booklog_id: str, booklog_password: str):
      pass
      # session, session_id = _login(booklog_id, booklog_password)
      # download_csv_file(session)
      # logout(session, session_id)

def _login(book_id: str, book_password: str):
    session = requests.session()
    ## create session ID
    ## php_session_idは同じものを複数使うと（かつそのセッションをクローズしないと？未確認）
    ## 2回目以降ログインできなくなるため現在時刻を代入し重複が発生しないようにする
    now = datetime.datetime.now()
    session_id = str(int(now.timestamp()))
    login_url = "https://booklog.jp/login"

    login_header = {
        "cookie": f"PHPSESSID={session_id}",
        "referer": login_url,
    }
    login_data = {
        "service": "booklog",
        "ref": "",
        "account": book_id,
        "password": book_password,
    }
    r1 = session.get(login_url)
    print(f"{r1.text=}")
    time.sleep(3)
    r2 = session.post(login_url, headers=login_header, data=login_data, allow_redirects=True)
    print(f"{r2.text=}")
    return session, session_id


def _get_signature(session) -> str:
    time.sleep(3)
    export_url = "https://booklog.jp/export"
    r = session.get(export_url)
    print(f"{r.text=}")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    button = soup.find(class_="buttons")
    print(f"{button=}")
    ## signatureを返す(ボタンにリンクとして埋め込まれている)
    signature = re.search(".*signature=(.*)", button.find("a")["href"])[1]
    return signature

def download_csv_file(session) -> str:
    signature = _get_signature(session)
    download_url = f"https://download.booklog.jp/shelf/csv?signature={signature}"
    ## csvデータとして取得
    time.sleep(3)
    r = session.get(download_url)
    r.encoding = "Shift_JIS"  ## これがないと文字化けする
    return r.text

def logout(session, session_id) -> None:
    logout_url = "https://booklog.jp/logout"
    ## ログアウト
    time.sleep(3)
    r = session.get(logout_url,
                        headers={"cookie": "PHPSESSID=" + session_id})
    r.close()

download_book_list("ngkqnok", "BookLog555")


import requests
import json

api_res=requests.get("http://api.booklog.jp/v2/json/4165b902f43abd44?count=10000")
json_res=json.loads(api_res.text)

print(json_res)