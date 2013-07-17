#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import pycurl
import cStringIO
import json
import time
import logging
import sys
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

GET_MSG_LIST_URL = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=list&t=ajax-appmsgs-fileselect&type=10&r=0.9663556832875031&pageIdx=0&pagesize=10&formid=file_from_1366447908777&subtype=3"
GET_MSG_REFERER_URL = 'http://mp.weixin.qq.com/cgi-bin/masssendpage?t=wxm-send&token=%s&lang=zh_CN'
POST_MSG_URL = "http://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response"
POST_MSG_REFERER_URL = "http://mp.weixin.qq.com/cgi-bin/masssendpage?&token=%s=wxm-send&lang=zh_CN"
POST_IMAGE_URL = "http://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&token=%s&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1"
LOGIN_URL = "http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"
CREATE_MSG_URL = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&t=ajax-response&sub=create"
CREATE_MSG_REFERER_URL = "http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=edit&t=wxm-appmsgs"

logger = logging.getLogger("sync")

class WeixinClient(object):
	cert = ''
	slave_user = ''
	slave_sid = ''
	token = ''

	def send(self, weixin_message):
		self._login()

		# post images to mp.weixin.qq.com
		for item in weixin_message.items:
			print item.image
			item.image_id = self._post_image(item.image)

		# create msg
		self._create_msg(weixin_message)

		# send msg
		msg_id = self._find_msg_by_title(weixin_message.title)
		if msg_id != -1:
			return self._post_msg(msg_id)
		else:
			return False


	def _login(self):
		c = pycurl.Curl()
		c.setopt(pycurl.URL, str(LOGIN_URL))
		c.setopt(pycurl.POSTFIELDS, 'username=bestgames_&pwd=964d6985a37d6c7c0d7b1d7da6b05608&imgecode=&f=json')
		buff = cStringIO.StringIO()
		hdr = cStringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, buff.write)
		c.setopt(pycurl.HEADERFUNCTION, hdr.write)
		c.perform()

		cookies = hdr.getvalue().splitlines()
		index_start = cookies[7].find('cert=')
		index_end = cookies[7].find(';',index_start)
		self.cert = cookies[7][index_start:index_end]

		index_start = cookies[8].find('slave_user=')
		index_end = cookies[8].find(';',index_start)
		self.slave_user = cookies[8][index_start:index_end]

		index_start = cookies[9].find('slave_sid=')
		index_end = cookies[9].find(';',index_start)
		self.slave_sid = cookies[9][index_start:index_end]

		json_obj = json.loads(buff.getvalue())
		error_msg = json_obj['ErrMsg']
		index_start = error_msg.find('&token')
		self.token = error_msg[index_start + 7:len(error_msg)]

		logger.info('cert:%s, slave_user:%s, slave_sid:%s, token:%s', (self.cert, self.slave_user, self.slave_sid, self.token))

	def _post_image(self, image):
		mimetype_list = {
		        'gif'  :  'image/gif',
		        'jpeg' :  'image/jpeg',
		        'jpg'  :  'image/jpeg',
		        'png'  :  'image/png'
		        }
		filetype = str(image).split('.')[-1]
		filetype = filetype.lower()
		if filetype in mimetype_list.keys():
			mimetype = mimetype_list[filetype]
		c = pycurl.Curl()
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.HTTPPOST, [('filename', str(image)), ('uploadfile', (pycurl.FORM_FILE, str(image), pycurl.FORM_CONTENTTYPE, mimetype))])
		c.setopt(pycurl.URL, str(POST_IMAGE_URL % self.token))
		c.setopt(pycurl.COOKIE,'hasWarningUer=1;remember_act=bestgames_;hasWarningUer=1;remember_act=bestgames_' + self.cert +';' + self.slave_user + ';' + self.slave_sid + ';')
		buff = cStringIO.StringIO()
		hdr = cStringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, buff.write)
		c.setopt(pycurl.HEADERFUNCTION, hdr.write)
		c.perform()

		index_start = buff.getvalue().find('formId,')
		index_start = buff.getvalue().find('\'',index_start)
		index_end = buff.getvalue().find('\'',index_start + 1)
		image_id = buff.getvalue()[index_start + 1:index_end]

		logger.info('post %s to weixin and get image_id %s' % (image, image_id))
		return image_id

	def _create_msg(self, weixin_message):
		c = pycurl.Curl()
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.REFERER, str(CREATE_MSG_REFERER_URL % self.token))
		c.setopt(pycurl.COOKIE,str('hasWarningUer=1;remember_act=bestgames_;hasWarningUer=1;remember_act=bestgames_;' + self.cert +';' + self.slave_user + ';' + self.slave_sid + ';'))
		c.setopt(pycurl.URL, str(CREATE_MSG_URL % self.token))

		index = 0
		post_params = 'error=false&count=' + str(len(weixin_message.items)) + '&AppMsgId='
		for item in weixin_message.items:
			if item.sourceurl is not None:
				post_params = post_params + '&title' + str(index) + '=' + str(item.title) + '&digest' + str(index) + '=' + str(item.digest) + '&content' + str(index) + '=' + str(item.content) + '&fileid' + str(index) + '=' + str(item.image_id) + '&sourceurl' + str(index) + '=' + str(item.sourceurl)
			else:
				post_params = post_params + '&title' + str(index) + '=' + str(item.title) + '&digest' + str(index) + '=' + str(item.digest) + '&content' + str(index) + '=' + str(item.content) + '&fileid' + str(index) + '=' + str(item.image_id)
			index += 1
		post_params = post_params + '&ajax=1';

		c.setopt(pycurl.POSTFIELDS, post_params)
		buff = cStringIO.StringIO()
		hdr = cStringIO.StringIO()
		c.setopt(c.WRITEFUNCTION, buff.write)
		c.setopt(c.HEADERFUNCTION, hdr.write)
		c.perform()

		logger.info('create weixin message')

	def _find_msg_by_title(self, msg_title):
		c = pycurl.Curl()
		c.setopt(pycurl.URL, str(GET_MSG_LIST_URL % self.token))
		c.setopt(pycurl.REFERER, str(GET_MSG_REFERER_URL % self.token))
		c.setopt(pycurl.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + self.cert +';' + self.slave_user + ';' + self.slave_sid + ';')
		buff = cStringIO.StringIO()
		hdr = cStringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, buff.write)
		c.setopt(pycurl.HEADERFUNCTION, hdr.write)
		c.perform()

		today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		msg_list = json.loads(buff.getvalue())
		msg_title = msg_title.replace(' ', '&nbsp;', len(msg_title))

		msg_id = -1
		found = False
		for msg in msg_list['List']:
			if msg['time'] == today:
				msg_id = msg['appId']
				for app_msg in msg['appmsgList']:
					if app_msg['title'] == msg_title:
						msg_id = msg['appId']
						found = True
			if found:
				break

		logger.info('found %s and msg_id %s' % (msg_title, msg_id))
		return msg_id

	def _post_msg(self, msg_id):
		c = pycurl.Curl()
		post_params = 'type=10&fid=' + msg_id + '&appmsgid=' + msg_id + '&error=false&needcomment=0&groupid=-1&sex=0&country=&city=&province=&token=' + self.token + '&ajax=1'
		c.setopt(pycurl.URL, str(POST_MSG_URL))
		c.setopt(pycurl.REFERER,str(POST_MSG_REFERER_URL % self.token))
		c.setopt(pycurl.POSTFIELDS, str(post_params))
		c.setopt(pycurl.COOKIE,'hasWarningUer=1;hasWarningUer=1;' + self.cert +';' + self.slave_user + ';' + self.slave_sid + ';')
		buff = cStringIO.StringIO()
		hdr = cStringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, buff.write)
		c.setopt(pycurl.HEADERFUNCTION, hdr.write)
		c.perform()

		logger.info('send msg_id %s' % (msg_id))
		return buff.getvalue().find('''"ret":"0"''') != -1
