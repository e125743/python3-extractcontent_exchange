from cython.parallel cimport parallel
cimport openmp
import analysis

def multiTask(lines, keyword, num_threads):
  cdef int thread_id
  cdef int thread_max = num_threads
  cdef int lines_num = len(lines)
  upSentencedic = [{} for j in range(lines_num)]
  leadID = []
  chunkdic = []
  keychunkID = []
  keytokenID = []
  RelateGroupes = []
  TokenGroupes = []
  keyword_num = []
  num = []
  for i in range(thread_max):
    keyword_num.append('')
    num.append('')
    leadID.append([])
    chunkdic.append([])
    keychunkID.append([])
    keytokenID.append([])
    RelateGroupes.append([])
    TokenGroupes.append([])
  analysiser = analysis.AnalysisContent()
  with nogil, parallel(num_threads=thread_max):
    with gil:
      thread_id = openmp.omp_get_thread_num()
      for keyword_num[thread_id] in range(len(keyword)):
        for num[thread_id] in range(thread_id, lines_num, thread_max):
          #print("num:%s" % num[thread_id] + "%s" % lines[num[thread_id]])
          if keyword[keyword_num[thread_id]] in lines[num[thread_id]]:
            #print("num%s:" % num[thread_id] + "%s" % lines[num[thread_id]])
            #print("thread:%s" % thread_id)
            leadID[thread_id], chunkdic[thread_id], keychunkID[thread_id], keytokenID[thread_id], RelateGroupes[thread_id], TokenGroupes[thread_id] = analysiser.ReceivedObj(lines[num[thread_id]], keyword[keyword_num[thread_id]])
            #print(tree)
            #print(print_format)
            #print("leadID:%s" % leadID)
            #print("keywordID:%s" % keywordID)
            #print("%s" % chunkdic)
            upSentencedic[num[thread_id]][keyword[keyword_num[thread_id]]] = analysiser.stepFourteen(leadID[thread_id], chunkdic[thread_id], keychunkID[thread_id], keytokenID[thread_id], RelateGroupes[thread_id], TokenGroupes[thread_id])
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