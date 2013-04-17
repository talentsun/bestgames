import urllib

class NetUtil:
    def download(self,url, localFileName = None):
        try:
            print 'start download'
            r = urllib.urlopen(url)
            f = open(localFileName, 'wb')
            f.write(r.read())
            f.close()
        except Exception, e:
            print 'Exception error is: %s' % e