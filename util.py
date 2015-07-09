#coding=utf-8
#__author__=chenjianfeng03@baidu.com

import re
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
    f = open('a.txt', 'w')
    para_list = s.split('\n')
    avg = len(s)/len(para_list)
    if(avg < 40):
        avg = 40
    if(avg > 80):
        avg = 60
    for i in range(len(para_list)):
        if len(para_list[i]) > avg:
            f.write(para_list[i].strip() + '\n')
    f.close()

if __name__ == "__main__":
    import urllib
    c = urllib.urlopen('http://www.baidu.com/link?url=6q4fFojUjtgatTFIzAhn9iD-YeBMDSVrmhw40yYPPRA4qQooxKkQ-lmi4hMrTcg3AwDETiz70ezHBDkClYh0ba')
    html = c.read()
    s = rm_tag(html)
    filter_content(s)
    #get_para(html)
