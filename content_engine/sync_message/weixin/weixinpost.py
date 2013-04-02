#encoding=utf-8
import pycurl
import cStringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class weixin:
    def postImage(self,cert,slave_user,slave_sid,msg_count):

        from_id_array = []
        count = 0;
        while count < msg_count:
            #TODO read filename from sql
            filename='/Users/huwei/test' + str(count) + '.jpg'
            from_id_array.append(self.postSingelImage(cert,slave_user,slave_sid,filename))
            count = count + 1

        self.createSingleMsg(cert,slave_user,slave_sid,from_id_array,msg_count)

    def postSingelImage(self,cert,slave_user,slave_sid,filename):
        c = pycurl.Curl()


        c.setopt(c.POST, 1)
        c.setopt(c.HTTPPOST, [('filename', filename), (('uploadfile', (c.FORM_FILE, filename)))])
        c.setopt(c.URL, "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1" )

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        print 'hdr:' + hdr.getvalue()
        print 'buff:' + buff.getvalue()
        index_start = buff.getvalue().find('formId,')
        index_start = buff.getvalue().find('\'',index_start)
        print 'index_start =' +  str(index_start)
        index_end = buff.getvalue().find('\'',index_start + 1)
        form_id = buff.getvalue()[index_start + 1:index_end]
        print 'form_id=' + form_id
        return form_id


    def createSingleMsg(self,cert,slave_user,slave_sid,from_id_array,msg_count):
        c = pycurl.Curl()

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        c.setopt(c.URL, "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=create")
        title = 'autopost'
        digest = 'test'
        content = '自动上传微信消息'
        count = 0
        post_params = 'error=false&count=' + str(msg_count) + '&AppMsgId='
        while count < msg_count:
            title = title + str(count)
            digest = digest + str(count)
            content = '自动上传微信消息' + str(count)
            post_params =post_params + '&title' + str(count) + '=' + title + '&digest' + str(count) + '=' + digest + '&content' + str(count) + '=' + content + '&fileid' + str(count) + '=' + from_id_array[count]
            count = count + 1

        post_params = post_params + '&ajax=1';
        c.setopt(c.POSTFIELDS,post_params)
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        print 'hdr:' + hdr.getvalue()
        print 'buff:' + buff.getvalue()


    def login(self):
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN')
        c.setopt(c.POSTFIELDS, 'username=bestgames_&pwd=964d6985a37d6c7c0d7b1d7da6b05608&imgecode=&f=json')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        print 'hdr:' + hdr.getvalue()
        print 'buff:' + buff.getvalue()

        cookies = hdr.getvalue().splitlines()
        index_start = cookies[7].find('cert=')
        index_end = cookies[7].find(';',index_start)
        cert = cookies[7][index_start:index_end]
        print 'cert=' + cert

        index_start = cookies[8].find('slave_user=')
        index_end = cookies[8].find(';',index_start)
        slave_user = cookies[8][index_start:index_end]
        print 'slave_user=' + cert

        index_start = cookies[9].find('slave_sid=')
        index_end = cookies[9].find(';',index_start)
        slave_sid = cookies[9][index_start:index_end]
        print 'slave_sid='  + slave_sid

        self.postImage(cert,slave_user,slave_sid,2)

w = weixin()
w.login()


