# -*- coding:utf-8 -*-
import bottle
import sys
import os

bottle.TEMPLATE_PATH.insert(0, 'views')
__author__ = 'yuyang18'

@bottle.get('/')
def index():
    return bottle.template("index.html")
@bottle.post('/')
def say_hello():

    query = bottle.request.forms.get('input_query', None)
    windows_size_str = bottle.request.forms.get('pn', None)

    pn = int(windows_size_str)
    res_bk = query
    res_zd = query
    #res_bk = "test"
    #res_zd = "test"
    cmd_bk = query
    cmd_zd = query
    cmd_all = cmd_bk+"\n"+cmd_zd
    #cmd_all= "test"
    a=bottle.template('index.html',query=query,win_sz=windows_size_str,zd_evi=res_zd,bk_evi=res_bk,cmd_evi=cmd_all)
    return a



if __name__ == '__main__':
    host_ip = "10.48.16.44"
    bottle.run(host=host_ip, port=8610)
