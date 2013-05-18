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
    gameRecommendReasonList = []
    gameScreenPath1List = []
    gameScreenPath2List = []
    gameScreenPath3List = []
    gameScreenPath4List = []
    adviceImageList = []
    weixin_message_title=''
    weixin_message_cover=''
    entity_id = ''
    weixin_status = ''
    weixin_token = ''

    get_msg_list_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=list&t=ajax-appmsgs-fileselect&type=10&r=0.9663556832875031&pageIdx=0&pagesize=10&formid=file_from_1366447908777&subtype=3"
    get_msg_referer_url = 'http://mp.weixin.qq.com/cgi-bin/masssendpage?t=wxm-send&token=%s&lang=zh_CN'
    post_msg_url = "http://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response"
    post_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/masssendpage?&token=%s=wxm-send&lang=zh_CN"
    post_image_url = "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&token=%s&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1"
    login_url = "http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"
    create_msg_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&t=ajax-response&sub=create"
    create_msg_referer_url = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=edit&t=wxm-appmsgs"

    def CoverImageBuilder(self,screen1,screen2,screen3,screen4):
        templete_file = open('./templates/screenShot.html','r')
        line = templete_file.readline()
        content = ''
        while line:
            content = content + line;
            line = templete_file.readline()

        templete_file.close()

        content = content.replace('screenShotPath1','/home/app_bestgames/content_engine/media/' + screen1)
        content = content.replace('screenShotPath2','/home/app_bestgames/content_engine/media/' + screen2)
        content = content.replace('screenShotPath3','/home/app_bestgames/content_engine/media/' + screen3)
        content = content.replace('screenShotPath4','/home/app_bestgames/content_engine/media/' + screen4)

        curtime = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
        root = "/home/app_bestgames/content_engine/media/"
        filename = root + curtime + 'share.html'
        shareGameFile = open(filename,'w')
        shareGameFile.write(content)
        shareGameFile.close()

        coverFileName = "cover.png"
        outputFilePath = root + coverFileName

        command = "phantomjs --disk-cache=yes --max-disk-cache-size=10000 rasterize.js "+ filename + "  " + outputFilePath

        print command
        os.system(command)

        self.iconList[0] = coverFileName


    def getMsgList(self,cert,slave_user,slave_sid,title):
        c = pycurl.Curl()
        c.setopt(c.URL, str(self.get_msg_list_url%self.weixin_token))
        c.setopt(c.REFERER,str(self.get_msg_referer_url%self.weixin_token))

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        msgList = json.loads(buff.getvalue())

        title = title.replace(' ','&nbsp;',len(title))

        msg_id = ''
        found = False;
        for msg in msgList['List']:
            if msg['time'] == today:
                msg_id = msg['appId']
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
        post_params = 'type=10&fid=' + msg_id + '&appmsgid=' + msg_id + '&error=false&needcomment=0&groupid=-1&sex=0&country=&city=&province=&token=' + self.weixin_token + '&ajax=1'
        c.setopt(c.URL, str(self.post_msg_url))
        print post_params
        c.setopt(c.REFERER,str(self.post_msg_referer_url%self.weixin_token))
        c.setopt(c.POSTFIELDS, str(post_params))

        c.setopt(c.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + cert +';' + slave_user + ';' + slave_sid + ';')
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()

        print 'hdr:' + hdr.getvalue()
        print 'buff:' + buff.getvalue()

        weixin_result = 3
        if buff.getvalue().find('''"ret":"0"''') != -1:
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
            filename= '/home/app_bestgames/content_engine/media/' + self.iconList[count]
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
        c.setopt(c.URL, str(self.post_image_url%self.weixin_token))
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
        url = self.create_msg_referer_url%self.weixin_token
        print url
        c.setopt(c.REFERER,str(url))
        c.setopt(c.COOKIE,'hasWarningUer=1;remember_act=bestgames_;hasWarningUer=1;remember_act=bestgames_;' + cert +';' + slave_user + ';' + slave_sid + ';')
        c.setopt(c.URL, str(self.create_msg_url%self.weixin_token))

        count = 0
        post_params = 'error=false&count=' + str(msg_count) + '&AppMsgId='

        while count < msg_count:
            title = str(self.gameBriefList[count])
            digest = str(self.gameBriefList[count])
            content = str(self.gameRecommendReasonList[count])
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

        self.getMsgList(cert,slave_user,slave_sid,self.gameBriefList[0])


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

        json_obj = json.loads(buff.getvalue())
        error_msg = json_obj['ErrMsg']
        print error_msg
        index_start = error_msg.find('&token')
        self.weixin_token = error_msg[index_start + 7:len(error_msg)]

