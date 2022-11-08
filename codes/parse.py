#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from datetime import datetime
import csv
import json

def log(*args, **kw):
  print(f"[{datetime.now().strftime('%FT%H:%M:%S%z')}]", *args, **kw)

file = open("gsrr.csv", "r", -1, "utf-8-sig")
reader = csv.reader(file)

header = next(reader)

try:
  with open("gsrr.json", "r", -1, "utf8") as file:
    data = json.load(file)
except Exception as e:
  data = {}

duplicated = {}
updated = []
added = []

while True:
  try:
    line = next(reader)
  except StopIteration:
    break
  line_dict = dict(zip(header, line))
  title = line_dict["產品名稱"]
  publisher = line_dict["業者名稱"]
  platform = line_dict["遊戲平台"]
  del line_dict["產品名稱"], line_dict["業者名稱"], line_dict["遊戲平台"]
  if title not in data:
    data[title] = {}
  if publisher not in data[title]:
    data[title][publisher] = {}
  if title not in duplicated:
    duplicated[title] = {}
  if publisher not in duplicated[title]:
    duplicated[title][publisher] = {}
  if platform in duplicated[title][publisher]:
    continue
  duplicated[title][publisher][platform] = True
  if platform in data[title][publisher]:
    if json.dumps(data[title][publisher][platform]) == json.dumps(line_dict):
      continue
    else:
      updated.append({
        "title": title,
        "publisher": publisher,
        "platform": platform,
        "old": data[title][publisher][platform],
        "new": line_dict
      })
      data[title][publisher][platform] = line_dict
  else:
    added.append({
      "title": title,
      "platform": platform,
      "new": line_dict
    })
    data[title][publisher][platform] = line_dict

file.close()

with open("gsrr.json", "w", -1, "utf8") as file:
  json.dump(data, file, ensure_ascii=False, separators=(",", ":"))

with open("updated.json", "w", -1, "utf8") as file:
  json.dump(updated, file, ensure_ascii=False, separators=(",", ":"))

with open("added.json", "w", -1, "utf8") as file:
  json.dump(added, file, ensure_ascii=False, separators=(",", ":"))
