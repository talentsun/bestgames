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

Router.get_instance().set({
		'name' : u'获取今日精品推荐游戏的下载地址',
		'pattern' : u'下载',
		'handler' : get_download_urls_for_today
	})
Router.get_instance().set({
		'name' : u'获取今日精品游戏推荐',
		'pattern' : u'(游戏|推荐)',
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