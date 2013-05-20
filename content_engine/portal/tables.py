# -*- coding: utf-8 -*-
from weixin.models import BaseDialog
from portal.models import Game, Redier, Collection, Problem,Weixin,Player,GameAdvices
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
        return game_name_list[0:len(game_name_list) - 2]

class GameAdviceColumn(tables.Column):
    def render(self, value):
        game_advice_list = ''
        game_advice_set = value.get_query_set()
        for game_info in game_advice_set:
            game_advice_list = game_advice_list + game_info.title + ', '
        return game_advice_list[0:len(game_advice_list) - 2]

class PlayerColumn(tables.Column):
    def render(self, value):
        player_list = ''
        player_set = value.get_query_set()
        for player in player_set:
            player_list = player_list + player.title + ', '
        return player_list[0:len(player_list) - 2]


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
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(verbose_name=u'名称', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"}, verbose_name=u'标签')
    ops = TemplateColumn(template_name="game_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = Game
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无精品游戏推荐"
        fields = ("name","presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("name","presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class RedierTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    game_name = tables.Column(verbose_name=u'游戏', orderable=False)
    title = tables.Column(verbose_name=u'标题', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="redier_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Redier
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无小兵变大咖"
        fields = ("game_name","title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("game_name","title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class CollectionTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="collection_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Collection
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无游戏合集"
        fields = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class WeixinTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微信同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    games = GameColumn(verbose_name=u"游戏名称",orderable=False,attrs={"class":"games"})
    advices = GameAdviceColumn(verbose_name=u"游戏情报站",orderable=False,attrs={"class":"advices"})
    players = PlayerColumn(verbose_name=u"我是玩家",orderable=False,attrs={"class": "players"})


    ops = TemplateColumn(template_name="weixin_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Weixin
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无微信消息"
        fields = ("title", "presenter","weibo_sync_timestamp","status","games","advices","players","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","games","advices","players","ops")
        attrs = {'class' : 'table table-striped'}


class ProblemTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="problem_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Problem
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无\"宅，必有一技\""
        fields = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}


class PlayerTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="player_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Player
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无\"我是玩家\""
        fields = ("title", "presenter","weibo_sync_timestamp","status","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","ops")
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

class GameAdvicesTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="game_advices_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = GameAdvices
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无\"游戏情报站\""
        fields = ("title", "presenter","weibo_sync_timestamp","status","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","ops")
        attrs = {'class' : 'table table-striped'}


