import sys
import codecs
import re
import urllib.request
import string
from bs4 import BeautifulSoup

argvs = sys.argv
argc = len(argvs)
UrlNum = argc - 2

if (argvs[argc - 1] in "Y" and UrlNum > 0):
  sys.stdout.write("Please input a Keyword:")
  keyword = input()
elif (UrlNum <= 0):
  print('Usage: # python %s URL1 URL2 ... URLn Y/N:Search about keyword or not?' % argvs[0])
  quit()

for num in range(1, UrlNum + 1):
  html = urllib.request.urlopen(argvs[num])
  soup = BeautifulSoup(html, "html.parser")

  if (argvs[argc - 1] in "Y"):
    h1 = soup.find_all("h1", text=re.compile(keyword))
    h2 = soup.find_all("h2", text=re.compile(keyword))
    h3 = soup.find_all("h3", text=re.compile(keyword))
    p = soup.find_all("p", text=re.compile(keyword))
  else:
    h1 = soup.find_all("h1")
    h2 = soup.find_all("h2")
    h3 = soup.find_all("h3")
    p = soup.find_all("p")

  print("\n\n\nURL:" + argvs[num] + "\n")
  print("\n\ntag:<h1>")

#  f = open('text.txt', 'w') 

  for list in h1:
    print("%s" % (re.sub('<.*?>', '', str(list))))
#    f.write(re.sub('<.*?>', '', str(list))) 

  print("\n\ntag:<h2>")
  for list in h2:
    print("%s" % (re.sub('<.*?>', '', str(list)))) 
#    f.write(re.sub('<.*?>', '', str(list))) 

  print("\n\ntag:<h3>")
  for list in h3:
    print("%s" % (re.sub('<.*?>', '', str(list)))) 
#    f.write(re.sub('<.*?>', '', str(list))) 

  print("\n\ntag:<p>")
  for list in p:
    print("%s" % (re.sub('<.*?>', '', str(list))))
#    f.write(re.sub('<.*?>', '', str(list))) 

#  f.close()
