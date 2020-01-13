# /usr/local/bin/python
# -*- coding: utf-8 -*-
import tool_ichikawa

### 延長条件を満たす時は延長ボタンを押す
module = tool_ichikawa.IchikawaModule()
module.set_sleep_time(3) ##[sec]
module.set_debug_mode(True)
module.extend_reservation_day_if_satisfied_condition()
