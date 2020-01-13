#!/bin/bash

today=`date +"%Y%m%d"`;
mkdir -p log

### 1. create reading & booking list
#python create_owning_or_reserving_booklist.py

### 2. reserve book list
python reserve_book_ichikawa.py > log/reservelog_${today}.txt 2>&1
