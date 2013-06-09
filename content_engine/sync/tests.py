#encoding=utf-8
from breve import Template, flatten
from breve.tags.html import tags

def build_game_message(game):
    t = Template(tags, root='./templates/')
    content = t.render('game', game)
    return content

content = build_game_message(dict(
	screenshot_path_1 = 'http://cow.bestgames7.com/media/best_games/2013-05-28/21-35-43.jpg',
	screenshot_path_2 = 'http://cow.bestgames7.com/media/best_games/2013-05-28/21-35-46.jpg',
	screenshot_path_3 = 'http://cow.bestgames7.com/media/best_games/2013-05-28/21-35-49.jpg',
	screenshot_path_4 = 'http://cow.bestgames7.com/media/best_games/2013-05-28/21-35-52.jpg'
	))

print content