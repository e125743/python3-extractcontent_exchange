#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import extractcontent
import urllib.request
import codecs
import re
import sys
import time
#import unicodedata
#from functools import reduce
import analysis
import os
import mysql.connector

#Webページの文書をエンコード
def conv_encoding(data):
    #エンコードする際の文字コード一覧
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
            'shift_jis', 'shift_jis_2004','shift_jisx0213',
            'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
            'iso2022_jp_ext','latin_1', 'ascii')
    #encode = None

    #全ての文字コードでエンコードを試行
    for encoding in lookup:
      try:
        #エンコードに成功した文書データを取得
        data = data.decode(encoding)
        #encode = encoding
        break
      except:
        pass

    #文書データを返還
    if isinstance(data, str):
        return data#,encode
    else:
        #返還に失敗した時にエラーメッセージ
        raise LookupError


def insertSentences(sentence, keyword, connector, cursor):
    '''
    connector = mysql.connector.connect(
                user='root',
                password=os.environ['PASSWORD'],
                host='localhost',
                database='debugger')
    cursor = connector.cursor()
    '''
    #sentencesテーブルに文章と興味キーワードの組み合わせがあるかを判定
    cursor.execute("select id from sentences where sentence = '" + sentence + "' and keyword = '" + keyword + "';")
    #print(cursor.fetchall())
    sentences = cursor.fetchall()

    #sentencesテーブルに文章と興味キーワードの組み合わせが未存在
    if len(sentences) == 0:
        print("row is null")
        #sys.stdout.write("Do you input %s or not?(Y/N)" % sentence)
        #flag = input()
        #if flag == 'Y':

        #sentencesテーブルのレコードに文章と興味キーワードを挿入
        cursor.execute("insert into sentences(sentence, keyword) values('" + sentence + "', '" + keyword + "');")
        print("Input a keyword:%s\n" % keyword + "sentence:%s" % sentence)
        #挿入したレコードのidを取得
        cursor.execute("select id from sentences where sentence = '" + sentence + "' and keyword = '" + keyword + "';")
        #print(cursor.fetchall())
        sentences = cursor.fetchall()

    #変更を保存
    connector.commit()
    '''
    cursor.close
    connector.close
    '''
    #挿入したレコードのidを返還
    return sentences



#1.解析した文章(sentencesId)がprogramLawsテーブルに未存在
#2.解析した文章(sentencesId)は、programLawsテーブルにあるが、
#生成した文章(answer)が未存在
#上記の条件の時、programLawsテーブルに解析した文章と生成した文章を挿入し、
#挿入したデータ群をmyLaws.txtに保存
def insertProgramLaws(sentencesId, answer, lawNumber, connector, cursor, index, lawAnswer, fp):
    '''
    connector = mysql.connector.connect(
                user='root',
                password=os.environ['PASSWORD'],
                host='localhost',
                database='debugger')
    cursor = connector.cursor()
    '''
    #programLawsテーブルに解析した文章が存在する時、生成されていた文章を取得
    cursor.execute("select answer from programLaws where sentences_id = " + sentencesId + " and law_number = " + lawNumber + ";")
    #print(cursor.fetchall())
    sentences = cursor.fetchall()

    #解析した文章がprogramLawsテーブルに未存在
    if len(sentences) == 0:
        print("row is null")
        #sys.stdout.write("Do you input %s or not?(Y/N)" % sentence)
        #flag = input()
        #if flag == 'Y':

        #programLawsテーブルに解析した文章と生成された文章を挿入
        cursor.execute("insert into programLaws(sentences_id, answer, law_number) values(" + sentencesId + ", '" + answer + "'," + lawNumber + ");")
        print("Input a law_number:%s\n" % lawNumber + "answer:%s" % answer)
        #programLawsテーブルに挿入した時のidを取得
        cursor.execute("select id from programLaws order by id desc limit 1")
        programId = cursor.fetchall()
        print("%s " % lawAnswer[0] + "%s " % programId[0] + "%s " % lawAnswer[1] + "%s" % lawAnswer[2])
        program_id = list(programId[0])
        #myLaw.txtにprogramLawsテーブルに挿入した生成された文章の理想値を保存
        writeData = lawAnswer[0] + " " + str(program_id[0]) + " " + lawAnswer[1] + " " + lawAnswer[2]
        print("insert:%s" % writeData)
        fp.write(writeData)
        #answerDataの添字をインクリメント
        index = index + 1
    #解析した文章がprogramLawsテーブルに存在
    else:
        i = 0
        #programLawsテーブルに生成された文章が存在するかを判定
        for row in sentences:
            if answer == row[0]:
                i = i + 1
        #programLawsテーブルに生成された文章が未存在
        if i == 0:
            #programLawsテーブルに解析した文章と生成された文章を挿入
            cursor.execute("insert into programLaws(sentences_id, answer, law_number) values(" + sentencesId + ", '" + answer + "'," + lawNumber + ");")
            print("Input a law_number:%s\n" % lawNumber + "answer:%s" % answer)
            #programLawsテーブルに挿入した時のidを取得
            cursor.execute("select id from programLaws order by id desc limit 1")
            programId = cursor.fetchall()
            print("%s " % lawAnswer[0] + "%s " % programId[0] + "%s " % lawAnswer[1] + "%s" % lawAnswer[2])
            program_id = list(programId[0])
            #myLaw.txtにprogramLawsテーブルに挿入した生成された文章の理想値を保存
            writeData = lawAnswer[0] + " " + str(program_id[0]) + " " + lawAnswer[1] + " " + lawAnswer[2]
            print("insert:%s" % writeData)
            fp.write(writeData)
            #answerDataの添字をインクリメント
            index = index + 1

    #programLawsテーブルの変更を保存
    connector.commit()
    return index
    '''
    cursor.close
    connector.close
    '''

