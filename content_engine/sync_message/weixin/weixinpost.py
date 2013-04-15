#encoding=utf-8
import pycurl
import cStringIO
import sys
import json
import time
reload(sys)
sys.setdefaultencoding('utf-8')

class weixin:

    get_msg_list_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?lang=zh_CN&sub=list&t=ajax-appmsgs-fileselect&type=10&r=0.20938333613582416&pageIdx=0&pagesize=10&formid=file_from_1364961994451&subtype=3"
    post_msg_url = "http://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response"
    post_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/masssendpage?t=wxm-send&lang=zh_CN"
    post_image_url = "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1"
    login_url = "http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"
    create_msg_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=create"
    create_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=edit&t=wxm-appmsgs-edit-new&type=10&subtype=3&lang=zh_CN&ismul=1"


    def getMsgList(self,cert,slave_user,slave_sid,title):
        c = pycurl.Curl()
        c.setopt(c.URL, self.get_msg_list_url)

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        msgList = json.loads(buff.getvalue())

        msg_id = ''
        found = False;
        for msg in msgList['List']:
            if msg['time'] == today:
                for appMsg in msg['appmsgList']:
                    if appMsg['title'] == title:
                        msg_id = msg['appId']
                        found = True;
            if found:
                break;

        print title + '  ' + msg_id
        self.postMsg(cert,slave_user,slave_sid,str(msg_id))

    def postMsg(self,cert,slave_user,slave_sid,msg_id):
        c = pycurl.Curl()
        post_params = 'type=10&fid=' + msg_id + '&appmsgid=' + msg_id + '&error=false&needcomment=0&groupid=-1&sex=0&country=&city=&province=&ajax=1'
        c.setopt(c.URL, self.post_msg_url)
        print post_params
        c.setopt(c.REFERER,self.post_msg_referer_url)
        c.setopt(c.POSTFIELDS, post_params)

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        print 'hdr:' + hdr.getvalue()
        print 'buff:' + buff.getvalue()



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
        c.setopt(c.URL, self.post_image_url)
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
        c.setopt(c.POST, 1)
        c.setopt(c.REFERER,self.create_msg_referer_url)
        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        c.setopt(c.URL, self.create_msg_url)

        #TODO get real content from mysql
        title = 'autopost'
        digest = 'test'
        content = '自动上传微信消息'
        count = 0

        post_params = 'error=false&count=' + str(msg_count) + '&AppMsgId='
        while count < msg_count:
            title = title + str(count)
            digest = digest + str(count)
            content = content + str(count)
            post_params =post_params + '&title' + str(count) + '=' + title + '&digest' + str(count) + '=' + digest + '&content' + str(count) + '=' + content + '&fileid' + str(count) + '=' + from_id_array[count]
            count = count + 1

        post_params = post_params + '&ajax=1';
        print post_params
        c.setopt(c.POSTFIELDS, post_params)
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.setopt(c.VERBOSE, True)
        c.perform()

        print 'createSingleMsg hdr:' + hdr.getvalue()
        print 'createSingleMsg buff:' + buff.getvalue()

        self.getMsgList(cert,slave_user,slave_sid,title)


    def login(self):
        c = pycurl.Curl()
        c.setopt(c.URL, self.login_url)
        c.setopt(c.POSTFIELDS, 'username=bestgames_&pwd=964d6985a37d6c7c0d7b1d7da6b05608&imgecode=&f=json')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

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

        #TODO get msg count from sql
        self.postImage(cert,slave_user,slave_sid,1)

w = weixin()
w.login()


