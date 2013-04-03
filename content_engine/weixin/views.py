# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.utils.encoding import smart_str, smart_unicode
import hashlib

import logging, traceback, time, struct, socket
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')
from portal.tables import SearchResultTable
from portal.models import Game
from service import search_pb2
import socket

import rules
import rules_game_search
from pyweixin import WeiXin
from router import Router
from message_builder import MessageBuilder
from data_loader import load_games_for_today, load_shorten_urls

TOKEN = "itv"

router_error = None
router_reply = None
def _route_callback(error=None, reply=None):
    global router_error, router_reply
    router_error = error
    router_reply = reply

@csrf_exempt
def index(request):
    global TOKEN, router_error, router_reply
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

        Router.get_instance().reply(message, _route_callback)
        
        if router_error is None and router_reply is not None:
            router_reply.platform = MessageBuilder.PLATFORM_WEIXIN
            return HttpResponse(MessageBuilder.build(message, router_reply), content_type="application/xml")
        else:
            return HttpResponse('<xml></xml>', content_type="application/xml")

def load(request):
    load_games_for_today()
    load_shorten_urls()
    return render(request, 'weixin_load.html', {})

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
