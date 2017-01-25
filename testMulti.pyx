from cython.parallel cimport parallel
cimport openmp
 
def getnumthreads(n):
    cdef int thread_id
    cdef int num_threads = int(n)
    list = [1,2,3,4,5,6,7,8,9,10]
    with nogil, parallel(num_threads=num_threads):
      with gil:
        thread_id = openmp.omp_get_thread_num()
        for i in range(thread_id, len(list), num_threads):
          print("list:%s" % list[i])
          print("thread:%s" % thread_id)