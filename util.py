#coding=utf-8
#__author__=chenjianfeng03@baidu.com

import re
def rm_tag(html):
    f = open('tmp.txt', 'w')
    s = ""
    r = re.compile('(?is)<body.*?>.*?</body>', re.M)
    m = r.search(html)
    #m = re.match(r, html)
    if(m):
        s = m.group()
    s = re.sub(r'(?is)<script.*?>.*?</script>', '', s)
    s = re.sub(r'(?is)<style.*?>.*?</style>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)
    s = re.sub(r'<(S*?)[^>]*>.*?|<.*? />', '', s)
    s = s.replace('\t', '')
    s = s.replace(' ', '')
    s = s.replace('/^m', '')
    print 'success'
    #s = re.sub(r'(<[^<>]+)\s*\n\s*','', s)
    l = s.split('\n')
    print len(l)
    for i in l: 
        if i.strip():
            if len(i) > 6:
                f.write(i.strip() + '\n')
    f.close()

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

if __name__ == "__main__":
    import urllib
    c = urllib.urlopen('http://tech.163.com/13/1230/10/9HB88VE600094NRG.html')
    html = c.read()
    #rm_tag(html)
    get_para(html)
