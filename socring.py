#coding=utf-8
#__author__=chenjianfeng03@baidu.com

import re

class Socring:
    def __init__(self, idf_file = 'baike_tf_idf_small.d'):
        self.idfDic = self.loadfile(idf_file)
        self.resultSocre = {}
        self.resultStr = {}
        
    def loadfile(self,filename):
        f = open(filename)
        dic = {}
        for i in f:
            list = i.split('\t')
            dic[list[0].strip()] = float(list[2].strip())
        f.close()
        return dic

    def socre(self, query, method="tf-idf", segType = 'para'):
        if(segType == 'para'):
            content_list = self.segPara(query)
        else:
            content_list = self.segSentence(query)
        if(method == 'tf-idf'):
            self.resultSocre, self.resultStr = self.tf_idf_socre(query, content_list)
        else:
            pass

        return self.resultSocre, self.resultStr

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
                    match += j + "\t"
            socreDict[i.strip()] = socre
            strDict[i.strip()] = match.strip()
        return socreDict, strDict

    def saveToFile(self):
        list = sorted(self.resultSocre.iteritems(), key = lambda x:x[1], reverse = True)
        f = open('socre.txt', 'w')
        for i in list:
            f.write(str(i[1]) + '\t' + i[0] + '\t' + self.resultStr[i[0]] + '\n')
        f.close()
