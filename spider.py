#coding=utf8

from pyquery import PyQuery
import urllib
import socket
import extract

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

socket.setdefaulttimeout(5)

class URL:
    def __init__(self, url, title = '', content = '', paragraphy = '', sentence = ''):
        self.url = url
        self.title = title
        self.content = content
        self.paragraphy = paragraphy
        self.sentence = sentence

class Retrieve:
    def __init__(self, query='\t', pn = 10):
        self.query_id = query.split('\t')[0]
        self.query_str = query.split('\t')[1]
        self.pn = pn
        self.seg = {}
        self.url_list =  []

        self.get_wd_seg_list()

    def get_content_from_query(self):
        query = 'http://www.baidu.com/s?wd=' + self.query_str + '&ie=utf-8'
        for i in range(self.pn):
            try:
                page = PyQuery(query + '&pn=' + str(i * 10))
                self.analysis_query(page, i)
            except Exception,e:
                log(str(e), 'ERROR')
                sys.exit(1)

    def analysis_query(self, page, num):
        for i in range(10):
            print num*10+i+1
            link = page('div').filter('#' + str(num*10+i+1)).find('h3').find('a').attr('href')
            if (link == None):
                link = page('div').filter('#' + str(num*10+i+1)).attr('mu')
            if('image.baidu.com' in link):
                continue
            try:
                title,content = self.get_title_content(link)
            except Exception,e:
                log(str(e), link)
                title = ''
                content = ''
            url = URL(link, title, content)
            self.url_list.append(url)
    
    def get_title_content(self, link):
        f = urllib.urlopen(link)
        cont = f.read()
        p = PyQuery(cont)
        title = p('head').find('title').text()
        content =  extract.run(cont)
        #print type(content).__name__
        f.close()
        return title, content

    def get_wd_seg_list(self):
        url_qz = 'http://10.48.16.44:8080/wordseg/'
        url_final = url_qz + self.query_str
        try:
            a = urllib.urlopen(url_final)
            cont = a.read()
            cont_list = cont.split('\n')
            phrase_res = cont_list[0]
            basic_res = cont_list[1]
            
            self.seg['phrase'] = phrase_res
            self.seg['basic'] = basic_res
        except Exception,e:
            log(str(e), "FATAL")
            sys.exit(1)

    def printResult(self):
        for i in self.url_list:
            print i.url
            print i.title 
            print i.content == ""
        print self.seg

    def saveToFile(self,filename):
        f = open(filename, 'a')
        f.write('query:' + self.query_str + '\n')
        f.write('phrase_seg:' + self.seg['phrase'] + '\n')
        f.write('basic_seg:' + self.seg['basic'] + '\n')
        f.write('query_result:' + str(len(self.url_list)) + '\n')
        for i in range(len(self.url_list)):
            f.write('url:' + self.url_list[i].url + '\n')
            f.write('title:' + self.url_list[i].title.encode('utf-8') + '\n')
            #print self.url_list[i].content
            try:
                f.write('content:' + self.url_list[i].content.encode('utf-8') + '\n')
            except:
                f.write('content:' + self.url_list[i].content.decode('gbk').encode('utf-8'))
        f.close()
    
def log(msg,msg_type):
    print>>sys.stderr,msg_type+"_chenjianfeng:"+msg

if __name__ == "__main__":
    r = Retrieve('10\t刘德华的妻子是谁', 20)
    r.get_content_from_query()
    #r.printResult()
    r.saveToFile('result.txt')
