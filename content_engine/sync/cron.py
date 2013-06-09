#encoding=utf-8
import cronjobs
import datetime
from portal.models import Game, Redier, Collection, Problem, Entity, Weixin, Player, GameAdvices
from message_sender import MessageSender
import weibo_message_builder
import weixin_message_builder
import web_message_builder

@cronjobs.register
def sync():
	sync_weibo()
	sync_weixin()
	sync_web()

@cronjobs.register
def sync_weibo():
	# query entities needed to sync
	entities = Entity.objects.filter(sync_timestamp1__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(hours=4)), status1=1)
	for entity in entities:
		weibo_message = None
		if entity.type == Entity.GAME:
			weibo_message = weibo_message_builder.build_game_message(Game.objects.get(id=entity.id))
		elif entity.type == Entity.REDIER:
			weibo_message = weibo_message_builder.build_redier_message(Redier.objects.get(id=entity.id))
		elif entity.type == Entity.COLLECTION:
			weibo_message = weibo_message_builder.build_collection_message(Collection.objects.get(id=entity.id))
		elif entity.type == Entity.PROBLEM:
			weibo_message = weibo_message_builder.build_problem_message(Problem.objects.get(id=entity.id))
		elif entity.type == Entity.PLAYER:
			weibo_message = weibo_message_builder.build_player_message(Player.objects.get(id=entity.id))
		elif entity.type == Entity.GAMEADVICE:
			weibo_message = weibo_message_builder.build_news_message(GameAdvices.objects.get(id=entity.id))
		if weibo_message is not None:
			MessageSender.send_weibo(weibo_message)

@cronjobs.register
def sync_weixin():
	#query weixin messages
	weixin_msgs = Weixin.objects.filter(sync_timestamp2__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=5)), status2=1)
	for msg in weixin_msgs:
		MessageSender.send_weixin(weixin_message_builder.build_weixin_message(msg))

@cronjobs.register
def sync_web():
	#query entities needed to sync
	entities = Entity.objects.filter(sync_timestamp3__range=(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=5)), status3=1)
	for entity in entities:
		web_message = None
		if entity.type == Entity.GAME:
			web_message = web_message_builder.build_game_message(Game.objects.get(id=entity.id))
		if weibo_message is not None:
			MessageSender.send_web(web_message)