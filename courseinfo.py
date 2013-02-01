#! /usr/bin/env python
# -*- coding: utf8 -*-
import cookielib, urllib2, urllib, socket
__author__ = "Blask"
import time, re
from bs4 import BeautifulSoup

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        excpetions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            if try_one_last_time:
                return f(*args, **kwargs)
            return
        return f_retry  # true decorator
    return deco_retry

@retry((urllib2.URLError,socket.timeout), tries=3, delay=3, backoff=2)
def login(stuid = None, pwd = None):  #用户名还是我自己的
    #登陆选课网站
    cj = cookielib.CookieJar()#详见cookielib
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    exheaders = [("User-Agent","Mozilla/4.0 (compatible; MSIE 7.1; Windows NT 5.1; SV1)"),] #加入头信息
    opener.addheaders=exheaders
    url_login = 'http://202.115.47.141/loginAction.do'
    post_data = (('zjh',stuid), ('mm',pwd))
    req1 = opener.open(url_login, urllib.urlencode(post_data), timeout=10)  #这时，cookie已经进来了。
    url_course = "http://202.115.47.141/xkAction.do?actionType=6"
    req2 = opener.open(url_course, timeout=10) #打开课程页面
    data2 = req2.read() #读取课程页面
    return data2.decode('gbk').encode('utf8') #要decode，否则为乱码

def parseHTML(stuid, pwd, w):
    try:
        soup = BeautifulSoup(''.join(login(stuid, pwd)))
        for data in soup.find_all('img'):
            line = data.get('name')
            w.write("%s %s %s %s\n" % (stuid, pwd, line[32:41], line[46:]))
    except TypeError, e:
        return 1

if __name__ == '__main__':
    f = open('id','r')
    w = open('data', 'w')
    for line in open('id'):
        line = f.readline()
        stuid = line[0:10]
        pwd = line[20:28]
        print(stuid)
        parseHTML(stuid, pwd, w)
    f.close()
    w.close()


