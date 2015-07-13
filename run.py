#coding=utf-8
#__coding__=chenjianfeng03@baidu.com

from spider import Retrieve
from socring import Socring

def run(queryStr, pn = 10):
    print "start retrieve..."
    r = Retrieve(queryStr, pn)
    r.get_content_from_query()
    r.saveToFile('result.txt')
    print "end retrieve..."
    print "start socring..."
    s = Socring()
    s.socre(r, 'tf-idf', 'para')
    s.saveToFile()
    print "end socring..."

if __name__ == "__main__":
    run("10\t刘德华的老婆是谁", 1)
