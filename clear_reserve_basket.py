# /usr/local/bin/python
# -*- coding: utf-8 -*-
import logging.config

from tools.tool_ichikawa import IchikawaModule

logging.config.fileConfig("log.conf")


### 予約カゴを空にする
def main():
  tool = IchikawaModule(sleep=3)
  result = tool.clear_reserve_basket()
  if result:  # 成功
    logging.info("Succeeded in clearing reservation basket")
  else:  # 失敗
    logging.info("Failed to clear reservation basket")


if __name__ == "__main__":
  main()
