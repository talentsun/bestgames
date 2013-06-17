from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from data_loader import load_games_for_today as load_games
from data_loader import load_shorten_android_download_url, load_shorten_ios_download_url
from portal.models import Game

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