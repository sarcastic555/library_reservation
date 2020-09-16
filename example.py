# /usr/local/bin/python
# -*- coding: utf-8 -*-

import json
import urllib.error
#import urllib2  ## for python2
import urllib.request  # # for pythoh3

booklogID = "ngkqnok"
url = 'http://api.booklog.jp/json/%s' % booklogID
#data = json.load(urllib2.urlopen(url)) ## for python2
data = json.load(urllib.request.urlopen(url))  ## for python3
tana = data["tana"]
books = data['books']

print(tana["account"])
print(tana["image_url"])
print(tana["id"])
print(tana["name"])

for book in books:
  print(book['title'])
  print(book['asin'])
  print(book['author'])
  print(book['url'])
  print(book['image'])
  print(book['title'])
  print(book['height'])
  print(book['width'])
  print(book['catalog'])
  print(book['id'])
