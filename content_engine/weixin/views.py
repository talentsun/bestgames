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
from message_builder import MessageBuilder, BuildConfig
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
    weixinlogger = logging.getLogger('weixin')
    if request.method == 'GET':
        if 'signature' not in request.GET or 'timestamp' not in request.GET or 'nonce' not in request.GET or 'echostr' not in request.GET:
                return HttpResponse('bad request %s' % str(request.GET))
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        weixinlogger.info("receive one get message signature %s timestamp %s nonce %s echostr %s" % (signature, timestamp, nonce, echostr))
        weixin = WeiXin.on_connect(TOKEN, timestamp, nonce, signature, echostr)
        if weixin.validate():
            return HttpResponse(echostr, content_type="text/plain")
        else:
            return HttpResponse(None, content_type="text/plain")
    elif request.method == 'POST':
        try:
            weixin = WeiXin.on_message(smart_str(request.raw_post_data))
            message = weixin.to_json()
            weixinlogger.info("receive one message %s" % str(message))

            Router.get_instance().reply(message, _route_callback)
            
            if router_error is None and router_reply is not None:
                router_reply.platform = MessageBuilder.PLATFORM_WEIXIN
                if router_reply.type != MessageBuilder.TYPE_NO_RESPONSE:
                    weixinlogger.info("reply success type %s platform %s data %s" % (router_reply.type, router_reply.platform, router_reply.data))
                    return HttpResponse(MessageBuilder.build(message, router_reply), content_type="application/xml")
                else:
                    weixinlogger.info("%s", router_reply.data)
            else:
                weixinlogger.info("router error %s router reply %s" % (str(router_error), str(router_reply)))
                raise "not find games"
                return HttpResponse('<xml></xml>', content_type="application/xml")
        except:
            logger.error(traceback.format_exc())
            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, u"小每的才一个月大，智商还很低，非常抱歉，没能理解你的话。不过小每会多玩游戏，变得越来越聪明的。\r\n你可以输入帮助了解小每现在支持的指令。")
            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")

def load(request):
    # load_games_for_today(True)
    # load_shorten_urls(True)
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
        for g in stResp.games:
            try:
                game = Game.objects.get(pk = g.gameId)
                game.nameRel = g.nameRel
                game.gameRel = g.gameRel
                logger.debug("game id %d" % g.gameId)
            except:
                logger.error("not find game with id %d" % g.gameId)
                continue
            games.append(game)
        return render(request, "search.html", {"games": SearchResultTable(games)})
