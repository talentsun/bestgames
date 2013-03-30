# Create your views here.
# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.utils.encoding import smart_str, smart_unicode
import hashlib

import logging, traceback, time, struct, socket
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')
from api.tables import GameTable
from api.models import Game

import xml.etree.ElementTree as ET
import socket
from pyweixin import WeiXin
from router import router

TOKEN = "itv"

@csrf_exempt
def index(request):
    global TOKEN
    if request.method == 'GET':
        if 'signature' not in request.GET or 'timestamp' not in request.GET or 'nonce' not in request.GET or 'echostr' not in request.GET:
                return HttpResponse('bad request %s' % str(request.GET))
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        weixin = WeiXin.on_connect(TOKEN, timestamp, nonce, signature, echostr)
        if weixin.validate():
            return HttpResponse(echostr, content_type="text/plain")
        else:
            return HttpResponse(None, content_type="text/plain")
    elif request.method == 'POST':
        weixin = WeiXin.on_message(smart_str(request.raw_post_data))
        message = weixin.to_json()
        
        build_conf = router.route(message['content'])
        if build_conf is not None:
            return HttpResponse(MessageBuilder.build(build_conf), content_type="application/xml")
        else:
            return HttpResponse('<xml></xml>', content_type="application/xml")


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

