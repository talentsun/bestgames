import urllib

class NetUtil:
    def download(self,url, localFileName = None):
        r = urllib.urlopen(url)
        f = open(localFileName, 'wb')
        f.write(r.read())
        f.close()