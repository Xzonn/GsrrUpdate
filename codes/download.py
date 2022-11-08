#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from datetime import datetime
import time

import requests

def log(*args, **kw):
  print(f"[{datetime.now().strftime('%FT%H:%M:%S%z')}]", *args, **kw)

url = "https://www.gamerating.org.tw/Files/%E9%81%8A%E6%88%B2%E8%BB%9F%E9%AB%94%E5%88%86%E7%B4%9A%E8%B3%87%E6%96%99%E4%B8%8B%E8%BC%89.csv"

tries = 10
while tries > 0:
  tries -= 1
  try:
    response = requests.get(url, timeout=10)
    if response.status_code < 400:
      with open("gsrr.csv", "wb") as file:
        file.write(response.content)
      log("Downloaded and saved successfully.")
      break
    log(f"Failed to download, server responses with {response.status_code}. Retry.")
  except Exception as e:
    log(f"Got an error wile downloading: {e}. Retry.")
  finally:
    time.sleep(5)