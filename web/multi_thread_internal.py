# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:30:12 2020

@author: Wenjie
"""


import _thread
import time

# 线程函数
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print('%s: %s' % (threadName, time.ctime(time.time())))
        
# 创建线程
try:
    _thread.start_new_thread(print_time, ('Thread - 1', 2))
    _thread.start_new_thread(print_time, ('Thread - 2', 3))
except:
    print('Error: 无法启动线程')
    
# while 1:
#     pass