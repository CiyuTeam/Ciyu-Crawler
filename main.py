#非定时，用于测试爬虫

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #得到Chinadaily文件夹的路径
execute(["scrapy","crawl","ChinaDaily1"])

"""
import time
import datetime
from scrapy import cmdline
def doSth():
  # 把爬虫程序放在这个类里 zhilian_spider 是爬虫的name
  cmdline.execute('scrapy crawl ChinaDaily1'.split())
# 想几点更新,定时到几点
def time_ti(h=10, m=00):
  while True:
    now = datetime.datetime.now()
    print(now.hour, now.minute)
    if now.hour == h and now.minute == m:
      print(now.hour, now.minute)
      doSth()
    # 每隔60秒检测一次
    time.sleep(10)

time_ti()
"""
