#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import extractcontent
import urllib.request
import codecs
import re
import sys
#import math
import time
#from cython.parallel cimport parallel
#cimport openmp
#from multiprocessing import Process, Pipe
import multiprocessing as mp
#import unicodedata
#from functools import reduce
#import multiTask
import analysis
#from concurrent.futures import ProcessPoolExecutor, as_completed

'''
def divide_list(xs, n):
    q = len(xs) // n
    m = len(xs) % n

    return reduce(
        lambda acc, i:
            (lambda fr = sum([ len(x) for x in acc ]):
                acc + [ xs[fr:(fr + q + (1 if i < m else 0))] ]
            )()
        ,
        range(n),
        []
    )

def lists_multiTask(key_lines):
  upSentenceDic = {}
  #i = 0
  for line in key_lines[0]:
    upSentences = {}
    for key in key_lines[1]:
      if key in line:
        #print(mp.current_process())
        leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysis.AnalysisContent().ReceivedObj(line, key)
        upSentences[key] = analysis.AnalysisContent().stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)
    upSentenceDic[line] = upSentences
    #print(i)
    #i = i + 1
  return upSentenceDic
'''

def multiTask(key_lines):#sentence, keyword, line_index, line_num):
  upSentences = {}
  '''
  for key in key_lines[1]:#keyword:
    if key in key_lines[0]:#sentence:
  '''
  leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysis.AnalysisContent().ReceivedObj(key_lines[0], key_lines[1])#sentence, key)
  upSentences[key_lines[1]] = analysis.AnalysisContent().stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)
  #print("%s" % mp.current_process() + "%s" % key_lines[3])#upSentences)
  return {key_lines[2]:upSentences}#{line_num:upSentences}


'''
def wrapper_plus_data(args):
  return multiTask(*args)



def multiTask_one(key_lines, thread_num):
  pool = mp.Pool(thread_num)
  return pool.map(wrapper_plus_data, key_lines)
'''


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
UrlNum = argc - 2

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
#keyword = [ 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s', 'iPhone 6s']
#keyword = ['Apple TV', 'Apple Pencil', 'iPhone 6s', 'Apple Watch', 'iPhone 6s Plus', 'iPad Pro', 'iPad Air']
keyword = ['Apple TV', 'Apple Pencil']
keyword_num = len(keyword)

thread_num = int(sys.argv[1])
#analysiser = analysis.AnalysisContent()
lines = []
for num in range(2, argc):
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
start = time.time()
if keyword_num > 0:
  #upSentencedic = multiTask.multiTask(lines, keyword, int(sys.argv[1]))
  #upSentencedic = multiTask.multiPrange(lines, keyword, int(sys.argv[1]))
  #upSentencedic = multiTask.multiList(lines, keyword, int(sys.argv[1]))
  #print(upSentencedic)

  #key_lines = [[lines[i], keyword, i] for i in range(len(lines))]
  #answerLines = multiTask_one(key_lines, thread_num)

  '''
  lists = divide_list(lines, thread_num)
  key_lines = [[line, keyword] for line in lists]
  for li in lists:
    print(li)
  pool = mp.Pool(thread_num)
  answerLines = []
  answerLines = pool.map(lists_multiTask, key_lines)
  '''

  #pool = ProcessPoolExecutor(thread_num)

  #key_lines = [(lines[i], keyword, i) for i in range(len(lines))]
  
  key_lines = []
  #k = 0
  for i in range(len(lines)):
    #l = 0
    for key in keyword:
      if key in lines[i]:# and l == 0:
        key_lines.append((lines[i], key, i))#, k))
        #print("k:%s" % k)
        #print("line:%s" % i)
        #k += 1
        #l += 1
      #else:
        #continue

  '''
  size, extra = divmod(len(key_lines), thread_num)
  if extra > 0:
    chunksize = size + 1
  else:
    chunksize = size
  '''

  pool = mp.Pool(thread_num)
  answerLines = pool.map(multiTask, key_lines)#, chunksize)
  #print(divmod(len(key_lines), thread_num))

  '''
  #print(answerLines)
  #Poolの呼び出し
  for answerLine in answerLines:
    for num in range(len(lines)):
      for key_lin in answerLine.keys():
        i = 0
        if key_lin == num and i == 0:
          i += 1
          for value in answerLine.values():
            for key in value.keys():
              for i in range(keyword_num):
                if key == keyword[i]:
                  print("\n%s:" % num + "%s:\n%s" % (keyword[i], lines[num]))
                  print(answerLine[num][keyword[i]])
                  all += 1
        else:
          continue
  '''

  
  for answerLine in answerLines:
    for line_num in answerLine.keys():
      print("sentence:%s" % lines[line_num])
      for sentences in answerLine[line_num].values():
        print(answerLine[line_num].keys())
        all += 1
        print("Answer:%s" % sentences)
      print("\n")
  

  #print([i for i in range(55, len(lines))])

  #for i in upSentencedic:
    #print(i)


  '''
  #ProcessPoolExecutorの呼び出し
  for sentence in answerLines:
    for i in range(keyword_num):
      #print(sentence)
      for num in range(len(lines)):
        #print(sentence)
        for num_key in sentence.keys():
          if num_key == num:
            #print("num:%s" % num + "num_key:%s" % num_key)
            for key in sentence[num_key].keys():
              if keyword[i] in key:
                print("\n%s:" % num + "%s:\n%s" % (keyword[i], lines[num]))
                print(sentence[num_key][keyword[i]])
                all += 1
            continue
  pool.shutdown()
  '''

  '''
  #lists_maltiTaskの呼び出し
  for k in answerLines:
    for num in range(len(lines)):
      for line_key in k.keys():
        if line_key == lines[num]:
          #print("key:%s" % line_key)
          #print(lines[num])
          for key in k[lines[num]].keys():
            for i in range(keyword_num):
              if keyword[i] in key:
                print("\n%s:" % num + "%s:\n%s" % (keyword[i], lines[num]))
                print(k[lines[num]][keyword[i]])
                all += 1
  '''

else:
  for num in range(len(lines)):
    print("\n%s:" % num + "%s\n" % lines[num])
    all += 1


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
#print(mp.cpu_count())
#print(len(lines))
