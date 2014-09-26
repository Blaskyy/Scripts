#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##meizi.py
#./meizi.py from to file
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
f = open(sys.argv[3],'w')
for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    content = urlopen('http://jandan.net/ooxx/page-%d#comments' % i).read()
    soup = BeautifulSoup(content)
    for i in soup.find_all('li'):
        for j in i.find_all('p'):
            for k in j.find_all('img'):
                try:
                    f.write("%s\n" % k.get('src'))
                except:
                    continue
f.close()

