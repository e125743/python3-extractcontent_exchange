from cython.parallel cimport parallel, prange
cimport openmp
import analysis
import time

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
  start = time.time()
  with nogil, parallel(num_threads=thread_max):
    with gil:
      thread_id = openmp.omp_get_thread_num()
      for keyword_num[thread_id] in range(len(keyword)):
        for num[thread_id] in range(thread_id, lines_num, thread_max):
          #print("num:%s" % num[thread_id] + "%s" % lines[num[thread_id]])
          if keyword[keyword_num[thread_id]] in lines[num[thread_id]]:
            #print("num%s:" % num[thread_id] + "%s" % lines[num[thread_id]])
            #print("thread:%s" % thread_id)
            elapsed_time = time.time() - start
            print("ReceivedObj_start:{0}".format(elapsed_time) + "[sec]" + ":%s" % thread_id)
            leadID[thread_id], chunkdic[thread_id], keychunkID[thread_id], keytokenID[thread_id], RelateGroupes[thread_id], TokenGroupes[thread_id] = analysiser[thread_id].ReceivedObj(lines[num[thread_id]], keyword[keyword_num[thread_id]])
            #print(tree)
            #print(print_format)
            #print("leadID:%s" % leadID)
            #print("keywordID:%s" % keywordID)
            #print("%s" % chunkdic)
            elapsed_time = time.time() - start
            print("stepFourteen_start:{0}".format(elapsed_time) + "[sec]" + ":%s" % thread_id)
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
      for i in prange(lines_num, schedule='guided'):
        with gil:
              thread_id = openmp.omp_get_thread_num()
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
  return upSentencedic