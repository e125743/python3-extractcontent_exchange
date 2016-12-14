import sys

argvs = sys.argv
argc = len(argvs)

if (argc <= 2):
  print('Usage: # python %s list_nums ListSubscript ... n>list_nums' % argvs[0])
  quit()

list_max = int(argvs[1])
argvs = argvs[2:argc]


list = []
for i in range(0, list_max):
  list.append([])

print(list)
print(argvs)

for i in argvs:
  if int(i) < list_max:
    list[int(i)] = i

print(list)
