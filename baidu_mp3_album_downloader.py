#!/usr/bin/env python2
import re, sys, os, urllib

re_song = re.compile(r'\'sid\': \'(.+?)\', \'sname\': \'(.+?)\'')
re_name = re.compile(r'\\\&\#\d+?;')

def main(albumid):
    f = urllib.urlopen('http://music.baidu.com/album/' + albumid).read()
    infos = re_song.findall(f)
    size = len(infos)
    z = 0
    if size <= 9:
        z = 1
    elif size >= 10 and size <= 99:
        z = 2
    elif size >= 100 and size <= 999:
        z = 3
    else:
        z = 1

    urls = []
    for i in range(1, size + 1):
        songid, sname = infos[i - 1]
        durl = 'http://yinyueyun.baidu.com/data/cloud/downloadsongfile\?songIds\=%s\&rate\=320' % songid
        sname = re_name.sub(r' - ', sname)      # remove all http symbol from song-name.
        sname = str(i).zfill(z) + '.' + sname.strip() + '.mp3'
        urls.append('aria2c --check-certificate=false -c -s10 -x10 -o "%s" %s &' % (sname, durl))

    for i in urls:
        status = os.system(i)
        if status == 2048:           # 320kbps-mp3 is not available, so getting 128kbps-mp3.
            os.system(i[:-10])
        if status not in [0, 2048]:     # other http-errors, such as 302.
            print '\n\n ----### ERROR ==> %d ###--- \n\n' % status
            break

if __name__ == '__main__':
    albumid = sys.argv[1]
    main(albumid)
