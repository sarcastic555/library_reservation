#!/bin/bash

mkdir -p log list
today=`/bin/date +"%Y%m%d"`
rm -v log/monthly_${today}.txt

## ブクログから読みたい本リストをダウンロード
echo "======= 1. python download_booklist.py ============"  >> log/monthly_${today}.txt 2>&1
date  >> log/monthly_${today}.txt 2>&1
python download_booklist.py >> log/monthly_${today}.txt 2>&1
date >> log/monthly_${today}.txt 2>&1

## 上記リストに対して、市川市立図書館に蔵書があるか長期待ちかどうかで分類
echo "======= 2. python classfy_list_ichikawa.py ============"  >> log/monthly_${today}.txt 2>&1
date >> log/monthly_${today}.txt 2>&1
python classfy_list_ichikawa.py >> log/monthly_${today}.txt 2>&1
date >> log/monthly_${today}.txt 2>&1
