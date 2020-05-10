# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:42:27 2020

@author: Wenjie
"""

import threading
import time
import queue

exitFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.que = que
    
    def run(self):
        print("开始线程：" + self.name + "\n")  
        process_data(self.threadID, self.name, self.que)
        print("结束线程: " + self.name + "\n")
        
# 线程函数
def process_data(threadID, threadName, que):
    while not exitFlag:
        threadID += 1
        
        if threadID >= 4:
            data = que.get()
            print('%s processing %s\n' % (threadName, data))
        time.sleep(1)   
        
threadList = []
for ti in range(10):
    threadList.append("Thread-" + str(ti+1))
nameList = []
for ni in range(1000):
    nameList.append("Work-Item-" + str(ni+1))
workQueue = queue.Queue(1500)
threads = []
threadID = 1

# 填充队列
for word in nameList:
    workQueue.put(word)
# 创建线程
for tName in threadList:
    thread = MyThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
# 等待队列清空
while not workQueue.empty():
    pass
# 通知线程可以退出
exitFlag = 1
# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")