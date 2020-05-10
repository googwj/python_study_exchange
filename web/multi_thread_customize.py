# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:42:27 2020

@author: Wenjie
"""

import threading
import time

exitFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
    
    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.delay, 5)
        print("结束线程: " + self.name)
        
# 线程函数
def print_time(threadName, delay, count):
    while count:
        if exitFlag:
            threadName.exit()
            
        time.sleep(delay)
        print('%s: %s' % (threadName, time.ctime(time.time())))
        count -= 1
        
# 创建新线程
thread1 = MyThread(1, 'Thread - 1', 1)
thread2 = MyThread(2, 'Thread - 2', 2)

# 开启线程
print('主线程开启')
thread1.start()
thread2.start()
print('=======================begin=====================')
thread1.join()
thread2.join()
print('退出主线程')