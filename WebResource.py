#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import extractcontent
import urllib.request
import codecs
import re
import sys
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

sys.stdout.write("Please input a Keyword:")
keyword = input()

if (UrlNum <= 0):
  print('Usage: # python %s URL1 URL2 ... URLn Y/N:Search about keyword or not?' % argvs[0])
  quit()

analysiser = analysis.AnalysisContent()
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
  for line in lines:
    if keyword in line:
      print("\n本文:")
      print("%s\n" % line)
      leadID, chunkdic, keychunkID, keytokenID, RelateGroupes = analysiser.ReceivedObj(line, keyword)
      #print("leadID:%s" % leadID)
      #print("keywordID:%s" % keywordID)
      #print("%s" % chunkdic)
      analysiser.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes)

  #html, title = extractor.as_html()
  #print("html:%s\ntitle:%s" % (html, title))
  #print("%s" % (type(title)))
  
  #f.write(html)
  #f.write(title)
  
  title = extractor.extract_title(file)
  print("title:%s" % title)
  
  #f.write(title)
  #f.close()
