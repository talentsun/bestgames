# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput
from datetime import datetime
from taggit.forms import TagField
from django_select2 import *
from weixin.models import Gift, GiftItem

from portal.models import Redier, Game, Category, Collection, Problem, Weixin, Player, News, Puzzle

class EntityForm(ModelForm):
    tags = TagField(label=u"标签",required=False)
    brief_comment = forms.CharField(label=u"一句话点评", help_text=u"20字以内（作为图文消息的标题同步到微信）", required=False, max_length=20)
    recommended_reason = forms.CharField(label=u"推荐理由", help_text=u"150字以内（作为微博内容同步到新浪微博）", required=False, max_length=150, widget=forms.Textarea())

class RedierForm(EntityForm):
    image_url = forms.ImageField(label=u"图片", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Redier
        fields = ('game_name',
            'title', 
            'image_url',
            'video_url',
            'tags',
            'sync_timestamp1',
            'sync_timestamp3',
            'presenter',
            'brief_comment',
            'recommended_reason')

class GameForm(EntityForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=u"选择分类", label=u"分类")
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

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
            'sync_timestamp1',
            'sync_timestamp3',
            'presenter',
            'rating',
            'size',
            'video_url',
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
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Collection
        fields = ('title',
            'cover',
            'video_url',
            'games',
            'tags',
            'sync_timestamp1',
            'sync_timestamp3',
            'presenter',
            'brief_comment',
            'recommended_reason')

class NewsChoices(AutoModelSelect2MultipleField):
    queryset = News.objects
    search_fields = ['title__icontains',]

class PlayerChoices(AutoModelSelect2MultipleField):
    queryset = Player.objects
    search_fields = ['title__icontains',]

class PuzzleChoices(AutoModelSelect2MultipleField):
    queryset = Puzzle.objects
    search_fields = ['title__icontains',]

class WeixinForm(EntityForm):
    cover = forms.ImageField(label=u"封面图片", help_text=u"建议使用640x320大小的图片", widget=AjaxClearableFileInput(),required=False)
    games = GameChoices(label=u"游戏推荐", required = False)
    news = NewsChoices(label=u"游戏情报站", required = False)
    players = PlayerChoices(label=u"我是玩家", required = False)
    puzzles = PuzzleChoices(label=u'趣题', required = False)
    sync_timestamp2 = forms.DateTimeField(label=u"微信同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Weixin
        fields = ('title',
                  'cover',
                  'games',
                  'news',
                  'players',
                  'puzzles',
                  'sync_timestamp2',
                  'presenter',
                  'recommended_reason'
                  )

class ProblemForm(EntityForm):
    image_url = forms.ImageField(label=u"图片", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Problem
        fields = ('title',
            'image_url',
            'video_url',
            'tags',
            'sync_timestamp1',
            'sync_timestamp3',
            'presenter',
            'brief_comment',
            'recommended_reason')

class PlayerForm(EntityForm):
    image_url = forms.ImageField(label=u"图片", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Player
        fields = ('title',
                  'image_url',
                  'video_url',
                  'sync_timestamp1',
                  'sync_timestamp3',
                  'presenter',
                  'brief_comment',
                  'recommended_reason')

class NewsForm(EntityForm):
    image_url = forms.ImageField(label=u"图片", help_text=u"建议图片宽度大于400像素", widget=AjaxClearableFileInput())
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = News
        fields = ('title',
                  'image_url',
                  'video_url',
                  'sync_timestamp1',
                  'sync_timestamp3',
                  'presenter',
                  'brief_comment',
                  'recommended_reason')


class PuzzleForm(EntityForm):
    image_url = forms.ImageField(label=u'题目图片', widget=AjaxClearableFileInput(), required = False)
    sync_timestamp1 = forms.DateTimeField(label=u"微博同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    sync_timestamp3 = forms.DateTimeField(label=u"网站同步时间", required=False, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))

    class Meta:
        model = Puzzle
        fields = (
            "title",
            'image_url',
            'sync_timestamp1',
            'sync_timestamp3',
            'presenter',
            'description',
            'option1',
            'option2',
            'option3',
            'option4',
            'right')

class GiftForm(ModelForm):
    picture = forms.ImageField(label=u'礼物图片', widget=AjaxClearableFileInput(), required = False)
    class Meta:
        model = Gift

class GiftItemForm(ModelForm):
    """
    grade = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        super(GiftItemForm, self).__init__(*args, **kwargs)
        self.fields['grade'].choices = []
        for i in Gift.objects.all():
            self.fields['grade'].choices.append((i.id, i.name))

    """
    class Meta:
        model = GiftItem
        fields = ("grade", 'value')
