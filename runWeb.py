#coding=utf-8
__author__='chenjianfeng03@baidu.com'

from spider import Retrieve
from socring import Socring
import bottle
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

bottle.TEMPLATE_PATH.insert(0, 'views')

s = Socring()

@bottle.get('/')
def index():
    return bottle.template("index.html")
@bottle.post('/')
def main():
    queryStr = bottle.request.forms.get('input_query', None)
    pn = int(bottle.request.forms.get('page_num', 1))
    type = bottle.request.forms.get('s_type', None)
    size = int(bottle.request.forms.get('w_size', None))

    r = Retrieve(queryStr, pn)
    r.get_content_from_query()
    r.saveToFile('result.txt')

    
    socreDic = s.socre(r, type, 'para', size)
    list = sorted(socreDic.iteritems(), key = lambda x:x[1], reverse = True)
    resultPara = ""
    for i in list:
        resultPara += str(i[1]) + '\t' + i[0] + '\n'
    
    socreDic = s.socre(r, type, 'sentence', size)
    list = sorted(socreDic.iteritems(), key = lambda x:x[1], reverse = True)
    resultSentence = ""
    for i in list:
        resultSentence += str(i[1]) + '\t' + i[0] + '\n'
    a=bottle.template('index.html',query=queryStr,page=pn,type=type,size=size,para_evi=resultPara,sen_evi=resultSentence)
    return a

bottle.run(host='10.94.157.59',port=8686)
