#!/usr/local/bin/python
#coding=utf8
import requests, urllib2


TINYURL_API = 'http://tinyurl.com/api-create.php?url='

def shorten_url(url):
	global TINYURL_API

	req = requests.get(TINYURL_API + url)
	if req.status_code == 200:
		return req.text
	else:
		return None 


def send_sms(user_no, content):
    url = "http://utf8.sms.webchinese.cn/?Uid=limijiaoyin&Key=66a7deba837e2f0630dc&smsMob=%s&smsText=%s" % (user_no, content.encode('utf-8'))
    resp = urllib2.urlopen(url)
    return resp.read()


if __name__ == '__main__':
    send_sms("13488684891", u"你好！发短信成功！")


    
