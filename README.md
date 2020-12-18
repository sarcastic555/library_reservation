# library_reservation

0. 準備
```bash
git clone https://github.com/sarcastic555/library_reservation.git
cd docker
source docker_build.sh
source docker_run.sh
```

1. ブックリストのダウンロード
```bash
python ./download_booklist.py
```

2. 1.でダウンロードしたブックリストを既読・未読即時利用可能・未読即時利用不可に分類
```bash
python ./classfy_list.py
```

3. 貸し出し延長が必要か判定し必要なら延長手続きを実施
```bash
python extension_checker.py
```

4. 借りている本、予約している本のリストを作成
```bash
python ./create_owning_or_reserving_booklist.py
```

5. 返却期限が迫っていればLINEで通知
```bash
python ./send_line_message.py
```

6. 予約バスケットをクリア
```bash
python ./clear_reserve_basket.py
```

7. 読みたい本リストの中から資料を予約
```
python ./reserve_book.py
```
