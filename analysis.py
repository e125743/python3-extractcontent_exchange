# coding=utf-8
import sys
import CaboCha
import xml.etree.ElementTree as ET

class AnalysisContent(object):

    def ReceivedObj(self, sentence, keyword):
        c = CaboCha.Parser()
        tree =  c.parse(sentence)
        print("%s" % tree.toString(CaboCha.FORMAT_TREE)) #簡易 Tree 表示での出力
        print("%s" % tree.toString(CaboCha.FORMAT_LATTICE)) #計算機に処理しやすいフォーマットで出力
        #文章の係り受けデータ群
        sent = ET.fromstring(tree.toString(CaboCha.FORMAT_XML))

        #興味キーワードのchunkID
        keychunkID = []
        #興味キーワードのtokenID
        keytokenID = []
        #係り受けの先頭のchunkID
        leadID = []
        #chunkの辞書
        chunkdic = {}
        #解析済みのchunkID
        AlreadyID = []
        #chunk内の全てのtokenID群
        TokenGroupes = {}
        #同じ係り受け関係のchunkID群
        RelateGroupes = []

        #chunkを文章の初めから解析
        for chunk in sent.findall('.//chunk'):
          #print("--元の文データ")
          #print("%s" % sent.findall(".//chunk[@id='0']"))
          #print("--一文")

          #print("--chunkID")
          #print("%s" % chunk.attrib['id'])
          #print("--一節")

          #解析済みのchunkIDは省略
          if chunk.attrib['id'] not in AlreadyID:
            #係り受けの先頭のchunkIDを保存
            leadID.append(chunk.attrib['id'])
            #chunkidを保存
            linkid = int(chunk.attrib['id'])

            #係り受けの関係にあるchunkIDを保存
            RelateID = []
            while True:
              #解析するchunkを取得
              linkchunk = sent.find(".//chunk[@id='{linkid}']".format(**locals()))
              #係り受けの解析が完了
              if linkid == '-1':
                #解析済みの係り受け関係のchunkIDの一群を保存
                RelateGroupes.append(RelateID)
                #print("listed!")
                #print("RelateGroupes:%s" % RelateGroupes)

              #係り受けの解析が未完了
              else:
                #同じ係り受けの関係にあるchunkIDを保存
                RelateID.append(int(linkid))
                #print("appendet!")
                #print("RelateID:%s" % RelateID)

              #解析するchunkが存在
              if linkchunk != None:

                #解析するchunkがまだ未解析
                if linkchunk.attrib['id'] not in AlreadyID:
                  #chunkの文を保存
                  chunkText = ""
                  #解析済みのchunkIDを保存
                  AlreadyID.append(linkchunk.attrib['id'])

                  #解析するchunkをtokenに分割
                  for tok in linkchunk:
                    #tokenの文を結合
                    chunkText += tok.text

                    #キー：chunkID
                    #値：chunk内の全てのtokenの{tokenID: [単語情報, 単語]}の群
                    #上記の構造で辞書作成
                    chunkdic.setdefault(int(linkchunk.attrib['id']), {})[int('{tok.attrib[id]}'.format(**locals()))] = [tok.attrib['feature'], tok.text]

                    #キー：chunkID
                    #値：chunk内のtokenID
                    TokenGroupes.setdefault(int(linkchunk.attrib['id']), []).append(int('{tok.attrib[id]}'.format(**locals())))
                    #print("text:%s" % tok.text)
                    #print("id:%s" % tok.attrib['id'])

                    #chunkの文中に興味キーワードが存在
                    if chunkText.endswith(keyword.replace(" ","")) is True:
                      #興味キーワードがあるchunkIDを保存
                      keychunkID.append(int(linkchunk.attrib['id']))
                      #興味キーワードのtokenIDを保存
                      #興味キーワードが連なる場合、一番後ろのtokenIDを保存
                      keytokenID.append(int(tok.attrib['id']))

                  #値の最後は{int型の最大値: 係り受け先のchunkID}
                  chunkdic.setdefault(int(linkchunk.attrib['id']), {})[int(sys.maxsize)] = int(linkchunk.attrib['link'])

                  #for id,text in sorted(chunkdic[int(linkchunk.attrib['id'])].items()):
                    #print("chunk:" + str(id) + "," + str(text))

                #解析したchunkの係り受け先のchunkIDを保存
                linkid = linkchunk.attrib['link']
                #print("linkid:%s" % linkid)
                #print("keywordID:%s" % keywordID)
                
              #解析するchunkが空（linkidが-1で係り受けの終りを表示）
              else:
                #係り受け解析終了
                break

            #print("%s" % chunkdic)

        #print("leadID:%s" % leadID)
        #print("%s" % chunkdic)
        #print("TokenGroupes:%s" % TokenGroupes)

        return (leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)


    #興味キーワードの係り受け先の終点を解析
    def setEndToken(chunkid, chunkdic):
        endtokenid = 0
        sentenceEnd = 0
        alltext = ""
        endflag = 0
        basicflag = 0
        continuous = 0
        #興味キーワードが存在するchunk内のtokenを分割
        for id,text in sorted(chunkdic[chunkid].items()):
          #tokenの単語情報が存在
          if isinstance(text, list):
            #tokenの単語を統合
            alltext += text[1]
            #tokenIDを保存
            sentenceEnd = id
            #print("%s" % type(text))
            #print("%s" % alltext)
            print("%s" % text[1])

            #単語が連用形以外の自立語の動詞であり、
            #endflagとbasicflagが0の時、endflagに1を保存
            if "動詞" in text[0] and "自立" in text[0] and endflag == 0 and basicflag == 0 and "連用形" not in text[0]:# or ("助動詞" in text[0] and "基本形" in text[0]): and "基本形" in text[0]: and "非自立" not in text[0]
              endflag = 1
              print("自立a%s" % endflag)

            #一つ前の単語が、連用形、基本形以外の自立語の動詞である時、
            #その後の単語が助動詞、助詞のいづれかだったら、endflagは1を保持
            #単語が、連用形以外の自立語の動詞である場合も1を保持
            elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:# and "基本形" in text[0]:
              endflag = 1
              print("自立b%s" % endflag)
            #それ以外
            else:
              endflag = 0
              print("自立%s" % endflag)

            #単語が基本形の場合、basicflagに1を保存
            if "基本形" in text[0]:
              basicflag = 1
              print("基本形")

            #continuousが0の時、単語が連用形の自立だったら、continuousに1を保存
            if continuous == 0 and "連用形" in text[0] and "自立" in text[0] and "非自立" not in text[0]:
              continuous = 1
            #一つ前の単語が連用形の自立で、
            #その後の単語が基本形だったら、endflagに1を保存
            elif continuous == 1 and "基本形" in text[0]:
              endflag = 1
            #それ以外
            else:
              continuous = 0

            #endflagが1の時、そのtokenを興味キーワードの係り受け先の終点に決定
            if endflag == 1:
              print("endtoken:%s" % alltext)
              print("%s" % endflag)
              endtokenid = id

            #単語が「だ」、「である」時、
            #そのtokenを興味キーワードの係り受け先の終点に決定
            elif alltext.endswith("だ") is True:
              print("endtoken:%s" % alltext)
              endtokenid = id
            elif alltext.endswith("である") is True:
              print("endtoken:%s" % alltext)
              endtokenid = id

        #係り受け先の終点になる単語のまとめ
        #1.基本形の自立語の動詞
        #2.連用形以外の自立語の動詞の後の助詞、助動詞
        #3.連用形の自立語の後の基本形の動詞
        #4.単語「だ」と「である」
        return (endtokenid, sentenceEnd)



    def stepFourteen(self, leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes):
        #print("leadID:%s" % leadID)

        """
        for chunkid, tokens in sorted(chunkdic.items()):
          print("%s " % chunkid, "%s" % tokens)
          for tokenid, token in sorted(tokens.items()):
            print("%s " % tokenid, "%s" % token)
        """

        #渡されたデータの確認
        print("chunkdic:%s" % chunkdic)
        print("RelateGroupes:%s" % RelateGroupes)
        print("TokenGroupes:%s" % TokenGroupes)
        print("keychunkID:%s" % keychunkID)
        print("keytokenID:%s" % keytokenID)

        #法則14により生成された文
        upSentencedic = []
        i = 0
        #興味キーワードのchunkIDを取得
        for id in keychunkID:
          print("keychunkID:%s" % id)
          #興味キーワードが含まれているchunkを取得
          keychunk = chunkdic[id]
          #興味キーワードが含まれているchunkの最後のtokenIDを取得
          keytokenEnd = TokenGroupes[id][-1]
          #興味キーワードが含まれているchunkの最初のtokenIDを取得
          keytokenFirst = TokenGroupes[id][0]

          #chunk内の興味キーワードの直後のtokenを取得成功
          try:
            keyrear = keychunk[int(keytokenID[i]) + 1]

          #chunk内の興味キーワードの直後のtokenを取得失敗
          #chunkの最後が興味キーワード
          except:

            #興味キーワードを含むchunkが文末
            if keychunk[int(sys.maxsize)] == -1:
              #print("%s" % keychunk[int(sys.maxsize)])

              #興味キーワードの後ろが空
              keyrear = []

            #興味キーワードを含むchunkが文中
            else:
              #興味キーワードを含むchunkの後ろのchunkを取得
              keychunk = chunkdic[int(id) + 1]
              #興味キーワードの後ろのtokenを取得
              keyrear = keychunk[int(keytokenID[i]) + 1]

          print("keyrear:%s" % keyrear)

          #興味キーワードの後ろのtokenが存在
          if len(keyrear) != 0:

            endtokenid = 0
            #興味キーワードの後ろが「の」
            if keyrear[1] == 'の':
              print("Yes:%s" % keyrear[1])

              #係り受け関係にあるchunkID群を分割
              for Groupe in RelateGroupes:
                #係り受け関係のchunk内に興味キーワードが存在
                if id in Groupe:
                  print("endchunk:%s" % chunkdic[Groupe[-1]])
                  print("%s" % Groupe)

                  #rearGroupe = list(filter((lambda x: x > id), Groupe))
                  #rearGroupe_set = set(rearGroupe)
                  #print("rearGroupe:%s" % rearGroupe)
                  #endtokenid = 0

                  #係り受け関係のchunk間に別のchunkがある場合を処理
                  #係り受け関係のchunkIDを分割
                  for groupeid in range(1, len(Groupe)):

                    #興味キーワードの係り受け先の終点が未決定の時、
                    #興味キーワードの後ろにあるchunkで、
                    #係り受け関係のchunk間に別のchunkが存在
                    if Groupe[groupeid] - Groupe[groupeid - 1] > 1 and Groupe[groupeid] > id and endtokenid == 0:
                      print("%s" % int(Groupe[groupeid] - Groupe[groupeid - 1]))
                      #係り受け関係間に別のchunkがあるchunkidの後ろを保存
                      lastid = Groupe[groupeid]
                      #係り受け関係間に別のchunkがあるchunkidの前を保存
                      beginid = Groupe[groupeid - 1]

                      rearLast = []
                      #係り受け関係にあるchunkID群を分割
                      for RelateGroupe in RelateGroupes:
                        #RelateGroupe_set = set(RelateGroupe)
                        #matching = list(RelateGroupe_set & rearGroupe_set)

                        #係り受け関係の間にあるchunkIDを取得
                        rearLast.extend(list(filter((lambda x: beginid < x < lastid), RelateGroupe)))

                      print("%s" % sorted(set(rearLast), reverse=True))

                      #係り受け関係の間にあるchunkIDを逆順で分割
                      for chunkid in sorted(set(rearLast), reverse=True):

                        #興味キーワードの係り受け先の終点が未決定
                        if endtokenid == 0:
                          #興味キーワードの係り受け先の終点を決定
                          endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                          print("%s" % endtokenid)
                        #興味キーワードの係り受け先の終点が存在
                        else:
                          print("endtokenid:%s" % endtokenid)
                          print("sentenceEnd:%s" % sentenceEnd)
                          break

                  #係り受け関係のchunkが連続している場合を処理
                  #興味キーワードの係り受け先の終点が未決定
                  if endtokenid == 0:
                    #係り受け関係にあるchunkID群を分割
                    for Groupe in RelateGroupes:
                      #係り受け関係のchunk内に興味キーワードが存在
                      if id in Groupe:
                        #係り受け関係のchunkIDを逆順で分割
                        for chunkid in sorted(Groupe, reverse=True):
                          #興味キーワードの係り受け先の終点が未決定
                          if endtokenid == 0:
                            #興味キーワードの係り受け先の終点を決定
                            endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                          #興味キーワードの係り受け先の終点が存在
                          else:
                            print("endtokenid:%s" % endtokenid)
                            print("sentenceEnd:%s" % sentenceEnd)
                            break
                    """
                    if len(matching) > 0 and Groupe != RelateGroupe:
                      matching_set = set(matching)
                      print("matchingGroupe:%s" % matching)
                      RelateGroupe = list(RelateGroupe_set - matching_set)
                      print("RelateGroupe:%s" % RelateGroupe)
                      #headGroupe = list(rearGroupe_set - matching_set)
                      #print("headGroupe:%s" % headGroupe)
                    """

            #興味キーワードの後ろが「の」以外
            else:
              print("not:%s" % keyrear[1])
              #endtokenid = 0

              #興味キーワードが存在するchunkと、
              #係り受け関係にあるchunk群の中に興味キーワードを、
              #主体とする動詞の終止形がある場合を処理
              #係り受け関係にあるchunkID群を分割
              for Groupe in RelateGroupes:
                #係り受け関係のchunk内に興味キーワードが存在
                if id in Groupe:
                  print("endchunk:%s" % chunkdic[Groupe[-1]])
                  print("%s" % Groupe)

                  #係り受け関係のchunkIDを分割
                  for chunkid in sorted(Groupe):#, reverse=True):
                    #興味キーワードが存在するchunkより後ろのchunk
                    if chunkid >= id:
                      #興味キーワードの係り受け先の終点が未決定
                      if endtokenid == 0:
                        #興味キーワードの係り受け先の終点を決定
                        endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                      #興味キーワードの係り受け先の終点が存在
                      else:
                        print("endtokenid:%s" % endtokenid)
                        print("sentenceEnd:%s" % sentenceEnd)
                        break

              #興味キーワードが存在するchunkと、
              #係り受け関係にあるchunk群の中に興味キーワードを、
              #主体とする動詞の終止形が無い場合を処理
              #興味キーワードの係り受け先の終点が未決定
              if endtokenid == 0:
                #係り受け関係にあるchunkID群を分割
                for Groupe in RelateGroupes:
                  #興味キーワードが存在しない係り受け関係のchunk
                  if id not in Groupe:

                    #係り受け関係のchunkIDを逆順に分割
                    for chunkid in sorted(Groupe, reverse=True):
                      #興味キーワードの係り受け先の終点が未決定
                      if endtokenid == 0:
                         #興味キーワードの係り受け先の終点を決定
                         endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                      #興味キーワードの係り受け先の終点が存在
                      else:
                        print("endtokenid:%s" % endtokenid)
                        print("sentenceEnd:%s" % sentenceEnd)
                        break

            #興味キーワードを係り受け先の終点の後ろに移動させる処理
            #興味キーワードの係り受け先の終点が存在
            if endtokenid != 0:
              upToken = {}
              print("%s" % chunkdic)
              print("keytokenEnd:%s" % keytokenEnd)
              print("keytokenFirst:%s" % keytokenFirst)

              #chunk内のtokenデータの取得
              for chunk in chunkdic.values():
                #print("%s" % chunk)

                #tokenIDを分割
                for tokenid in chunk.keys():
                  print("token:%s" % chunk[tokenid])

                  #tokenデータに単語情報と単語が存在
                  if isinstance(chunk[tokenid], list) is True:

                    #興味キーワードの係り受け先の終点
                    if tokenid == endtokenid:
                      #興味キーワードの係り受け先の終点が「だ」
                      if chunk[tokenid][1].endswith("だ") is True:
                        #「だ」を「である」に変更
                        chunk[tokenid][1] = "である"

                    #興味キーワードの係り受け先の終点から興味キーワードの間の
                    #tokenIDを移動する興味キーワードのtoken数だけ減少
                    if keytokenEnd < tokenid <= int(endtokenid):
                      setid = tokenid + keytokenFirst - keytokenEnd - 1
                    #移動する興味キーワードのtokenIDを
                    #興味キーワードの係り受け先の終点の後ろに調整
                    elif keytokenFirst <= tokenid <= keytokenID[i]:
                      setid = endtokenid + tokenid - keytokenEnd
                    #興味キーワードより前のtokenIDは同値
                    elif tokenid < keytokenFirst:
                      setid = tokenid
                    #興味キーワードの係り受け先の終点より後ろは削除
                    else:
                      continue
                    """
                    elif keytokenID[i] < tokenid <= keytokenEnd or endtokenid < tokenid:
                      break
                    else:
                      setid = tokenid + keychunkID[i] - keytokenEnd
                    """
                    
                    #書き換えた順番でtokenを保存
                    upToken[setid] = chunk[tokenid][1]

              print("upToken:%s" % upToken)
              #print("upToken:%s" % sorted(upToken.items()))

              #書き換えた文章を生成
              upSentence = ''
              for key in sorted(upToken.keys()):
                upSentence += upToken[key]
              print("upSentence:%s" % upSentence)
              #書き換えた文章を保存
              upSentencedic.append(upSentence)

          i += 1
        return upSentencedic
        """
        for id in keychunkID:
          print("keywordChunk:%s" % chunkdic[id])

          while True:
            try:
              chunk = chunkdic[id]
              print("%s" % chunk)
              for tokenid, token in sorted(chunk.items()):

                if isinstance(token, list):

                  #if '名詞' in token[0]:
                  print("%s " % tokenid, "%s" % token)

                else:
                  id = token
                  break

            except:
              
              break
        """
