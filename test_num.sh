#!/bin/sh


> resultTest_num.txt
thread_num=1
while [ $thread_num -le 8 ]
do

count=1
allTime=0.0
while [ $count -le 100 ]
do
time=`python3.5 WebResource.py ${thread_num} http://www.itmedia.co.jp/mobile/articles/1509/10/news166.html http://www.itmedia.co.jp/mobile/articles/1509/10/news166_2.html http://www.itmedia.co.jp/mobile/articles/1509/10/news166_3.html | tail -n2 | head -n1 | cut -f2 -d":" | cut -f1 -d"["`
allTime=`echo "scale=19; ${allTime} + ${time} / 100" | bc`
count=`expr ${count} + 1`
done
echo "${thread_num} ${allTime}" >> resultTest_num.txt


thread_num=`expr ${thread_num} + 1`
done
