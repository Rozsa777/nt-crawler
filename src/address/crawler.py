#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import time
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from operator import itemgetter

# NAVITIME 住所検索TOP
def crawl():
  init()
  prefectures()

def init():
  if not os.path.exists('data'):
    os.mkdir('data')


def prefectures():
  print(f"prefectures start : {now()}")
  TOP_URL = 'https://www.navitime.co.jp/?ctl=0050'
  response = requests.get(TOP_URL)
  soup = BeautifulSoup(response.text, 'lxml')
  sub_urls = []
  prefectures = []
  for li in soup.find_all("li", attrs={"class": "pref-item"}):
    target = li.find("a", reversed=False)
    url = target.get("href")
    sub_urls.append(url)
    data = itemgetter(4, 5)(url.split("/"))
    prefectures.append(data)

  df = pd.DataFrame(prefectures, columns=['code', 'name'])
  df.to_csv("data/prefectures.csv", index=False)
  print(f"prefectures end : {now()}")

  # cities(sub_urls)

def cities(urls: list):
  print(f"cities start : {now()}")
  sub_urls = []
  cities = []
  for url in urls:
    prefecture_code =  url.split("/")[4]
    print(f"----- prefecture_code={prefecture_code} start : {now()} -----")
    # if not prefecture_code == '13':
    #   continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for div in soup.find_all("div", attrs={"class": "address_list"}):
      for li in div.find_all("li", attrs={"class": "left"}):
        ruby = li.find("span").getText()
        url = 'https://www.navitime.co.jp' + li.find("a").get("href")
        name = li.find("a").getText()
        sub_urls.append(url)
        code = url.split("/")[4]
        data = (code, name, ruby, prefecture_code)
        cities.append(data)

    time.sleep(1)

  df = pd.DataFrame(cities, columns=['code', 'name', 'ruby', 'prefecture_code'])
  df.to_csv("data/cities.csv", index=False)
  print(f"cities end : {now()}")

  towns(sub_urls)

def towns(urls: list):
  print(f"towns start : {now()}")
  sub_urls = []
  towns = []
  for url in urls:
    city_code =  url.split("/")[4]
    print(f"----- city_code={city_code} start : {now()} -----")
    # if not city_code == '13113':
    #   continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for div in soup.find_all("div", attrs={"class": "address_list"}):
      for li in div.find_all("li", attrs={"class": "left"}):
        ruby = li.find("span").getText()
        url = 'https://www.navitime.co.jp' + li.find("a").get("href")
        name = li.find("a").getText()
        sub_urls.append(url)
        code = url.split("/")[4]
        data = (code, name, ruby, city_code)
        towns.append(data)

    time.sleep(1)

  df = pd.DataFrame(towns, columns=['code', 'name', 'ruby', 'city_code'])
  df.to_csv("data/towns.csv", index=False)
  print(f"towns end : {now()}")

def now():
  return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

if __name__ == "__main__":
  crawl()
