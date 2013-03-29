# Create your views here.
# coding: utf8
from django.http import HttpResponse
import hashlib

import logging, traceback, time
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')


import xml.etree.ElementTree as ET

def dealWithInput(inputText):
    root = ET.fromstring(inputText)
    infos = {}
    for child in root:
        infos[child.tag] = child.text
    return infos

def responseText(meName, userName, text):
    textTpl = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%d</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>
    """

    return textTpl % (userName, meName, time.time(), text)

@csrf_exempt
def index(request):
    try:
        logger.debug("index %s" % request.method)
        if request.method == 'GET':
            if 'signature' not in request.GET or 'timestamp' not in request.GET or 'nonce' not in request.GET or 'echostr' not in request.GET:
                return HttpResponse('bad request %s' % str(request.GET))
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            echostr = request.GET['echostr']
            infos = [signature, timestamp, nonce]
            infos.sort()
            m = hashlib.sha1()
            m.update(''.join(infos))
            caledSig = m.hexdigest()

            return HttpResponse(echostr)

        if request.method == 'POST':
            logger.debug(request.raw_post_data)
            infos = dealWithInput(request.raw_post_data)
            logger.debug(str(infos))
            resp = responseText(infos['ToUserName'], infos['FromUserName'], "欢迎")
            logger.debug(resp)
            return HttpResponse(resp)
    except:
        logger.debug(traceback.format_exc())
