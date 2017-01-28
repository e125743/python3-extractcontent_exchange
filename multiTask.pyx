from cython.parallel cimport parallel, prange
cimport openmp
import analysis
import time
from functools import reduce
import sys
import CaboCha
import xml.etree.ElementTree as ET
import analysis

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

Def multiList(lines, keywords, num_threads):
  cdef int thread_id
  cdef int thread_max = num_threads
  cdef lists = divide_list(lines, num_threads)
  answers = []
  for i in range(thread_max):
    answers.append('')

  #並列化
  with nogil, parallel(num_threads=thread_max):
    with gil:
      thread_id = openmp.omp_get_thread_num()
      list = lists[thread_id]
      #print(list)
      answer = []
      #analysiser = analysis.AnalysisContent()
      keyword = keywords
      #print("thread:%s\n" % thread_id + "%s" % lists[thread_id])
      for sentence in list:
        for key in keyword:
          if key in sentence:
            leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysis.ReceivedObj(sentence, key)

            """
            c = CaboCha.Parser()
            tree =  c.parse(sentence)
            #print("%s" % tree.toString(CaboCha.FORMAT_TREE)) #簡易 Tree 表示での出力                                         
            #print("%s" % tree.toString(CaboCha.FORMAT_LATTICE)) #計算機に処理しやすいフォーマットで出力                      
            sent = ET.fromstring(tree.toString(CaboCha.FORMAT_XML))

            keychunkID = []
            keytokenID = []
            leadID = []
            chunkdic = {}
            AlreadyID = []
            TokenGroupes = {}
            RelateGroupes = []
            for chunk in sent.findall('.//chunk'):
              #print("%s" % sent.findall(".//chunk[@id='0']"))

              if chunk.attrib['id'] not in AlreadyID:
                leadID.append(chunk.attrib['id'])
                linkid = int(chunk.attrib['id'])

                RelateID = []
                while True:
                  linkchunk = sent.find(".//chunk[@id='{linkid}']".format(**locals()))
                  if linkid == '-1':
                    RelateGroupes.append(RelateID)
                    #print("listed!")
                    #print("RelateGroupes:%s" % RelateGroupes)
                  else:
                    RelateID.append(int(linkid))
                    #print("appendet!")
                    #print("RelateID:%s" % RelateID)

                  if linkchunk != None:
                    if linkchunk.attrib['id'] not in AlreadyID:
                      chunkText = ""
                      AlreadyID.append(linkchunk.attrib['id'])

                      for tok in linkchunk:
                        chunkText = chunkText + tok.text
                        chunkdic.setdefault(int(linkchunk.attrib['id']), {})[int('{tok.attrib[id]}'.format(**locals()))] = [tok.attrib['feature'], tok.text]
                        TokenGroupes.setdefault(int(linkchunk.attrib['id']), []).append(int('{tok.attrib[id]}'.format(**locals())))
                        #print("text:%s" % tok.text)
                        #print("id:%s" % tok.attrib['id'])
                        if chunkText.endswith(key.replace(" ","")) is True:
                          keychunkID.append(int(linkchunk.attrib['id']))
                          keytokenID.append(int(tok.attrib['id']))

                      chunkdic.setdefault(int(linkchunk.attrib['id']), {})[int(sys.maxsize)] = int(linkchunk.attrib['link'])

                      #for id,text in sorted(chunkdic[int(linkchunk.attrib['id'])].items()):
                        #print("chunk:" + str(id) + "," + str(text))

                    linkid = linkchunk.attrib['link']
                    #print("linkid:%s" % linkid)
                    #print("keywordID:%s" % keywordID)

                  else:
                    break
            """

            upSentences = analysis.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)

            """
            i = 0
            upSentences = []
            for id in keychunkID:
              #print("keychunkID:%s" % id)
              keychunk = chunkdic[id]
              keytokenEnd = TokenGroupes[id][-1]
              keytokenFirst = TokenGroupes[id][0]

              try:
                keyrear = keychunk[int(keytokenID[i]) + 1]
              except:
                if keychunk[int(sys.maxsize)] == -1:
                  #print("%s" % keychunk[int(sys.maxsize)])
                  keyrear = []

                else:
                  keychunk = chunkdic[int(id) + 1]
                  keyrear = keychunk[int(keytokenID[i]) + 1]

              #print("keyrear:%s" % keyrear)

              if len(keyrear) != 0:
                endtokenid = 0
                if keyrear[1] == 'の':
                  #print("Yes:%s" % keyrear[1])

                  for Groupe in RelateGroupes:
                    if id in Groupe:

                      for groupeid in range(1, len(Groupe)):
                        if Groupe[groupeid] - Groupe[groupeid - 1] > 1 and Groupe[groupeid] > id and endtokenid == 0:
                          #print("%s" % int(Groupe[groupeid] - Groupe[groupeid - 1]))                                         
                          lastid = Groupe[groupeid]
                          beginid = Groupe[groupeid - 1]

                          rearLast = []
                          for RelateGroupe in RelateGroupes:
                            #RelateGroupe_set = set(RelateGroupe)
                            #matching = list(RelateGroupe_set & rearGroupe_set)
                            rearLast.extend(list(filter((lambda x: beginid < x < lastid), RelateGroupe)))

                          #print("%s" % sorted(set(rearLast), reverse=True))
                          for chunkid in sorted(set(rearLast), reverse=True):
                            if endtokenid == 0:
                              #endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)

                              endtokenid = 0
                              sentenceEnd = 0
                              alltext = ""
                              endflag = 0
                              basicflag = 0
                              for id,text in sorted(chunkdic[chunkid].items()):
                                if isinstance(text, list):
                                  alltext = alltext + text[1]
                                  sentenceEnd = id
                                  #print("%s" % type(text))
                                  #print("%s" % alltext)
                                  #print("%s" % text[1])


                                  if "動詞" in text[0] and "自立" in text[0] and "非自立" not in text[0] and endflag == 0 and basicflag == 0:
                                    endflag = 1
                                    #print("自立a%s" % endflag)

                                  elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:
                                    endflag = 1
                                    #print("自立b%s" % endflag)

                                  else:
                                    endflag = 0
                                    #print("自立%s" % endflag)

                                  if "基本形" in text[0]:
                                    basicflag = 1

                                  if endflag == 1:
                                    #print("endtoken:%s" % alltext)
                                    #print("%s" % endflag)
                                    endtokenid = id

                                  elif alltext.endswith("だ") is True:
                                    #print("endtoken:%s" % alltext)
                                    endtokenid = id

                                  elif alltext.endswith("である") is True:
                                    #print("endtoken:%s" % alltext)
                                    endtokenid = id

                              #print("%s" % endtokenid)
                            else:
                              #print("endtokenid:%s" % endtokenid)
                              #print("sentenceEnd:%s" % sentenceEnd)
                              break

                      if endtokenid == 0:
                        for Groupe in RelateGroupes:
                          if id in Groupe:
                            for chunkid in sorted(Groupe, reverse=True):
                              if endtokenid == 0:
                                #endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)

                                endtokenid = 0
                                sentenceEnd = 0
                                alltext = ""
                                endflag = 0
                                basicflag = 0
                                for id,text in sorted(chunkdic[chunkid].items()):
                                  if isinstance(text, list):
                                    alltext = alltext + text[1]
                                    sentenceEnd = id
                                    #print("%s" % type(text))
                                    #print("%s" % alltext)
                                    #print("%s" % text[1])


                                    if "動詞" in text[0] and "自立" in text[0] and "非自立" not in text[0] and endflag == 0 and basicflag == 0:
                                      endflag = 1
                                      #print("自立a%s" % endflag)

                                    elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:
                                      endflag = 1
                                      #print("自立b%s" % endflag)

                                    else:
                                      endflag = 0
                                      #print("自立%s" % endflag)

                                    if "基本形" in text[0]:
                                      basicflag = 1

                                    if endflag == 1:
                                      #print("endtoken:%s" % alltext)
                                      #print("%s" % endflag)
                                      endtokenid = id

                                    elif alltext.endswith("だ") is True:
                                      #print("endtoken:%s" % alltext)
                                      endtokenid = id

                                    elif alltext.endswith("である") is True:
                                      #print("endtoken:%s" % alltext)
                                      endtokenid = id

                              else:
                                #print("endtokenid:%s" % endtokenid)
                                #print("sentenceEnd:%s" % sentenceEnd)
                                break


                else:
                  #print("not:%s" % keyrear[1])
                  #endtokenid = 0
                  for Groupe in RelateGroupes:
                    if id in Groupe:
                      for chunkid in sorted(Groupe, reverse=True):
                        if endtokenid == 0:
                          #endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)

                          endtokenid = 0
                          sentenceEnd = 0
                          alltext = ""
                          endflag = 0
                          basicflag = 0
                          for id,text in sorted(chunkdic[chunkid].items()):
                            if isinstance(text, list):
                              alltext = alltext + text[1]
                              sentenceEnd = id
                              #print("%s" % type(text))
                              #print("%s" % alltext)
                              #print("%s" % text[1])


                              if "動詞" in text[0] and "自立" in text[0] and "非自立" not in text[0] and endflag == 0 and basicflag == 0:
                                endflag = 1
                                #print("自立a%s" % endflag)

                              elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:
                                endflag = 1
                                #print("自立b%s" % endflag)

                              else:
                                endflag = 0
                                #print("自立%s" % endflag)

                              if "基本形" in text[0]:
                                basicflag = 1

                              if endflag == 1:
                                #print("endtoken:%s" % alltext)
                                #print("%s" % endflag)
                                endtokenid = id

                              elif alltext.endswith("だ") is True:
                                #print("endtoken:%s" % alltext)
                                endtokenid = id

                              elif alltext.endswith("である") is True:
                                #print("endtoken:%s" % alltext)
                                endtokenid = id

                        else:
                          #print("endtokenid:%s" % endtokenid)
                          #print("sentenceEnd:%s" % sentenceEnd)
                          break

                  if endtokenid == 0:
                    for Groupe in RelateGroupes:
                      if id not in Groupe:

                        for chunkid in sorted(Groupe, reverse=True):
                          if endtokenid == 0:
                            #endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)

                            endtokenid = 0
                            sentenceEnd = 0
                            alltext = ""
                            endflag = 0
                            basicflag = 0
                            for id,text in sorted(chunkdic[chunkid].items()):
                              if isinstance(text, list):
                                alltext = alltext + text[1]
                                sentenceEnd = id
                                #print("%s" % type(text))
                                #print("%s" % alltext)
                                #print("%s" % text[1])


                                if "動詞" in text[0] and "自立" in text[0] and "非自立" not in text[0] and endflag == 0 and basicflag == 0:
                                  endflag = 1
                                  #print("自立a%s" % endflag)

                                elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:
                                  endflag = 1
                                  #print("自立b%s" % endflag)

                                else:
                                  endflag = 0
                                  #print("自立%s" % endflag)

                                if "基本形" in text[0]:
                                  basicflag = 1

                                if endflag == 1:
                                  #print("endtoken:%s" % alltext)
                                  #print("%s" % endflag)
                                  endtokenid = id

                                elif alltext.endswith("だ") is True:
                                  #print("endtoken:%s" % alltext)
                                  endtokenid = id

                                elif alltext.endswith("である") is True:
                                  #print("endtoken:%s" % alltext)
                                  endtokenid = id

                          else:
                            #print("endtokenid:%s" % endtokenid)
                            #print("sentenceEnd:%s" % sentenceEnd)
                            break

                if endtokenid != 0:
                  upToken = {}
                  #print("%s" % chunkdic)
                  #print("keytokenEnd:%s" % keytokenEnd)
                  #print("keytokenFirst:%s" % keytokenFirst)
                  for chunk in chunkdic.values():
                    #print("%s" % chunk)
                    for tokenid in chunk.keys():
                      #print("token:%s" % chunk[tokenid])

                      if isinstance(chunk[tokenid], list) is True:

                        if tokenid == endtokenid:
                          if chunk[tokenid][1].endswith("だ") is True:
                            chunk[tokenid][1] = "である"

                        if keytokenEnd < tokenid <= int(endtokenid):
                          setid = tokenid + keytokenFirst - keytokenEnd - 1
                        elif keytokenFirst <= tokenid <= keytokenID[i]:
                          setid = endtokenid + tokenid - keytokenEnd
                        elif tokenid < keytokenFirst:
                          setid = tokenid
                        else:
                          continue

                        upToken[setid] = chunk[tokenid][1]

                  upSentence = ''
                  for key in sorted(upToken.keys()):
                    upSentence = upSentence + upToken[key]
                  #print("upSentence:%s" % upSentence)
              upSentences.append(upSentence)
              i = i + 1
            """

            answer.append(upSentences)
      #print("thread:%s\n" % thread_id + "%s\n" % answer + "%s\n" % key)
      answers[thread_id] = answer

  return answers

