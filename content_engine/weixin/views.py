# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.utils.encoding import smart_str, smart_unicode
import hashlib

import logging, traceback, time, struct, socket
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

logger = logging.getLogger('default')
from content_engine import settings
from portal.tables import SearchResultTable
from portal.models import Game, Puzzle
from portal.views import _auth_user, _redirect_back
from service import search_pb2
import socket

import rules
#import rules_draw
from rules_answer_puzzle import *
from rules_integral_exchange import *
from state_machine import *
from state_verify import *
import rules_base_dialog
import rules_game_search
from pyweixin import WeiXin
from router import Router
from message_builder import MessageBuilder, BuildConfig
from data_loader import load_games_for_today, load_shorten_urls

from weixin.forms import DialogForm
from weixin.models import WeixinUser, Gift, GiftItem, UserGift, UserAnswer

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from datetime import date, timedelta, datetime

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
            try:
                user = WeixinUser.objects.get(uid=message['FromUserName'])
            except:
                user = WeixinUser()
                user.src = message['ToUserName']
                user.uid = message['FromUserName']
                user.integral = 0
                user.save()

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
            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, u"非常抱歉，没能理解你的话")
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

def gifts(request, user_id=None):
    user = get_object_or_404(WeixinUser, id=user_id)

    if request.method == 'POST':
        gift_id = request.POST.get('gift_id', None)
        if gift_id is not None:
            gift = Gift.objects.get(id=int(gift_id))
            if gift.integral <= user.integral:
                giftItem = GiftItem.objects.filter(grade=gift, state=0)[0]
                giftItem.state = 1
                giftItem.save()
                user.integral -= gift.integral
                user.save()

                userGift = UserGift()
                userGift.gift = giftItem
                userGift.user = user
                userGift.save()
    
    gifts = []
    for gift in Gift.objects.filter(show=1):
        gifts.append({
            'id' : gift.id,
            'name' : gift.name,
            'integral' : gift.integral,
            'item_count' : gift.giftitem_set.filter(state=0).count(),
            'picture' : settings.MEDIA_URL + gift.picture.name
            })

    user_gifts = []
    for user_gift in UserGift.objects.filter(user=user).order_by('-getTime'):
        user_gifts.append({
            'name' : user_gift.gift.grade.name,
            'picture' : settings.MEDIA_URL + user_gift.gift.grade.picture.name,
            'value' : user_gift.gift.value,
            'get_time' : user_gift.getTime
            })

    return render(request, 'gifts.html', {'credit' : user.integral, 'gifts' : gifts, 'user_gifts' : user_gifts})

def puzzles(request, puzzle_id=None):
    user = get_object_or_404(WeixinUser, id=request.GET.get('user_id', None))

    if puzzle_id is None:
        puzzle = Puzzle.objects.filter(Q(status1=2) | Q(weixin__status2=2)).latest('sync_timestamp1')
    else:
        puzzle = get_object_or_404(Puzzle, id=puzzle_id)
    
    user_answer = UserAnswer.objects.filter(questionId=puzzle, userId=user)
    puzzle_data = {
    'id' : puzzle.id,
    'title' : puzzle.title,
    'image' : settings.MEDIA_URL + puzzle.image_url.name,
    'option1' : puzzle.option1,
    'option2' : puzzle.option2,
    'option3' : puzzle.option3,
    'option4' : puzzle.option4,
    'right' : puzzle.right,
    'description' : puzzle.description
    }
    if user_answer is not None and user_answer.count() > 0:
        puzzle_data['answered'] = True
        puzzle_data['correct'] = user_answer[0].userOption == puzzle.right
        puzzle_data['userOption'] = user_answer[0].userOption
    else:
        puzzle_data['answered'] = False
        puzzle_data['correct'] = False

    return render(request, 'puzzle.html', {'user' : user, 'puzzle' : puzzle_data})

def intro(request):
    return render(request, 'weixin_intro.html', {})