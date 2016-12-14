from cython.parallel cimport parallel
cimport openmp
import analysis

def multiTask(lines, keyword, num_threads):
  cdef int thread_id
  cdef int thread_max = num_threads
  cdef int lines_num = len(lines)
  upSentencedic = []
  leadID = []
  chunkdic = []
  keychunkID = []
  keytokenID = []
  RelateGroupes = []
  TokenGroupes = []
  num = [None for i in range(thread_max)]
  for j in range(lines_num):
    upSentencedic.append([])
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
      for num[thread_id] in range(thread_id, lines_num, thread_max):
        #print("num:%s" % num[thread_id] + "%s" % lines[num[thread_id]])
        if keyword in lines[num[thread_id]]:
          #print("num%s:" % num[thread_id] + "%s" % lines[num[thread_id]])
          #print("thread:%s" % thread_id)
          leadID[num[thread_id]], chunkdic[num[thread_id]], keychunkID[num[thread_id]], keytokenID[num[thread_id]], RelateGroupes[num[thread_id]], TokenGroupes[num[thread_id]] = analysiser.ReceivedObj(lines[num[thread_id]], keyword)
          #print(tree)
          #print(print_format)
          #print("leadID:%s" % leadID)
          #print("keywordID:%s" % keywordID)
          #print("%s" % chunkdic)
          upSentencedic[num[thread_id]] = analysiser.stepFourteen(leadID[num[thread_id]], chunkdic[num[thread_id]], keychunkID[num[thread_id]], keytokenID[num[thread_id]], RelateGroupes[num[thread_id]], TokenGroupes[num[thread_id]])
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