# coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig
from data_loader import load_games_for_today, load_latest_game_collection, load_random_games

def get_download_urls_for_today(rule, info):
    games = load_games_for_today()
    if games is not None and len(games) > 0:
        return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, games)
    else:
        collection = load_latest_game_collection()
        if collection is not None and collection.games.count() > 0:
            return BuildConfig(MessageBuilder.TYPE_GAME_COLLECTION, None, collection.games.all())
        else:
            return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'小每今天累屎了，没有推荐游戏[[哭]]')

def get_games_for_today(rule, info):
    games = load_games_for_today()
    if games is not None and len(games) > 0:
        return BuildConfig(MessageBuilder.TYPE_GAMES, None, games)
    else:
        collection = load_latest_game_collection()
        if collection is not None and collection.games.count() > 0:
            return get_latest_game_collection(rule, info)
        else:
            return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'小每今天累屎了，没有推荐游戏[[哭]]')

def get_random_games(rule, info):
    games = load_random_games()
    return BuildConfig(MessageBuilder.TYPE_GAMES, None, games)
    

def get_latest_game_collection(rule, info):
    return BuildConfig(MessageBuilder.TYPE_GAME_COLLECTION, None, load_latest_game_collection())

def voice_message(rule, info):
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"非常抱歉，小每还不能理解语音信息，现在你可以用文字和小每交流")

def get_welcome(rule, info):
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"""您好，小每立志成为一个您身边的手机游戏砖家，您可以和小每对话，让小每来帮您：
1. 找游戏的下载地址
回复游戏的名字，例如“滑雪大冒险”
2. 推荐好玩的游戏
回复“推荐”，每次回复都有不同的游戏哟，
3. 根据您的喜好找好玩的游戏
回复描述游戏的词，例如“赛车”，“恐怖”""")

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

def match_voice_message(rule, info):
    return info.type == 'voice'

def match_subscribe_event(rule, info):
    return info.type == "event" and info.event == 'subscribe'

def match_unsubscribe_event(rule, info):
    return info.type == "event" and info.event == 'unsubscribe'

Router.get_instance().set({
        'name' : u'获取今日精品推荐游戏的下载地址',
        'pattern' : u'^下载$',
        'handler' : get_download_urls_for_today
    })
Router.get_instance().set({
        'name' : u'获取随机推荐的游戏',
        'pattern' : u'^(推荐)$',
        'handler' : get_random_games
    })
Router.get_instance().set({
        'name' : u'获取今日精品游戏推荐',
        'pattern' : u'^(今日推荐)$',
        'handler' : get_games_for_today
    })
"""
Router.get_instance().set({
        'name' : u'获取本周游戏合集',
        'pattern' : u'合集',
        'handler' : get_latest_game_collection
    })
"""
Router.get_instance().set({
        'name' : u'打招呼',
        'pattern' : u'^(你好|hi|hello|您好).*',
        'handler' : ['''你好，小每立志成为一个您身边的手机游戏砖家，您可以和小每对话，让小每来帮您：
1. 找游戏的下载地址
回复游戏的名字，例如“滑雪大冒险”
2. 推荐好玩的游戏
回复“推荐”，每次回复都有不同的游戏哟，
3. 根据您的喜好找好玩的游戏
回复描述游戏的词，例如“赛车”，“恐怖”''']
    })
Router.get_instance().set({
        'name' : u'自我介绍',
        'pattern' : u'(^你是谁.*)|(小每)',
        'handler' : ['''我是小每呀，立志成为一个您身边的手机游戏砖家，您可以和小每对话，让小每来帮您：
1. 找游戏的下载地址
回复游戏的名字，例如“滑雪大冒险”
2. 推荐好玩的游戏
回复“推荐”，每次回复都有不同的游戏哟，
3. 根据您的喜好找好玩的游戏
回复描述游戏的词，例如“赛车”，“恐怖”''']
    })
"""
Router.get_instance().set({
        'name' : u'有病',
        'pattern' : u'.*有病.*',
        'handler' : ['你有药啊！','你妹啊！','春了吧。。。']
    })
"""
Router.get_instance().set({
        'name' : u'收听致辞',
        'pattern' : match_subscribe_event,
        'handler' : get_welcome
    })
Router.get_instance().set({
        'name' : u'取消收听',
        'pattern' : match_unsubscribe_event,
        'handler' : unsubscribe
    })
Router.get_instance().set({
        'name' : u'声音消息',
        'pattern' : match_voice_message,
        'handler' : voice_message
    })

help_wording = u"""小每立志成为一个您身边的手机游戏砖家，您可以和小每对话，让小每来帮您：
1. 找游戏的下载地址
回复游戏的名字，例如“滑雪大冒险”
2. 推荐好玩的游戏
回复“推荐”，每次回复都有不同的游戏哟，
3. 根据您的喜好找好玩的游戏
回复描述游戏的词，例如“赛车”，“恐怖”
4. 积分商城
回复“礼品”查看自己的积分并获取礼品"""
Router.get_instance().set({
    'name' : u'帮助说明',
    'pattern' : u'^(帮助|使用说明)$',
    'handler' : help_wording
})
