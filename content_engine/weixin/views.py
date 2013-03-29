# Create your views here.
# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
import hashlib

import logging, traceback, time, struct, socket
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')
from api.tables import GameTable
from api.models import Game


import xml.etree.ElementTree as ET
import socket

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

def search(request):
    games = []
    if request.method == 'GET':
        return render(request, "search.html", {"games": GameTable(games)})
    elif request.method == 'POST':
        logger.debug("content %s" % request.POST['content'])
        content = request.POST['content'].encode("utf-8")
        req = struct.pack("!H%ds" % len(content), len(content), content)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(req, ("127.0.0.1", 8128))
        resp = s.recv(4196)
        startAddr = 0
        num = struct.unpack("!H", resp[startAddr : startAddr + 2])[0]
        logger.debug("get %d games" % num)
        startAddr += 2
        for i in range(num):
            gameId = struct.unpack("!I", resp[startAddr : startAddr + 4])[0]
            logger.debug("get game %d" % gameId)
            if gameId != 0:
                games.append(Game.objects.get(pk = gameId))
        return render(request, "search.html", {"games": GameTable(games)})

