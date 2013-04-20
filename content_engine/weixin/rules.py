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


def get_welcome(rule, info):
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"""欢迎收听小每（全称每日精品游戏)。这里是游戏者的乐园，每天都会有经过人工精挑细选的好游戏呈上。回复“滑雪大冒险”，获得滑雪大冒险游戏的下载地址～\n回复“恐怖”将获得恐怖类的游戏～\n回复“推荐”我们将随机给你随机推荐好游戏～""")

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

def match_subscribe_event(rule, info):
    return info.type == "event" and info.event == 'subscribe'

def match_unsubscribe_event(rule, info):
    return info.type == "event" and info.event == 'unsubscribe'

"""
Router.get_instance().set({
        'name' : u'获取今日精品推荐游戏的下载地址',
        'pattern' : u'^下载$',
        'handler' : get_download_urls_for_today
    })
"""
Router.get_instance().set({
        'name' : u'获取随机推荐的游戏',
        'pattern' : u'^(推荐|下载)$',
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
        'handler' : ['你好，有什么想玩的吗？试着给小每描述一下你想玩的游戏吧！']
    })
Router.get_instance().set({
        'name' : u'自我介绍',
        'pattern' : u'^你是谁.*',
        'handler' : ['我是小每呀（全程每日精品游戏）,我们团队要为游戏爱好者解决找游戏和玩游戏遇到的困难，让玩家得到更好的游戏体验，感谢对我们的支持']
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

help_wording = u"""你可以通过以下3种方式来使用小每:
1、输入游戏名字
比如你想玩滑雪大冒险，就输入滑雪大冒险
2、找特定类型的游戏
比如你想玩赛车游戏，就输入赛车即可
3、推荐
如果你想让小每帮你随机推荐几款好游戏就输入推荐"""
Router.get_instance().set({
    'name' : u'帮助说明',
    'pattern' : u'^(帮助|使用说明)$',
    'handler' : help_wording
})
