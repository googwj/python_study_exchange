# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:31:20 2020

@author: Venbye
"""

import requests                 #Web请求
from bs4 import BeautifulSoup   #Html解析

url  = "https://npm.taobao.org/mirrors/python/"
resp = requests.get(url,timeout=30)
soup = BeautifulSoup(resp.text,"lxml")
data = soup.find('body').find_all('a')
for link in data:
    href = link['href']
    print(href)