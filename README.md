# python3-extractcontent_exchange

# Execution means
python3.5 WebResource.py "SubProcessNumber:int" "URL1:string" ... "URLn:string"  
example:  
python3.5 WebResource.py 4 http://www.itmedia.co.jp/mobile/articles/1509/10/news166.html http://www.itmedia.co.jp/mobile/articles/1509/10/news166_2.html http://www.itmedia.co.jp/mobile/articles/1509/10/news166_3.html

# Explain Source
* WebResource.py  
This is main source code.  
Accepts "int:SubProcessNumber" and "string:URL" as arguments.  
Calls modules,  
Extracts the document's groups from the resource of the web site,  
Divides the document's groups into sentence,  
Analyzes the sentence and implements inverse,  
And displays the result.

* extractcontent.py  
This souece code extracts the document's groups from the resource of the web site.

* analysis.py  
This souece code analyzes the sentence and implements inverse.

* test_num.sh  
This source code measures processing time of WebResource.py.  
Outputs "SubProcess:int ProcessingTime:float(by sec)" into resultTest_num.txt.
