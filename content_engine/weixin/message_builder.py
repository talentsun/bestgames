# -*- coding: utf-8 -*-
from inspect import isfunction
from pyweixin import WeiXin
from datetime import datetime
import logging

from django.core.cache import cache
logger = logging.getLogger("default")

from data_loader import load_shorten_android_download_url, load_shorten_ios_download_url

class BuildConfig:
    def __init__(self, type, platform, data):
        self.type = type
        self.platform = platform
        self.data = data

    type = None
    platform = None
    data = None

def _build_weixin_download_urls(context, data):
    content = ''
    for game in data:
        content = content + game.name + '\n'
        logger.debug("android %s iOS %s" % (game.android_download_url, game.iOS_download_url))

        if game.android_download_url is not None and len(game.android_download_url) > 0:
            android_download_shorten_url = load_shorten_android_download_url(game)

            if android_download_shorten_url is not None:
                content = content + u'安卓下载地址'
                content = content + android_download_shorten_url + '\n'
            else:
                content = content + u'无安卓版\n'
        else:
            content = content + u'无安卓版\n'

        if game.iOS_download_url is not None and len(game.iOS_download_url) > 0:
            ios_download_shorted_url = load_shorten_ios_download_url(game)

            if ios_download_shorted_url is not None:
                content = content + u'苹果下载地址'
                content = content + ios_download_shorted_url + '\n'
            else:
                content = content + u'无苹果版\n'
        else:
            content = content + u'无苹果版\n'
            
        content = content + '\n'

    return WeiXin.to_text_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            content=content,
            func_flag=0)

def _build_weixin_games(context, data):
    articles = []
    is_first = True
    for game in data:
        url_pos = game.recommended_reason.find('http://')
        if url_pos != -1:
            description = game.recommended_reason[:url_pos]
        else:
            description = game.recommended_reason
        if is_first:
            pic_url = 'http://weixin.bestgames7.com/media/%s' % game.screenshot_path_1
            title = game.name
            is_first = False
        else:
            pic_url = 'http://weixin.bestgames7.com/media/%s' % game.icon
            title = '%s - %s' % (game.brief_comment.strip(), game.name)
        url = 'http://weixin.bestgames7.com/games/%d/preview' % game.id

        articles.append({'title' : title, 'description' : description, 'pic_url' : pic_url, 'url' : url})
    resp = WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles)
    logger.debug("len %d %s" % (len(resp), resp))
    return resp

def _build_weixin_gift_shop(context, data):
    articles = []
    articles.append({'title' : u'积分商城', 'description' : u'使用积分在积分商城兑换您心仪的礼品。', 'pic_url' : 'http://cow.bestgames7.com/static/img/giftshop.png', 'url' : 'http://cow.bestgames7.com/weixin/gifts/%d' % data})
    return WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles)

def _build_weixin_answer(context, data):
    articles = []
    articles.append({'title' : u'趣味答题', 'description' : u'每天一道题，答对一题得5分，积分可以换奖品。', 'pic_url' : 'http://cow.bestgames7.com/static/img/puzzle.png', 'url' : 'http://cow.bestgames7.com/weixin/puzzles?user_id=%d' % data})
    return WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles)

def _build_weixin_game_collection(context, data):
    articles = []
    
    articles.append({'title' : u'游戏合集之' + data.title, 'description' : u'游戏合集' + data.recommended_reason, 'pic_url' : 'http://weixin.bestgames7.com/media/%s' % data.cover, 'url' : 'http://weixin.bestgames7.com/collections/%d/preview' % data.id})
    for game in data.games.all()[:3]:
        title = '%s - %s' % (game.brief_comment, game.name)
        url_pos = game.recommended_reason.find('http://')
        if url_pos != -1:
            description = game.recommended_reason[:url_pos]
        else:
            description = game.recommended_reason
        pic_url = 'http://weixin.bestgames7.com/media/%s' % game.icon
        url = 'http://weixin.bestgames7.com/games/%d/preview' % game.id
        
        articles.append({'title' : title, 'description' : description, 'pic_url' : pic_url, 'url' : url})

    return WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles) 

def _build_weixin_intro(context, data):
    articles = []
    articles.append({'title' : u'小每 - 您身边的手机游戏砖家', 'description' : u'发现好玩的手机游戏，了解最新的手机游戏资讯，参与趣味答题赢积分换礼品。', 'pic_url' : 'http://cow.bestgames7.com/static/img/weixin-intro.jpg', 'url' : 'http://cow.bestgames7.com/weixin/intro'})
    return WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles)

def _build_weixin_raw_text(context, data):
    # FIXME
    return WeiXin.to_text_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            content=data,
            func_flag=0)

class MessageBuilder:
    # message types
    TYPE_DOWNLOAD_URL = 'type_download_url'
    TYPE_RAW_TEXT = 'type_raw_text'
    TYPE_GAMES = 'type_games'
    TYPE_GAME_COLLECTION = 'type_game_collection'
    TYPE_GIFT_SHOP = 'type_gift_shop'
    TYPE_ANSWER = 'type_answer'
    TYPE_NO_RESPONSE = 'no_response'
    TYPE_INTRO = 'intro'

    # platforms
    PLATFORM_WEIXIN = 'weixin'

    @classmethod
    def build(self,  context = None, build_config = None):
        return self._call_build_method(context, build_config.type, build_config.platform, build_config.data)

    _build_methods = {
        TYPE_DOWNLOAD_URL : {
            PLATFORM_WEIXIN : _build_weixin_download_urls
        },
        TYPE_RAW_TEXT : {
            PLATFORM_WEIXIN : _build_weixin_raw_text
        },
        TYPE_GAMES : {
            PLATFORM_WEIXIN : _build_weixin_games
        },
        TYPE_GAME_COLLECTION : {
            PLATFORM_WEIXIN : _build_weixin_game_collection
        },
        TYPE_GIFT_SHOP : {
            PLATFORM_WEIXIN : _build_weixin_gift_shop
        },
        TYPE_ANSWER : {
            PLATFORM_WEIXIN : _build_weixin_answer
        },
        TYPE_INTRO : {
            PLATFORM_WEIXIN : _build_weixin_intro
        }
    }

    @classmethod
    def _call_build_method(self, context, type, platform, data):
        if self._build_methods[type] is not None:
            if isfunction(self._build_methods[type]):
                return self._build_methods[type](context, data)
            elif self._build_methods[type][platform] is not None and isfunction(self._build_methods[type][platform]):
                return self._build_methods[type][platform](context, data)
        raise 'do not support type: %s and platform: %s' % (type, platform)