#        print self.weixin_token

        msg_count = len(self.iconList)
        print str(msg_count)
        self.postImage(cert,slave_user,slave_sid,msg_count)

    def get_msg_from_sql(self):
        con = None
        try:
            con = mdb.connect('118.244.225.222', 'root',
                'nameLR9969', 'content_engine',charset='utf8');

            cur = con.cursor()

            curtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
            print 'start: ' + curtime
            #curtime = '2013-04-22 14:10'
            sql = "SELECT weixin2.entity_ptr_id,weixin2.title AS weixin_title, weixin2.cover AS weixin_cover,games.`name` AS game_name,games.icon AS game_icon,game_entities.`recommended_reason` AS game_recommended_reason,game_entities.brief_comment AS game_brief_comment," \
                  "games.screenshot_path_1 AS game_screenshot_path_1,games.screenshot_path_2 AS game_screenshot_path_2,"\
                  "games.screenshot_path_3 AS game_screenshot_path_3, games.screenshot_path_4 AS game_screenshot_path_4,weixin_entities.weibo_sync_timestamp AS weixin_weibo_sync_timestamp," \
                  "weixin_entities.`status` AS weixin_status,weixin_entities.`recommended_reason`" \
                  " FROM weixin2 INNER JOIN weixin2_games ON weixin2.entity_ptr_id = weixin2_games.weixin_id "\
                  "INNER JOIN games ON weixin2_games.game_id = games.entity_ptr_id INNER JOIN entities game_entities ON games.entity_ptr_id = game_entities.id "\
                  "INNER JOIN entities weixin_entities ON weixin2.entity_ptr_id = weixin_entities.id INNER JOIN categories ON games.category_id = categories.id "\
                  "WHERE weixin_entities.weibo_sync_timestamp like '"+ curtime +  "%' and weixin_entities.status = '1' and weixin_entities.type ='5'"
            print sql
            cur.execute(sql)
            data = cur.fetchall()

            cur.execute(sql)

            data = cur.fetchall()
            r = 0
            for result in data:
                self.entity_id = result[0]
                self.weixin_message_title = result[1]
                self.weixin_message_cover = result[2]
                self.nameList.append(result[3])
                self.iconList.append(result[4])
                url_pos = result[5].find('http://')
                if url_pos != -1:
                    description = result[5][:url_pos]
                else:
                    description = result[5]
                self.gameRecommendReasonList.append(description + '<br><br><font color="gray">回复游戏名获得该游戏的下载地址</font>')
                self.gameBriefList.append(result[6] + "  -  " + result[3])
                self.gameScreenPath1List.append(result[7])
                self.gameScreenPath2List.append(result[8])
                self.gameScreenPath3List.append(result[9])
                self.gameScreenPath4List.append(result[10])
                self.weixin_status = result[13]

                r = 1

            sql = "select weixin2.entity_ptr_id, weixin2.title,weixin2.cover, advice_entities.`recommended_reason`,"+ \
                  " advice_entities.brief_comment,game_advices.advice_image, advice_entities.status, advice_entities.weibo_sync_timestamp,game_advices.title " + \
                  " FROM weixin2 INNER JOIN weixin2_advices ON weixin2.entity_ptr_id = weixin2_advices.weixin_id INNER JOIN game_advices ON weixin2_advices.`gameadvices_id` = game_advices.entity_ptr_id " +\
                  " INNER JOIN entities advice_entities WHERE advice_entities.weibo_sync_timestamp like '" + curtime + "%' and advice_entities.status = '1' and advice_entities.type ='5'";

            sql = "select weixin2.entity_ptr_id, weixin2.title,weixin2.cover, advice_entities.`recommended_reason`, " + \
                  " advice_entities.brief_comment,game_advices.advice_image, advice_entities.status, " + \
                  " advice_entities.weibo_sync_timestamp,game_advices.title  FROM weixin2 INNER JOIN weixin2_advices " + \
                  " ON weixin2.entity_ptr_id = weixin2_advices.weixin_id INNER JOIN game_advices " + \
                  "ON weixin2_advices.`gameadvices_id` = game_advices.entity_ptr_id " + \
                  " INNER JOIN entities advice_entities ON game_advices.entity_ptr_id = advice_entities.id" + \
                  " INNER JOIN entities weixin_entities ON weixin2.entity_ptr_id = weixin_entities.id " + \
                  " WHERE weixin_entities.weibo_sync_timestamp like '" + curtime + "' and weixin_entities.status = '3' and weixin_entities.type ='5'";

            cur.execute(sql)
            data = cur.fetchall()

            cur.execute(sql)

            data = cur.fetchall()


            for result in data:
                self.entity_id = result[0]
                self.weixin_message_title = result[1]
                self.weixin_message_cover = result[2]
                url_pos = result[3].find('http://')
                if url_pos != -1:
                    description = result[3][:url_pos]
                else:
                    description = result[3]
                if(str(description).strip() == ''):
                    description = result[8]
                self.gameRecommendReasonList.append(description)
                if str(result[4]).strip() == '':
                    result[4] = u"游戏情报站"
                self.gameBriefList.append(result[4] + " - " + result[8])
                self.iconList.append(result[5])
                self.weixin_status = result[6]
                r = 1

            if r != 0:
                if self.weixin_message_title is None or self.weixin_status is None\
                   or str(self.weixin_status).strip() == '' or self.weixin_message_cover is None\
                or str(self.weixin_message_cover).strip() == '':
                    if len(self.gameScreenPath1List) == 0:
                        pass
                    else:
                        self.CoverImageBuilder(self.gameScreenPath1List[0],self.gameScreenPath2List[0],self.gameScreenPath3List[0],self.gameScreenPath4List[0])
                        pass
                else:
                    self.iconList.insert(0,self.weixin_message_cover)
                    self.gameBriefList.insert(0,self.weixin_message_title)
                    self.gameRecommendReasonList.insert(0,self.weixin_status)
                self.login()

        finally:
            if con:
                con.close()


if __name__ == '__main__':
    print weixin().get_msg_from_sql()







