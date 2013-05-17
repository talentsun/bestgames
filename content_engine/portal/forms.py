# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput
from datetime import datetime
from taggit.forms import TagField
from django_select2 import *

from portal.models import Redier, Game, Category, Collection, Problem,Weixin,Player,GameAdvices

class EntityForm(ModelForm):
	tags = TagField(label=u"标签",required=False)
	brief_comment = forms.CharField(label=u"一句话点评", help_text=u"20字以内（作为图文消息的标题同步到微信）", required=False, max_length=20)
	recommended_reason = forms.CharField(label=u"推荐理由", help_text=u"150字以内（作为微博内容同步到新浪微博）", required=False, max_length=150, widget=forms.Textarea())
	weibo_sync_timestamp = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
				'autoclose' : 'true',
				'showMeridian' : 'true',
				'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				}))

class RedierForm(EntityForm):
	class Meta:
		model = Redier
		fields = ('game_name',
			'title', 
			'redier_image',
			'tags',
			'weibo_sync_timestamp',
			'presenter',
			'brief_comment',
			'recommended_reason')
		widgets = {
			'redier_image' : AjaxClearableFileInput()}

class GameForm(EntityForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=u"选择分类", label=u"分类")

	class Meta:
		model = Game
		fields = ('name', 
			'icon', 
			'description', 
			'category',
			'tags',
			'android_download_url', 
			'iOS_download_url', 
			'screenshot_path_1', 
			'screenshot_path_2', 
			'screenshot_path_3', 
			'screenshot_path_4', 
			'weibo_sync_timestamp',
			'presenter',
			'rating',
			'brief_comment',
			'recommended_reason')
		widgets = {
			'icon' : AjaxClearableFileInput(),
			'screenshot_path_1' : AjaxClearableFileInput(),
			'screenshot_path_2' : AjaxClearableFileInput(),
			'screenshot_path_3' : AjaxClearableFileInput(),
			'screenshot_path_4' : AjaxClearableFileInput()}

class GameChoices(AutoModelSelect2MultipleField):
	queryset = Game.objects
	search_fields = ['name__icontains',]

class CollectionForm(EntityForm):
    cover = forms.ImageField(label=u"封面图片", help_text=u"建议使用640x320大小的图片", widget=AjaxClearableFileInput())
    games = GameChoices(label=u"游戏")

	class Meta:
		model = Collection
		fields = ('title',
			'cover',
			'games',
			'tags',
			'weibo_sync_timestamp',
			'presenter',
			'brief_comment',
			'recommended_reason')

class GameAdviceChoices(AutoModelSelect2MultipleField):
    queryset = GameAdvices.objects
    search_fields = ['name__icontains',]

class WeixinForm(EntityForm):
    cover = forms.ImageField(label=u"封面图片", help_text=u"建议使用640x320大小的图片", widget=AjaxClearableFileInput(),required=False)
    games = GameChoices(label=u"游戏")
    gameAdvices = GameAdviceChoices(label=u"游戏情报站")

    class Meta:
        model = Weixin
        fields = ('title',
                  'cover',
                  'games',
                  'gameAdvices',
                  'weibo_sync_timestamp',
                  'presenter',
                  'recommended_reason'
                  )

class ProblemForm(EntityForm):
	problem_image = forms.ImageField(label=u"必有一技", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())

	class Meta:
		model = Problem
		fields = ('title',
			'problem_image',
			'tags',
			'weibo_sync_timestamp',
			'presenter',
			'brief_comment',
			'recommended_reason')

class PlayerForm(EntityForm):
    player_image = forms.ImageField(label=u"我是玩家", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())

    class Meta:
        model = Player
        fields = ('title',
                  'player_image',
                  'weibo_sync_timestamp',
                  'presenter',
                  'recommended_reason')

class GameAdvicesForm(EntityForm):
    advice_image = forms.ImageField(label=u"游戏情报站", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())

    class Meta:
        model = GameAdvices
        fields = ('title',
                  'advice_image',
                  'weibo_sync_timestamp',
                  'presenter',
                  'recommended_reason')