# -*- coding: utf-8 -*-
from weixin.models import BaseDialog, Gift, GiftItem
from portal.models import Game, Redier, Collection, Problem, Weixin, Player, News, Puzzle
import django_tables2 as tables
from django_tables2.columns import DateTimeColumn, TemplateColumn
from taggit.utils import edit_string_for_tags

class TagColumn(tables.Column):
    def render(self, value):
        return edit_string_for_tags(value.get_query_set())

class GameColumn(tables.Column):
    def render(self, value):
        game_name_list = ''
        game_set = value.get_query_set()
        for game_info in game_set:
            game_name_list = game_name_list + game_info.name + ', '
        if len(game_name_list) > 0:
            return game_name_list[0:len(game_name_list) - 2]
        else:
            return u'—'

class NewsColumn(tables.Column):
    def render(self, value):
        news_list = ''
        news_set = value.get_query_set()
        for game_info in news_set:
            news_list = news_list + game_info.title + ', '
        if len(news_list) > 0:
            return news_list[0:len(news_list) - 2]
        else:
            return u'—'

class PlayerColumn(tables.Column):
    def render(self, value):
        player_list = ''
        player_set = value.get_query_set()
        for player in player_set:
            player_list = player_list + player.title + ', '
        if len(player_list) > 0:
            return player_list[0:len(player_list) - 2]
        else:
            return u'—'

class PuzzleColumn(tables.Column):
    def render(self, value):
        puzzle_list = ''
        puzzle_set = value.get_query_set()
        for puzzle in puzzle_set:
            puzzle_list = puzzle_list + puzzle.title + ', '
        if len(puzzle_list) > 0:
            return puzzle_list[0:len(puzzle_list) - 2]
        else:
            return u'—'


class SearchResultTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(orderable=False)
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    
    class Meta:
        model = Game
        empty_text = u"暂无精品游戏推荐"
        fields = ("entity_ptr_id", "name","tags","category", "description", "nameRel", "gameRel")
        sequence = fields
        attrs = {'class' : 'table table-striped'}

class GameTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    name = tables.Column(verbose_name=u'名称', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="game_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = Game
        order_by = "-id"
        empty_text = u"暂无精品游戏推荐"
        fields = ("name","presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("name","presenter","sync_timestamp1", "sync_timestamp3", "status","ops")
        attrs = {'class' : 'table table-striped'}

class RedierTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    game_name = tables.Column(verbose_name=u'游戏', orderable=False)
    title = tables.Column(verbose_name=u'标题', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="redier_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Redier
        order_by = "-id"
        empty_text = u"暂无小兵变大咖"
        fields = ("game_name","title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("game_name","title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}

class CollectionTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="collection_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Collection
        order_by = "-id"
        empty_text = u"暂无游戏合集"
        fields = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}

class WeixinTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    sync_timestamp2 = DateTimeColumn(verbose_name=u"微信同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    games = GameColumn(verbose_name=u"游戏名称",orderable=False,attrs={"class":"games"})
    news = NewsColumn(verbose_name=u"游戏情报站",orderable=False,attrs={"class":"news"})
    players = PlayerColumn(verbose_name=u"我是玩家",orderable=False,attrs={"class": "players"})
    puzzles = PuzzleColumn(verbose_name=u"趣题",orderable=False,attrs={"class": "puzzles"})

    ops = TemplateColumn(template_name="weixin_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Weixin
        order_by = "-id"
        empty_text = u"暂无微信消息"
        fields = ("news","games","players","puzzles","sync_timestamp2","status","ops")
        sequence = ("news","games","players","puzzles","sync_timestamp2","status","ops")
        attrs = {'class' : 'table table-striped'}


class ProblemTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="problem_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Problem
        order_by = "-id"
        empty_text = u"暂无\"宅，必有一技\""
        fields = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}


class PlayerTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="player_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Player
        order_by = "-id"
        empty_text = u"暂无\"我是玩家\""
        fields = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}

class DialogTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    question = tables.Column(orderable=False)
    answer = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    ops = TemplateColumn(template_name="dialog_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = BaseDialog 
        empty_text = u"暂无\"基本对话\""
        fields = ("id", "question", "answer", "presenter" ,"ops")
        sequence = ("id", "question", "answer", "presenter" ,"ops")
        attrs = {'class' : 'table table-striped'}

class NewsTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="news_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = News
        order_by = "-id"
        empty_text = u"暂无\"游戏情报站\""
        fields = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}


class PuzzleTable(tables.Table):
    id = tables.Column(orderable=True)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_timestamp1 = DateTimeColumn(verbose_name=u"微博同步时间",orderable=False)
    sync_timestamp3 = DateTimeColumn(verbose_name=u"网站同步时间",orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="puzzle_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})


    class Meta:
        model = Puzzle
        order_by = "-id"
        empty_text = u"暂无\"趣题\""
        fields = ("id", "title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        sequence = ("id", "title", "presenter","sync_timestamp1","sync_timestamp3","status","ops")
        attrs = {'class' : 'table table-striped'}

class GiftTable(tables.Table):
    ops = TemplateColumn(template_name="gift_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = Gift
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'show', 'integral', 'cost')
        orderable = False



class GiftItemTable(tables.Table):
    grade = tables.Column(verbose_name=u"礼品类型", accessor='grade.name')
    ops = TemplateColumn(template_name="gift_item_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = GiftItem
        order_by = '-state'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        exclude = ('id',)