#Webページのスクリーニングクラスの呼び出し
extractor = extractcontent.ExtractContent()

#パラメータを設定
opt = {"threshold":1, "continuous_factor": 1.00, "punctuation_weight": 20}#, "debug": True}
extractor.set_default(opt)

#コマンドライン引数からURLを取得
argvs = sys.argv
argc = len(argvs)
UrlNum = argc - 1

#データベースの設定と接続
connector = mysql.connector.connect(
            user='root',
            password=os.environ['PASSWORD'],
            host='localhost',
            database='debugger')
cursor = connector.cursor()

#URLのエラーメッセージ
if (UrlNum <= 0):
  print('Usage: # python %s URL1 URL2 ... URLn Y/N:Search about keyword or not?' % argvs[0])
  quit()

'''
sys.stdout.write("Please input number of Keyword:")
keyword_num = int(input())
keyword = [None for i in range(keyword_num)]

for i in range(keyword_num):
  sys.stdout.write("Please input a Keyword:")
  keyword[i] = input()
'''

#興味キーワード
keyword = ['Apple TV', 'Apple Pencil']
#興味キーワードの総数
keyword_num = len(keyword)
#print(keyword)

#時間計測
start = time.time()

#解析するクラスと接続
analysiser = analysis.AnalysisContent()
all = 0

#理想値（['NULL 理想とする文 ◯\n']）を取得
fp = open('./answer.txt', 'r')
#理想値を配列に変換
answerLines = fp.readlines()
print(answerLines)
fp.close()

#理想値を細かく分割（['NULL', '理想とする文', '◯\n']）
answerData = []
for answerLine in answerLines:
  answerData.append(answerLine.split(" "))
print(answerData)

#プログラムの結果を保存するファイル作成
fp = open('./myLaws.txt', 'w')

#answerDataの添字
index = 0
#コマンドラインのURL群を分割
for num in range(1, UrlNum + 1):
  #コマンドラインのURLを取得
  response = urllib.request.urlopen(argvs[num])
  #URLからWebページの文書を取得
  html = response.read()

  #文書をutf-8形式で保存するファイル作成
  f = codecs.open("index.txt", "w", "utf-8")

  #文書をエンコード
  data = conv_encoding(html)

  #エンコードされた文書コードをutf-8で保存
  f.write(data)
  f.close()

  #utf-8の文書データを取得
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
  
  #文書データをスクリーニングし、文章部分だけを取得
  text, title = extractor.as_text()
  #f.write(text)
  #f.write(title)
  #print("texttype:%s" % type(text))
  print("title:%s\n\ntext:" % (title))

  #文章データを改行で分割
  text = text.splitlines()
  lines = []
  #文章データを「。」で分割
  for line in text:
    lines.extend(line.split("。"))
  #良く分からない空白を削除
  while (True):
    try:
      lines.remove("")
    except:                                              
      break

  #興味キーワードが存在
  if keyword_num > 0:
    #興味キーワード群を分割
    for num in range(keyword_num):
      #文章群から文章を抽出
      for line in lines:
        #興味キーワードが含まれている文章
        if keyword[num] in line:
          print("\n本文:")
          print("%s:%s\n" % (keyword[num], line))
          #sentencesテーブルに文章と興味キーワードが無い時、
          #文章と興味キーワードの組み合わせをsentencesテーブルに保存し、
          #レコードのidを保存
          sentences = insertSentences(line, keyword[num], connector, cursor)

          #レコードのidを分割
          for k in sentences:
            id = k[0]

          #文章と興味キーワードの係り受け解析を実行
          leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes = analysiser.ReceivedObj(line, keyword[num])
          #print("leadID:%s" % leadID)
          #print("keywordID:%s" % keywordID)
          #print("%s" % chunkdic)

          #生成法則の番号（14）を保存
          lawNumber = "14"

          #文章に生成法則14を実行し、文章を改変
          upSentencedic = analysiser.stepFourteen(leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)

          #sentencesテーブルに文章と興味キーワードの挿入が成功
          if id is not '':
            #生成法則14で改変された文章を分割
            for upSentence in upSentencedic:
              print(upSentence)
              print(index)
              #解析した文章と生成された文章(upSentence)をprogramLawsテーブルに保存
              index_p = insertProgramLaws(str(id), upSentence, lawNumber, connector, cursor, index, answerData[index], fp)
              #answerDataの添字を更新
              index = index_p
          id = ''
          #解析した文章の総数
          all += 1
  #興味キーワードが未存在
  else:
    #Webページから取得した文章を全表示
    for line in lines:
      print("\n本文:")
      print("%s\n" % line)
      #Webページから取得した文章の総数
      all += 1
  #html, title = extractor.as_html()
  #print("html:%s\ntitle:%s" % (html, title))
  #print("%s" % (type(title)))
  
  #f.write(html)
  #f.write(title)
  
  title = extractor.extract_title(file)
  print("title:%s" % title)
  
  #f.write(title)
  #f.close()
cursor.close
connector.close
fp.close

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print("Sample_num:%s" % all)