def multiTask(lines, keyword, num_threads):
  cdef int thread_id
  cdef int thread_max = num_threads
  cdef int lines_num = len(lines)
  upSentencedic = [ {} for j in range(lines_num)]
  leadID = []
  chunkdic = []
  keychunkID = []
  keytokenID = []
  RelateGroupes = []
  TokenGroupes = []
  keyword_num = []
  num = []
  analysiser = []
  keywords = []
  for i in range(thread_max):
    analysiser.append(analysis.AnalysisContent())
    keyword_num.append('')
    num.append('')
    leadID.append([])
    chunkdic.append([])
    keychunkID.append([])
    keytokenID.append([])
    RelateGroupes.append([])
    TokenGroupes.append([])
    keywords.append(keyword)
  #start = time.time()
  with nogil, parallel(num_threads=thread_max):
    with gil:
      thread_id = openmp.omp_get_thread_num()
      for keyword_num[thread_id] in range(len(keyword)):
        for num[thread_id] in range(thread_id, lines_num, thread_max):
          #print("num:%s" % num[thread_id] + "%s" % lines[num[thread_id]])
          if keyword[keyword_num[thread_id]] in lines[num[thread_id]]:
            #print("num%s:" % num[thread_id] + "%s" % lines[num[thread_id]])
            #print("thread:%s" % thread_id)
            #elapsed_time = time.time() - start
            #print("ReceivedObj_start:{0}".format(elapsed_time) + "[sec]" + ":%s" % thread_id)
            leadID[thread_id], chunkdic[thread_id], keychunkID[thread_id], keytokenID[thread_id], RelateGroupes[thread_id], TokenGroupes[thread_id] = analysiser[thread_id].ReceivedObj(lines[num[thread_id]], keywords[thread_id][keyword_num[thread_id]])
            #print(tree)
            #print(print_format)
            #print("leadID:%s" % leadID)
            #print("keywordID:%s" % keywordID)
            #print("%s" % chunkdic)
            #elapsed_time = time.time() - start
            #print("stepFourteen_start:{0}".format(elapsed_time) + "[sec]" + ":%s" % thread_id)
            upSentencedic[num[thread_id]][keyword[keyword_num[thread_id]]] = analysiser[thread_id].stepFourteen(leadID[thread_id], chunkdic[thread_id], keychunkID[thread_id], keytokenID[thread_id], RelateGroupes[thread_id], TokenGroupes[thread_id])
            #if len(upSentencedic[num]) == 0:
              #upSentencedic[num] = ""
              #print("num:%s" % num)
              #print("thread:%s" % thread_id)
              #print("\n本文:%s\n" % lines[num])
              #print("%s" % num + ":%s" % upSentencedic[num])
              #for upSentence in upSentencedic]:
                #print(upSentence)
  #print(upSentencedic)
  print(openmp.omp_get_max_threads())
  return upSentencedic



