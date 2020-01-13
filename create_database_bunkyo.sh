#!/bin/bash

mkdir -p list
mkdir -p log
today=`/bin/date +"%Y%m%d"`
. ~/.bashrc

### 1. download all book list in booklog
python download_booklist.py > log/download_booklist_log_${today}.txt 2>&1

### 2. create reading & booking book list
#/Users/nagakura/anaconda3/bin/python create_owning_or_reserving_booklist.py > log/create_owning_or_reserving_booklist_log_${today}.txt 2>&1

### 3. classfy 1. booklist to a:not found in library booklist, b:long waiting time c:short waiting time
#/Users/nagakura/anaconda3/bin/python classfy_list.py > log/classfy_list_log_${today}.txt 2>&1
