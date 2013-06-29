from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from data_loader import load_games_for_today as load_games
from data_loader import load_shorten_android_download_url, load_shorten_ios_download_url
from portal.models import Game, Puzzle
from weixin.models import WeixinUser, UserAnswer
from django.db.models import Q
from datetime import date, datetime, timedelta

@dajaxice_register
def load_games_for_today(request):
	load_games(True)
	dajax = Dajax()
	return dajax.json()

@dajaxice_register
def begin_load_shorten_urls(request, offset=0):
	index = 0
	for game in Game.objects.all()[offset:]:
		load_shorten_ios_download_url(game, True)
		load_shorten_android_download_url(game, True)
		index += 1
		print index
		if index >= 2:
			break
	dajax = Dajax()
	print 'total:%d' % Game.objects.count()
	print 'offset:%d' % (offset+index)
	print 'percent:%d' % int((offset+index)*100//Game.objects.count())
	dajax.add_data({'offset':offset+index, 'percent':int((offset+index)*100//Game.objects.count())}, 'load_shorten_urls_callback')
	return dajax.json()

@dajaxice_register
def answer_puzzle(request, user_id, puzzle_id, option):
	puzzle = Puzzle.objects.get(pk=puzzle_id)
	user = WeixinUser.objects.get(pk=user_id)
	user_answer = UserAnswer(questionId=puzzle, userId=user, userOption=option)
	user_answer.save()

	correct = False
	if int(user_answer.userOption) == puzzle.right:
		correct = True
		user.integral += 5
		user.save()

	dajax = Dajax()
	dajax.add_data({'correct' : correct, 'credit' : user.integral, 'user_option' : option}, 'answer_puzzle_callback')
	return dajax.json()

@dajaxice_register
def load_puzzle(request, user_id, puzzle_id):
	dajax = Dajax()
	dajax.redirect('/weixin/puzzles/%d?user_id=%d' % (puzzle_id, user_id), 0)
	return dajax.json()

@dajaxice_register
def load_puzzles(request, user_id):
	user = WeixinUser.objects.get(pk=user_id)
	puzzles = []
	for puzzle in Puzzle.objects.filter(Q(status1=2) | Q(weixin__status2=2)).filter(sync_timestamp1__range=(date.today()-timedelta(days=2), datetime.today())).order_by('-sync_timestamp1'):
		user_answer = UserAnswer.objects.filter(questionId=puzzle, userId=user)
		answered = False
		correct = False
		if user_answer is not None and user_answer.count() > 0:
			answered = True
			correct = user_answer[0].userOption == puzzle.right
		puzzles.append({
			'id' : puzzle.id,
			'title' : puzzle.title,
			'answered' : answered,
			'correct' : correct
			})

	dajax = Dajax()
	dajax.add_data({ 'puzzles' : puzzles }, 'load_puzzles_callback')
	return dajax.json()
