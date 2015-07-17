# -*- coding=utf-8 -*-
import sys, os, codecs, re
 
reload(sys) 
sys.setdefaultencoding('utf-8')
 
import cProfile
import urllib2
 
re_title = re.compile(r'<title>(.*?)</title>', re.I|re.U|re.S)
re_body = re.compile(r'<body[^>]*>.*</body>', re.I|re.U|re.S)
re_doc_type = re.compile(r'<!DOCTYPE.*?>', re.I|re.U|re.S)
re_comment = re.compile(r'<!--.*?-->', re.I|re.U|re.S)
re_js = re.compile(r'<script.[^>]*>.*?</script>', re.I|re.U|re.S)
re_css = re.compile(r'<style[^>]*>.*?</style>', re.I|re.U|re.S)
re_special = re.compile(r'&.{2,8};|&#.{2,8};', re.I|re.U|re.S)
re_other = re.compile(r'<[^>]*>', re.I|re.U|re.S)
 
BLOCK_HEIGHT = 3
THRESHOLD = 90
 
class TextExtract(object):
    def __init__(self, new_html, join=True):
        self.html = new_html
        self.join = join
        self.text_start = 0
        self.text_end = 0
        self.text_body = ''
        self.block_len = []
        self.title = ''
        self.content = ''
         
        self.extract()
 
    def extract(self):
        self.extract_title()
        self.extract_body()
        self.remove_tags()
        self.extract_text()
     
    def extract_title(self):
        m = re_title.search(self.html)
        if m:
            self.title = m.group(1)
 
    def extract_body(self):
        m = re_body.search(self.html)
        if m:
            self.text_body = m.group()
 
    def remove_tags(self):
        self.text_body = re_doc_type.sub('', self.text_body)
        self.text_body = re_comment.sub('', self.text_body)
        self.text_body = re_js.sub('', self.text_body)
        self.text_body = re_css.sub('', self.text_body)
        self.text_body = re_special.sub('', self.text_body)
        self.text_body = re_other.sub('', self.text_body)
 
    def extract_text(self):
        lines = self.text_body.split('\n')
        line_len = len(lines)
        for i in xrange(0,line_len,1):
            lines[i] = re.sub(r'\s+', ' ', lines[i]).strip()
         
        for i in xrange(1,line_len-1,1):
            if len(lines[i]) > 0 and len(lines[i]) < 30 and 0 == len(lines[i-1]) and 0 == len(lines[i+1]):
                lines[i] = ''
 
        for i in xrange(0, len(lines)-BLOCK_HEIGHT, 1):
            line_len = 0
            for j in xrange(0, BLOCK_HEIGHT, 1):
                line_len += len(lines[i+j])
            self.block_len.append(line_len)
 
        self.text_start = self.find_text_start(0)
        self.text_end = 0
 
        if(0 == self.text_start):
            self.content = 'nothing can find'
        else:
            if self.join:
                line_lens = len(lines)
                while self.text_end < line_lens:
                    self.text_end = self.find_text_end(self.text_start)
                    self.content += self.get_text(lines)
                    self.text_start = self.find_text_start(self.text_end)
                    if 0 == self.text_start:
                        break
                    self.text_end = self.text_start
            else:
                self.text_end = self.find_text_end(self.text_start)
                self.content += self.get_text(lines)
 
    def find_text_start(self, index):
        blk_len = len(self.block_len)
        for i in xrange(index, blk_len-1, 1):
            if self.block_len[i] > THRESHOLD and self.block_len[i+1] > 0:
                return i
        return 0
 
    def find_text_end(self, index):
        blk_len = len(self.block_len)
        for i in xrange(index, blk_len-1, 1):
            if 0== self.block_len[i] and 0== self.block_len[i+1]:
                return i
        return blk_len-1
 
    def get_text(self, lines):
        str = ''
        for i in xrange(self.text_start, self.text_end, 1):
            str += lines[i]+'\n'
        return str

def run(content):
    try:
        #url = 'http://news.youth.cn/jy/201507/t20150717_6875451_2.htm'
        #proxied_request = urllib2.urlopen(url)
        #status_code = proxied_request.code
        #mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        #content = proxied_request.read()
        #encoding = proxied_request.headers['content-type'].split('charset=')[-1]
        #ucontent = unicode(content, encoding)
        text_extract = TextExtract(content)
        return text_extract.content
    except urllib2.HTTPError as e:
        print e
