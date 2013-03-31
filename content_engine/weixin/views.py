# Create your views here.
# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
import hashlib

import logging, traceback, time, struct, socket
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')
from api.tables import SearchResultTable
from api.models import Game
from service import search_pb2


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
        return render(request, "search.html", {"games": SearchResultTable(games)})
    elif request.method == 'POST':
        logger.debug("content %s" % request.POST['content'])
        content = request.POST['content']
        stQuery = search_pb2.Query()
        stQuery.query = content
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(struct.pack("!H", 1) + stQuery.SerializeToString(), ("127.0.0.1", 8128))
        resp = s.recv(4196)
        stResp = search_pb2.Response()
        stResp.ParseFromString(resp)
        logger.debug("result %d" % stResp.result)
        logger.debug("gameIds %s" % str(stResp.gameIds))
        for id in stResp.gameIds:
            try:
                game = Game.objects.get(pk = id)
                logger.debug("game id %d" % id)
            except:
                logger.error("not find game with id %d" % id)
                continue
            games.append(game)
        return render(request, "search.html", {"games": SearchResultTable(games)})

