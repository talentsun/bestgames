# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput
from datetime import datetime
from taggit.forms import TagField
from django_select2 import *

from api.models import Redier, Game, Category, Collection

class EntityForm(ModelForm):
	tags = TagField(label=u"标签", help_text=u"使用英文逗号\",\"分隔不同标签")
	brief_comment = forms.CharField(label=u"一句话点评", help_text=u"20字以内（作为图文消息的标题同步到微信）", required=True, max_length=20)
	recommended_reason = forms.CharField(label=u"推荐理由", help_text=u"120字以内（作为微博内容同步到新浪微博）", required=True, max_length=160, widget=forms.Textarea())
	weibo_sync_timestamp = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
				'autoclose' : 'true',
				'showMeridian' : 'true',
				'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				}))

class RedierForm(EntityForm):
	game = forms.ModelChoiceField(queryset=Game.objects.all(), empty_label=u"选择游戏", label=u"游戏")

	class Meta:
		model = Redier
		fields = ('game',
			'title', 
			'redier_image',
			'tags',
			'weibo_sync_timestamp',
			'presenter',
			'rating',
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
			'rating',
			'brief_comment',
			'recommended_reason')