fp = open('./answer.txt', 'r')
answerLines = fp.readlines()
print(answerLines)
fp.close()

answerData = []
for answerLine in answerLines:
  answerData.append(answerLine.split(" "))
print(answerData)