def multiPrange(lines, keyword, num_threads):
  cdef int i
  cdef int thread_max = num_threads
  cdef int lines_num = len(lines)
  cdef upSentencedic = [ {} for j in range(lines_num) ]
  #key = []
  #keywordlist = []
  #num = []
  #for k in range(thread_max):
    #num.append('')
    #key.append('')
    #keywordlist.append(keyword)
  analysiser = analysis.AnalysisContent()
  start = time.time()
  for key in keyword:
    with nogil, parallel(num_threads=thread_max):
      for i in prange(lines_num, schedule='static'):
        with gil:
              #thread_id = openmp.omp_get_thread_num()
        #num[thread_id] = 0
        #for key[thread_id] in keywordlist[thread_id]:
            #print("num:%s" % num[thread_id] + "%s" % lines[num[thread_id]])
              if key in lines[i]:
            #print("num%s:" % num[thread_id] + "%s" % lines[num[thread_id]])
            #print("thread:%s" % thread_id)
                #elapsed_time = time.time() - start
                #print("ReceivedObj_start:{0}".format(elapsed_time) + "[sec]" + ":key%s" % key + ":th%s" % thread_id + ":l%s" % i)
                leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysiser.ReceivedObj(lines[i], key)
            #print(tree)
            #print(print_format)
            #print("leadID:%s" % leadID)
            #print("keywordID:%s" % keywordID)
            #print("%s" % chunkdic)
                #elapsed_time = time.time() - start
                #print("stepFourteen_start:{0}".format(elapsed_time) + "[sec]" + ":key%s" % key + ":th%s" % thread_id + ":l%s" % i)# + ":num%s" % num)
                upSentencedic[i][key] = analysiser.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)#, upSentencedic, i, num[thread_id])
              #num[thread_id] =+ 1
            #if len(upSentencedic[num]) == 0:
              #upSentencedic[num] = ""
              #print("num:%s" % num)
              #print("thread:%s" % thread_id)
              #print("\n本文:%s\n" % lines[num])
              #print("%s" % num + ":%s" % upSentencedic[num])
              #for upSentence in upSentencedic]:
                #print(upSentence)
  #print(upSentencedic)
  #print(openmp.omp_get_max_threads())
  return upSentencedic