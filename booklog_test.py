# /usr/local/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import sys
import os 
import json
import platform
import pandas as pd
import re

### booklog setting
booklogID = "ngkqnok"
url = 'http://api.booklog.jp/json/%s' % booklogID
params={'count':'50', 'status':'1'}

### my library page
ID='1036505'
PASSWORD='zk2ec6'

## count
## いくつのアイテムを取得するか(default:5)
#####
## status. 1:読みたい, 2:いま読んでる, 3:読み終わった
## see http://unformedbuilding.com/articles/booklog-blogparts-api/ for more detail
## see http://maky.dip.jp/blog/?p=78
print ('URL=%s' % url)
python_version=int(platform.python_version_tuple()[0])
if (python_version == 2):
    import urllib2  ## for python2
    url += "?{0}".format( urllib.urlencode( param ) )
    data = json.load(urllib2.urlopen(url)) ## for python2
elif (python_version == 3):
    import urllib
    from urllib import parse, request ## for pythoh3
    #import urllib.request, urllib.error ## for pythoh3
    url += "?{0}".format( urllib.parse.urlencode( params ) )
    data = json.load(urllib.request.urlopen(url)) ## for python3
else:
    print ('Erroer. python version (%d) is invalid' % python_version)

books = data['books']
### タイトルはbooks['title'], 著者はbooks['author']で得られる
