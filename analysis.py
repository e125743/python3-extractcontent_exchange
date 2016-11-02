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
                    chunkText += tok.text
                    chunkdic.setdefault(int(linkchunk.attrib['id']), {})[int('{tok.attrib[id]}'.format(**locals()))] = [tok.attrib['feature'], tok.text]
                    TokenGroupes.setdefault(int(linkchunk.attrib['id']), []).append(int('{tok.attrib[id]}'.format(**locals())))
                    #print("text:%s" % tok.text)
                    #print("id:%s" % tok.attrib['id'])

                    if chunkText.endswith(keyword.replace(" ","")) is True:
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

            #print("%s" % chunkdic)

        #print("leadID:%s" % leadID)
        #print("%s" % chunkdic)
        #print("TokenGroupes:%s" % TokenGroupes)
        return (leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes)



    def setEndToken(chunkid, chunkdic):
        endtokenid = 0
        sentenceEnd = 0
        alltext = ""
        endflag = 0
        basicflag = 0
        for id,text in sorted(chunkdic[chunkid].items()):
          if isinstance(text, list):
            alltext += text[1]
            sentenceEnd = id
            #print("%s" % type(text))
            #print("%s" % alltext)
            print("%s" % text[1])


            if "動詞" in text[0] and "自立" in text[0] and "非自立" not in text[0] and endflag == 0 and basicflag == 0:
              endflag = 1
              print("自立a%s" % endflag)
            elif ("助動詞" or "助詞" or "動詞" in text[0]) and endflag == 1 and basicflag == 0:
              endflag = 1
              print("自立b%s" % endflag)
            else:
              endflag = 0
              print("自立%s" % endflag)

            if "基本形" in text[0]:
              basicflag = 1
              print("基本形")

            if endflag == 1:
              print("endtoken:%s" % alltext)
              print("%s" % endflag)
              endtokenid = id
            elif alltext.endswith("だ") is True:
              print("endtoken:%s" % alltext)
              endtokenid = id
            elif alltext.endswith("である") is True:
              print("endtoken:%s" % alltext)
              endtokenid = id
        
        return (endtokenid, sentenceEnd)



    def stepFourteen(self, leadID, chunkdic, keychunkID, keytokenID, RelateGroupes, TokenGroupes):
        #print("leadID:%s" % leadID)

        """
        for chunkid, tokens in sorted(chunkdic.items()):
          print("%s " % chunkid, "%s" % tokens)
          for tokenid, token in sorted(tokens.items()):
            print("%s " % tokenid, "%s" % token)
        """

        print("chunkdic:%s" % chunkdic)
        print("RelateGroupes:%s" % RelateGroupes)
        print("TokenGroupes:%s" % TokenGroupes)
        print("keychunkID:%s" % keychunkID)
        print("keytokenID:%s" % keytokenID)

        i = 0
        for id in keychunkID:
          print("keychunkID:%s" % id)
          keychunk = chunkdic[id]
          keytokenEnd = TokenGroupes[id][-1]
          keytokenFirst = TokenGroupes[id][0]

          try:
            keyrear = keychunk[int(keytokenID[i]) + 1]
          except:
            if keychunk[int(sys.maxsize)] == -1:
              print("%s" % keychunk[int(sys.maxsize)])
              keyrear = []

            else:
              keychunk = chunkdic[int(id) + 1]
              keyrear = keychunk[int(keytokenID[i]) + 1]

          print("keyrear:%s" % keyrear)

          if len(keyrear) != 0:
            endtokenid = 0
            if keyrear[1] == 'の':
              print("Yes:%s" % keyrear[1])

              for Groupe in RelateGroupes:
                if id in Groupe:
                  print("endchunk:%s" % chunkdic[Groupe[-1]])
                  print("%s" % Groupe)

                  #rearGroupe = list(filter((lambda x: x > id), Groupe))
                  #rearGroupe_set = set(rearGroupe)
                  #print("rearGroupe:%s" % rearGroupe)
                  #endtokenid = 0

                  for groupeid in range(1, len(Groupe)):
                    if Groupe[groupeid] - Groupe[groupeid - 1] > 1 and Groupe[groupeid] > id and endtokenid == 0:
                      print("%s" % int(Groupe[groupeid] - Groupe[groupeid - 1]))
                      lastid = Groupe[groupeid]
                      beginid = Groupe[groupeid - 1]

                      rearLast = []
                      for RelateGroupe in RelateGroupes:
                        #RelateGroupe_set = set(RelateGroupe)
                        #matching = list(RelateGroupe_set & rearGroupe_set)
                        rearLast.extend(list(filter((lambda x: beginid < x < lastid), RelateGroupe)))

                      print("%s" % sorted(set(rearLast), reverse=True))
                      for chunkid in sorted(set(rearLast), reverse=True):
                        if endtokenid == 0:
                          endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                          print("%s" % endtokenid)
                        else:
                          print("endtokenid:%s" % endtokenid)
                          print("sentenceEnd:%s" % sentenceEnd)
                          break

                  if endtokenid == 0:
                    for Groupe in RelateGroupes:
                      if id in Groupe:
                        for chunkid in sorted(Groupe, reverse=True):
                          if endtokenid == 0:
                            endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
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


            else:
              print("not:%s" % keyrear[1])

              #endtokenid = 0
              for Groupe in RelateGroupes:
                if id in Groupe:
                  print("endchunk:%s" % chunkdic[Groupe[-1]])
                  print("%s" % Groupe)

                  for chunkid in sorted(Groupe, reverse=True):
                    if endtokenid == 0:
                      endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                    else:
                      print("endtokenid:%s" % endtokenid)
                      print("sentenceEnd:%s" % sentenceEnd)
                      break

              if endtokenid == 0:
                for Groupe in RelateGroupes:
                  if id not in Groupe:

                    for chunkid in sorted(Groupe, reverse=True):
                      if endtokenid == 0:
                         endtokenid,sentenceEnd=AnalysisContent.setEndToken(chunkid, chunkdic)
                      else:
                        print("endtokenid:%s" % endtokenid)
                        print("sentenceEnd:%s" % sentenceEnd)
                        break

            if endtokenid != 0:
              upToken = {}
              print("%s" % chunkdic)
              print("keytokenEnd:%s" % keytokenEnd)
              print("keytokenFirst:%s" % keytokenFirst)
              for chunk in chunkdic.values():
                #print("%s" % chunk)
                for tokenid in chunk.keys():
                  print("token:%s" % chunk[tokenid])

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
                    """
                    elif keytokenID[i] < tokenid <= keytokenEnd or endtokenid < tokenid:
                      break
                    else:
                      setid = tokenid + keychunkID[i] - keytokenEnd
                    """
                    

                    upToken[setid] = chunk[tokenid][1]

              print("upToken:%s" % upToken)
              #print("upToken:%s" % sorted(upToken.items()))

              upSentence = ''
              for key in sorted(upToken.keys()):
                upSentence += upToken[key]
              print("upSentence:%s" % upSentence)
            
          i += 1
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
