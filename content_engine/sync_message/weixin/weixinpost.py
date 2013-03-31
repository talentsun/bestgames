import pycurl
import cStringIO
import re

class weixin:
    filename='/Users/huwei/test.jpg'
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.HTTPPOST, [('title', 'test'), (('file', (c.FORM_FILE, filename)))])
    c.setopt(c.VERBOSE, 1)
    buff = cStringIO.StringIO()
    hdr = cStringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, buff.write)
    c.setopt(c.URL, "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1" )
    c.setopt(c.HEADERFUNCTION, hdr.write)

    c.setopt(c.HTTPHEADER,['Cookie','hasWarningUser=1; pgv_pvid=8543179264; '
                                    'o_cookie=406465841; ptui_loginuin=406465841; '
                                    'ptisp=cn; pt2gguin=o0406465841; RK=5dB+IHLqWv;'
                                    ' cert=Q8LbUgrLPQbhWRGKKpm9pcExkntSNrqA; '
                                    'slave_user=gh_d8d72c671c22; '
                                    'slave_sid=UThMYlVnckxQUWJoV1JHS0twbTlwY0V4a250U05ycUF5OE1wbmE5OV9qcVc5NERUdFhfUTdFbXJaUGdKZUVqTU40YTljaWliekc0SUtHemFBd19IOWo1NjhsTm1fNTVNN2ZUanY4dDNPdkt5YWlHTHd6dGZ4Z0ZmcUVMV2pzR0s='])
    c.perform()

    print "status code: %s" % c.getinfo(pycurl.HTTP_CODE)
    # -> 200

    status_line = hdr.getvalue().splitlines()[0]
    m = re.match(r'HTTP\/\S*\s*\d+\s*(.*?)\s*$', status_line)
    if m:
        status_message = m.groups(1)
    else:
        status_message = ''

    print "status message: %s" % status_message



weixin()
