#coding=utf-8
#__author__=chenjianfeng03@baidu.com

import re

class Socring:
    def __init__(self, idf_file = 'baike_tf_idf_small.d'):
        self.idfDic = self.loadfile(idf_file)
        self.resultSocre = {}
        
    def loadfile(self,filename):
        f = open(filename)
        dic = {}
        for i in f:
            list = i.split('\t')
            dic[list[0].strip()] = float(list[2].strip())
        f.close()
        return dic

    def socre(self, query, method="tf-idf", segType = 'para', windows_size = 2):
        if(segType == 'para'):
            content_list = self.segPara(query)
        else:
            content_list = self.segSentence(query)
        if(method == 'tf-idf'):
            self.resultSocre = self.tf_idf_socre(query, content_list)
        elif (method == 'gram'):
            self.resultSocre = self.gram_socre(query, content_list, windows_size)
        elif(method == 'basic'):
            self.resultSocre = self.basic_socre(query, content_list, windows_size)
        else:
            pass

        return self.resultSocre

    def segPara(self, query):
        result = []
        for i in query.url_list:
            result.extend(i.content.split('\n'))
        return result

    def segSentence(self, query):
        result = []
        for i in query.url_list:
            s = ".".join(i.content.split('\n'))
            list = re.split('\.|\。', s)
            result.extend(list)
        return result

    def tf_idf_socre(self, query, content_list):
        socreDict = {}
        strDict = {}
        segQuery = query.seg['phrase']
        for i in content_list:
            socre = 0.0
            match = ""
            for j in segQuery.split(' '):
                if(j.strip() in i):
                    socre += self.idfDic[j]
                    match += j + "/" + str(self.idfDic[j]) + '\t'
            socreDict[match.strip()+ '\t' + i.strip()] = socre
        return socreDict
    
    def gram_socre(self, query, content_list, windows_size):
        socreDict = {}
        strDict = {}
        seglist = query.seg['phrase'].split(' ')
        print seglist
        searchList = []
        for i in range(len(seglist) - windows_size + 1):
            s = ""
            for j in range(windows_size):
                s += seglist[i+j]
            searchList.append(s)
        print searchList
        print len(searchList)
        for i in content_list:
            socre = 0.0
            match = ''
            for j in searchList:
                if(j.strip() in i):
                    socre += 1
                    match += j + '\t'
            socreDict[match.strip() + '\t' + i.strip()] = socre
        return socreDict

    def basic_socre(self, query, content_list, windows_size):
        socreDict = {}
        strDict = {}
        unicodeStr = unicode(query.query_str, 'utf-8')
        searchList = []
        for i in range(len(unicodeStr) - windows_size + 1):
            s = ""
            for j in range(windows_size):
                s += unicodeStr[i+j]
            searchList.append(s.encode('utf-8'))
        print searchList
        print len(searchList)
        for i in content_list:
            socre = 0.0
            match = ''
            for j in searchList:
                if(j.strip() in i):
                    socre += 1
                    match += j + '\t'
            socreDict[match.strip() + '\t' + i.strip()] = socre
        return socreDict
                
    def saveToFile(self):
        list = sorted(self.resultSocre.iteritems(), key = lambda x:x[1], reverse = True)
        f = open('socre.txt', 'w')
        for i in list:
            f.write(str(i[1]) + '\t' + i[0] + '<br>')
        f.close()
