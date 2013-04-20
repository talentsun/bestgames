#encoding=utf-8
import pycurl
import cStringIO
import sys
import json
import time
import MySQLdb as mdb
import os
import shutil
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

class weixin:

    nameList = []
    iconList = []
    gameBriefList = []
    gameRatingList = []
    gameCategoryList = []
    collection_title=''
    collection_cover=''
    entity_id = ''
    weixin_status = ''

    get_msg_list_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=492370483&lang=zh_CN&sub=list&t=ajax-appmsgs-fileselect&type=10&r=0.9663556832875031&pageIdx=0&pagesize=10&formid=file_from_1366447908777&subtype=3"
    get_msg_referer_url = 'http://mp.weixin.qq.com/cgi-bin/masssendpage?t=wxm-send&token=492370483&lang=zh_CN'
    post_msg_url = "http://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response&token=492370483"
    post_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/masssendpage?&token=492370483t=wxm-send&lang=zh_CN"
    post_image_url = "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&token=492370483&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1"
    login_url = "http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"
    create_msg_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=492370483&lang=zh_CN&t=ajax-response&sub=create"
    create_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=492370483&lang=zh_CN&sub=edit&t=wxm-appmsgs"


    def getMsgList(self,cert,slave_user,slave_sid,title):
        c = pycurl.Curl()
        c.setopt(c.URL, self.get_msg_list_url)
        c.setopt(c.REFERER,self.get_msg_referer_url)

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

        weixin_result = 3
        if buff.getvalue().index('''"ret":"0"''') != -1:
            weixin_result = 2;

        self.update_weixin_status(weixin_result)

    def update_weixin_status(self,weixin_result):
        con = mdb.connect('localhost', 'root',
            'nameLR9969', 'content_engine');

        cur = con.cursor()
        sql = "update entities set status = '"  + str(weixin_result) + "' where id = '" + str(self.entity_id) + "';"
        print sql
        cur.execute(sql)
        con.commit()
        con.close()



    def postImage(self,cert,slave_user,slave_sid,msg_count):

        from_id_array = []
        count = 0;
        while count < msg_count:
            #TODO read filename from sql
            if count == 0:
                filename = '/home/app_bestgames/content_engine/media/' + self.collection_cover
            else:
                filename= '/home/app_bestgames/content_engine/media/' + self.iconList[count - 1]
            shutil.copy(filename,'/home/app_bestgames/weixinpic/' + str(count) + ".jpg")
            filename = '/home/app_bestgames/weixinpic/' + str(count) + ".jpg"
            from_id_array.append(self.postSingelImage(cert,slave_user,slave_sid,filename))
            count = count + 1

        self.createSingleMsg(cert,slave_user,slave_sid,from_id_array,msg_count)

    def postSingelImage(self,cert,slave_user,slave_sid,filename):
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        print filename
        values = [
            ("filename", filename),
            ("uploadfile", (c.FORM_FILE, filename))
        ]
        c.setopt(c.HTTPPOST, values)
        c.setopt(c.URL, self.post_image_url)
        c.setopt(c.COOKIE,'hasWarningUer=1;remember_act=bestgames_;hasWarningUer=1;remember_act=bestgames_' + cert +';' + slave_user + ';' + slave_sid + ';')
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
        c.setopt(c.COOKIE,'hasWarningUer=1;remember_act=bestgames_;hasWarningUer=1;remember_act=bestgames_;' + cert +';' + slave_user + ';' + slave_sid + ';')
        c.setopt(c.URL, self.create_msg_url)

        #TODO get real content from mysql
        count = 0

        post_params = 'error=false&count=' + str(msg_count) + '&AppMsgId='
        while count < msg_count:
            if count == 0:
                title = str(self.collection_title)
                digest = str(self.collection_title)
                content = str(self.weixin_status)
            else:
                title = str(self.gameBriefList[count - 1])
                digest = str(self.gameBriefList[count - 1])
                content = str(self.gameBriefList[count - 1 ])
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

#        print 'count = ' + str(len(self.iconList))
##        self.iconList.
        self.postImage(cert,slave_user,slave_sid,len(self.iconList) + 1)

    def get_msg_from_sql(self):
        con = None

        try:

            con = mdb.connect('localhost', 'root',
                'nameLR9969', 'content_engine',charset='utf8');

            cur = con.cursor()

            curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
            print 'start: ' + curtime
            #curtime = '2013-04-22 14:10'
            sql = "SELECT weixin.entity_ptr_id,weixin.title AS weixin_title, weixin.cover AS weixin_cover,games.`name` AS game_name,games.icon AS game_icon,game_entities.brief_comment AS game_brief_comment,games.rating AS game_rating,categories.`name` AS game_category,"\
                  "weixin_entities.weibo_sync_timestamp AS weixin_weibo_sync_timestamp,weixin_entities.`status` AS weixin_status,weixin_entities.`recommended_reason` FROM weixin INNER JOIN weixin_games ON weixin.entity_ptr_id = weixin_games.weixin_id "\
                  "INNER JOIN games ON weixin_games.game_id = games.entity_ptr_id INNER JOIN entities game_entities ON games.entity_ptr_id = game_entities.id "\
                  "INNER JOIN entities weixin_entities ON weixin.entity_ptr_id = weixin_entities.id INNER JOIN categories ON games.category_id = categories.id "\
                  "WHERE weixin_entities.weibo_sync_timestamp like '"+ curtime +  "%' and weixin_entities.status = '1' and weixin_entities.type ='5'"
            print sql
            cur.execute(sql)
            data = cur.fetchall()

            cur.execute(sql)

            data = cur.fetchall()
            r = 0
            for result in data:
                self.entity_id = result[0]
                self.collection_title = result[1]
                self.collection_cover = result[2]
                self.nameList.append(result[3])
                self.iconList.append(result[4])
                self.gameBriefList.append(result[5])
                self.gameRatingList.append(result[6])
                self.gameCategoryList.append(result[7])
                self.weixin_status = result[10]

                r = 1

            if r != 0:
                self.login()
#                print len(self.iconList)

        finally:
            if con:
                con.close()


if __name__ == '__main__':
    weixin().get_msg_from_sql()





