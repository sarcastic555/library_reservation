#!/bin/bash

mkdir -p log
today=`/bin/date +"%Y%m%d"`
if [ -f log/daily_${today}.txt ]; then
    rm -v log/daily_${today}.txt
fi

### 貸出延長ボタンを押す必要がある本に対しては押す
### 朝８時から０時までしか受け付けていないので注意！
echo "======= 1. python extension_checker.py ============" >> log/daily_${today}.txt 2>&1
python extension_checker.py >> log/daily_${today}.txt 2>&1

### 現在貸出中/予約中の本のリストを作成
echo "======= 2. python create_owning_or_reserving_booklist.py ============" >> log/daily_${today}.txt 2>&1
python create_owning_or_reserving_booklist.py >> log/daily_${today}.txt 2>&1

### メールを送信する必要がある場合はメール送信
echo "======= 3. python mailsend_checker.py ============" >> log/daily_${today}.txt 2>&1
python mailsend_checker.py >> log/daily_${today}.txt 2>&1

### 予約かごを空にする
echo "======= 4. python clear_reserve_basket.py ============" >> log/daily_${today}.txt 2>&1
python clear_reserve_basket.py >> log/daily_${today}.txt 2>&1

### 条件を満たした場合は本の予約を実行
echo "======= 5. python reserve_book.py ============" >> log/daily_${today}.txt 2>&1
python reserve_book.py >> log/daily_${today}.txt 2>&1
