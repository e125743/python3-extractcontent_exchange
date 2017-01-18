#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import extractcontent
import urllib.request
import codecs
import re
import sys
import math
import time
#from cython.parallel cimport parallel
#cimport openmp
#from multiprocessing import Process, Pipe
#import unicodedata
#from functools import reduce
import analysis
import multiTask

'''
def lines_task(lines, keyword):
  print(len(lines))
  for line in lines:
    if keyword in line:
      print("\n本文:")
      print("%s\n" % line)
      leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes, tree, print_format = analysiser.ReceivedObj(line, keyword)
      print(tree)
      print(print_format)
      #print("leadID:%s" % leadID)
      #print("keywordID:%s" % keywordID)
      #print("%s" % chunkdic)
      upSentencedic = analysiser.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)
      if len(upSentencedic) > 0:
        for upSentence in upSentencedic:
          print(upSentence)
'''

def conv_encoding(data):
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
            'shift_jis', 'shift_jis_2004','shift_jisx0213',
            'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
            'iso2022_jp_ext','latin_1', 'ascii')
    #encode = None

    for encoding in lookup:
      try:
        data = data.decode(encoding)
        #encode = encoding
        break
      except:
        pass

    if isinstance(data, str):
        return data#,encode
    else:
        raise LookupError


extractor = extractcontent.ExtractContent()

opt = {"threshold":1, "continuous_factor": 1.00, "punctuation_weight": 20}#, "debug": True}
extractor.set_default(opt)

argvs = sys.argv
argc = len(argvs)
UrlNum = argc - 1

if (UrlNum <= 0):
  print('Usage: # python %s pthread_number URL1 URL2 ... URLn' % argvs[0])
  quit()

'''
sys.stdout.write("Please input number of Keyword:")
keyword_num = int(input())
keyword = [None for i in range(keyword_num)]

for i in range(keyword_num):
  sys.stdout.write("Please input a Keyword:")
  keyword[i] = input()
'''
keyword = [ 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s']
keyword_num = len(keyword)

start = time.time()
lines_thread_num = int(sys.argv[1])
analysiser = analysis.AnalysisContent()
lines = []
for num in range(2, UrlNum + 1):
  response = urllib.request.urlopen(argvs[num])
  html = response.read()
  
  f = codecs.open("index.txt", "w", "utf-8")
  
  data = conv_encoding(html)
  
  f.write(data)
  f.close()
  
  file = open("index.txt", "r").read()
  
  #print("%s" % file.encode())
  #byfile = str(file.encode('utf-8'))
  #print("%s" % type(file))
  
  #print("%s" % encoding)
  #print("%s" % (str(html)))
  #print("htnltype:%s" % type(html.decode(encoding)))
  #print("%s" % data)
  #extractor.analyse(data, encoding)
  
  analyse = extractor.analyse(file)#, encoding)
  print("\n\n\nURL:" + argvs[num] + "\n\n")
  print("analysehtml:%s" % analyse)
  #f = codecs.open("decode_utf.txt", "w", "utf-8")
  
  text, title = extractor.as_text()
  #f.write(text)
  #f.write(title)
  #print("texttype:%s" % type(text))
  print("title:%s\n\ntext:" % (title))
  
  text = text.splitlines()
  for line in text:
    lines.extend(line.split("。"))
  while (True):
    try:
      lines.remove("")
    except:
      break

'''
for num in range(0, len(lines)):
  if keyword in lines[num]:
    print("%s:" % num + "%s" % lines[num])
'''

all = 0
if keyword_num > 0:
  upSentencedic = multiTask.multiTask(lines, keyword, int(sys.argv[1]))
  #upSentencedic = multiTask.multiPrange(lines, keyword, int(sys.argv[1]))
  #print(upSentencedic)

'''
  for i in range(keyword_num):
    for num in range(len(lines)):
      if keyword[i] in lines[num]:
        print("\n%s:" % num + "%s:\n%s" % (keyword[i], lines[num]))
        print(upSentencedic[num][keyword[i]])
        all += 1
else:
  for num in range(len(lines)):
    print("\n%s:" % num + "%s\n" % lines[num])
    all += 1
'''

'''
thread_num = int(sys.argv[1])
lines_length = len(lines)
processes = []
task_lines = []
start = 0
task_block = math.floor(lines_length / thread_num)
task_rest = lines_length % thread_num

print(task_rest)
print(task_block)
for i in range(1, thread_num + 1):
  #print(i)
  #print("最初" + "%s" % start)
  if i < thread_num:
    #print("最後" + "%s" % int(task_block * i))
    task_lines = lines[start:int(task_block * i)]
  else:
    #print("最後" + "%s" % int(task_block * i + task_rest))
    task_lines = lines[start:int(task_block * i + task_rest)]
  #print(task_lines[0])
  #print(task_lines[len(task_lines) - 1])

  processes.append(Process(group=None, target=lines_task, args=(task_lines, keyword,)))
  start = int(task_block * i)

for process in processes:
  print("process start!\n\n")
  process.start()

for process in processes:
  print("process end!\n\n")
  process.join()
'''

#html, title = extractor.as_html()
#print("html:%s\ntitle:%s" % (html, title))
#print("%s" % (type(title)))
  
#f.write(html)
#f.write(title)
  
title = extractor.extract_title(file)
print("title:%s" % title)
  
#f.write(title)
#f.close()
elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print("Sample_num:%s" % all)
