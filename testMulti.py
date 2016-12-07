from cython.parallel import parallel, threadid
import sys

list = [1,2,3,4,5,6,7,8,9,10]

for i in list:
  with parallel(int(sys.argv[1])):
    print(threadid())
    print(i)
