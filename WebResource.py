#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import extractcontent
import urllib.request
import codecs
import re
import sys
import time
#import unicodedata
#from functools import reduce
import analysis

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
  print('Usage: # python %s URL1 URL2 ... URLn Y/N:Search about keyword or not?' % argvs[0])
  quit()

sys.stdout.write("Please input number of Keyword:")
keyword_num = int(input())
keyword = [None for i in range(keyword_num)]

for i in range(keyword_num):
  sys.stdout.write("Please input a Keyword:")
  keyword[i] = input()

#print(keyword)
start = time.time()
analysiser = analysis.AnalysisContent()
all = 0
for num in range(1, UrlNum + 1):
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
  lines = []
  for line in text:
    lines.extend(line.split("。"))
  while (True):
    try:
      lines.remove("")
    except:                                                              
      break
  if keyword_num > 0:
    for num in range(keyword_num):
      for line in lines:
        if keyword[num] in line:
          print("\n本文:")
          print("%s:%s\n" % (keyword[num], line))
          leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysiser.ReceivedObj(line, keyword[num])
          #print("leadID:%s" % leadID)
          #print("keywordID:%s" % keywordID)
          #print("%s" % chunkdic)
          analysiser.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)
          all += 1
  else:
    for line in lines:
      print("\n本文:")
      print("%s\n" % line)
      all += 1
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
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print("Sample_num:%s" % all)
