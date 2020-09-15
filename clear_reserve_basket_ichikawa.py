# /usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import sys
import tool_ichikawa

### 予約かごを空にする
reserver = tool_ichikawa.IchikawaModule()
reserver.set_debug_mode(True)
reserver.set_sleep_time(3)
print("clear reserve basket start")
reserver.clean_reserve_busket()
print("clear reserve basket end")
