# -*- coding: utf-8 -*-
import codecs

if __name__ == "__main__":
    fin  = codecs.open("read.txt","r","utf-8")
    fout_euc = codecs.open("euc_out.txt","w","euc_jp")
    fout_shift = codecs.open("utf-8.txt","w","shift_jis")

    for row in fin:
        fout_euc.write(row)
        fout_shift.write(row)
     
    fin.close()
    fout_euc.close()
    fout_shift.close()
