#coding=utf-8
#__author__=chenjianfeng03@baidu.com

import re
import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def rm_tag(html):
    f = open('temp.txt', 'w')
    s = ""
    r = re.compile('(?is)<body.*?>.*?</body>', re.M)
    m = r.search(html)
    if(m):
        s = m.group()
    s = s.replace('<br />', '\n')
    s = re.sub(r'(?is)<script.*?>.*?</script>', '', s)
    s = re.sub(r'(?is)<style.*?>.*?</style>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)
    s = re.sub(r'<(S*?)[^>]*>.*?|<.*? />', '', s)
    s = s.replace('\t', '')
    s = s.replace(' ', '')
    s = s.replace('/^m', '')
    #s = re.sub(r'(<[^<>]+)\s*\n\s*','', s)
    l = s.split('\n')
    #print len(l)
    for i in l: 
        if i.strip():
            if len(i) > 6:
                f.write(i.strip() + '\n')
    f.close()
    return s

def get_para(html):
    f = open('tmp.txt', 'w')
    r = re.compile('(?is)<p.*?>.*?</p>', re.M)
    s = "\n".join(re.findall(r, html))
    s = re.sub(r'(?is)<script.*?>.*?</script>', '', s)
    s = re.sub(r'(?is)<style.*?>.*?</style>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)
    s = re.sub(r'(?is)<a.*?>.*?</a>', '', s)
    s = re.sub(r'<(S*?)[^>]*>.*?|<.*? />', '', s)
    s = s.replace('\t', '')
    s = s.replace(' ', '')
    s = s.replace('/^M', '')
    m = s.split('\n')
    for i in m:
        if(i.strip()):
            f.write(i.strip() + '\n')
    f.close()

def filter_content(s):
    #f = open('content.txt', 'w')
    para_list = s.split('\n')
    content = ''
    avg = len(s)/len(para_list)
    if(avg < 70):
        avg = 70
    if(avg > 100):
        avg = 80
    for i in range(len(para_list)):
        if len(para_list[i].strip()) > avg:
            content += para_list[i] + '\n'
            #f.write(para_list[i].strip() + '\n')
    #f.close()
    return content

def run(html):
    s = rm_tag(html)
    return filter_content(s)


if __name__ == "__main__":
    c = urllib.urlopen('http://www.baidu.com/link?url=5XI8pKnj-kOmmwvZqMn86mBl1-S21UUFrm-3TSmG-5u9Xrd-MJSvhi6agfzwJTFxh8HOIsnq_0f-JaagfWhsIq')
    html = c.read()
    result = run(html)
    print type(result).__name__
    f = open('tmp.txt', 'w')
    f.write(result + '\n')
    f.close()
