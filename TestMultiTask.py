#!/usr/bin/env python
# -*- encoding:utf-8 -*- 
from multiprocessing import Process
import sys
import time

def task(list, list_length, thread_num, i):
  for num in range(i - 1, list_length, thread_num):
    print("I'm %s" % i)
    print(list[num])

argvs = sys.argv
argc = len(argvs) - 1
if (argc <= 0):
  print('Usage: # python %s pthread_number 文字列' % argvs[0])
  quit()

thread_num = int(sys.argv[1])
list = list(sys.argv[2])
list_length = len(list)

#for num in range(0, list_length):
#  print(list[num])

processes = [Process(group=None, target=task, args=(list, list_length, thread_num, i))
             for i in range(1, thread_num + 1)]

for process in processes:
  process.start()
  print("process start!")

for process in processes:
  process.join()
