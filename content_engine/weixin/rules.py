# coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig
from data_loader import load_games_for_today, load_latest_game_collection

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

def get_latest_game_collection(rule, info):
    return BuildConfig(MessageBuilder.TYPE_GAME_COLLECTION, None, load_latest_game_collection())


def get_welcome(rule, info):
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"欢迎收听每日精品游戏，我喜欢你叫我小每。在这里我们人工为你在海量的游戏中，找到几个属于你的游戏，希望你喜欢。除了接收消息，你还可以做到更多的（提示：你可以回复一下帮助哟!）")

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

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
        'name' : u'获取今日精品游戏推荐',
        'pattern' : u'^(游戏|推荐)$',
        'handler' : get_games_for_today
    })
Router.get_instance().set({
        'name' : u'获取本周游戏合集',
        'pattern' : u'合集',
        'handler' : get_latest_game_collection
    })
Router.get_instance().set({
        'name' : u'打招呼',
        'pattern' : u'.*(你好|hi|hello|您好).*',
        'handler' : ['你好喽','小每祝您全家发财','好毛啊好']
    })
Router.get_instance().set({
        'name' : u'有病',
        'pattern' : u'.*有病.*',
        'handler' : ['你有药啊！','你妹啊！','春了吧。。。']
    })
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

help_wording = u"""你可以通过输入下面五类句子来使用小每:
1. 推荐游戏
如果你想尝试一些新的游戏，那么就使用这一句话，小每将给你推荐几款好玩的新游戏。
2.推荐画面精美的赛车游戏
如果你有特定的口味，那么小每将给你推荐好玩的画面精美的赛车游戏，你可以将画面精美的赛车游戏换成任何词
3.推荐和植物大战僵尸类似的游戏
那么小每将给你找和植物大战僵尸类似的游戏，你可以将植物大战僵尸换成你玩过的好游戏的名字
4.下载魔法庄园
如果你有自己想玩的游戏，比如魔法庄园，那么小每将给你找到魔法庄园的下载地址
5.帮助
小每将告诉你最新的使用指南"""
Router.get_instance().set({
    'name' : u'帮助说明',
    'pattern' : u'帮助|使用说明',
    'handler' : help_wording
})
