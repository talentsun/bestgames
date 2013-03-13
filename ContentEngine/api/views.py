# -*- coding: utf-8 -*-
import sys
import os

from django.template import loader,Context
from django.http import HttpResponse
from sina.sinaAuth import SinaAuth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404, render, redirect
from taggit.models import Tag
from django.conf import settings

from api.models import Game, Redier
from api.tables import GameTable, RedierTable
from api.forms import GameForm, RedierForm

import django_tables2 as tables

def index(request):
    games = GameTable(Game.objects.all(),prefix="hg-")
    games.paginate(page=request.GET.get("hg-page",1), per_page=10)
    games.data.verbose_name = u"精品游戏推荐"

    rediers = RedierTable(Redier.objects.all(),prefix="gr-")
    rediers.paginate(page=request.GET.get("gr-page",1), per_page=10)
    rediers.data.verbose_name = u"小兵变大咖"

    return render(request, "index.html", {"games": games, "rediers":rediers})

def auth(request):
    auth = SinaAuth()
    return HttpResponseRedirect(auth.getAuthorizeUrl())

def sina_login(request):
    code = request.GET.get('code')
    print code
    auth = SinaAuth()
    print auth.getToken(code)
    if auth is None:
        return HttpResponseRedirect("/")
    else:
        username = 'admin'
        password = 'admin'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print 'login success'
                return HttpResponseRedirect("/")

def add_rediers(request):
    form = RedierForm()
    return render(request, "add_edit_redier.html", { "form": form })

def add_edit_game(request, game_id=None):
    if game_id:
        game = get_object_or_404(Game, entity_ptr_id=game_id)
    else:
        game = None

    if request.method == "POST":
        form = GameForm(request.POST, request.FILES,instance=game)
        if form.is_valid():
            game = form.save()
            if request.POST['icon']:
                game.icon = request.POST['icon'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.icon = request.POST['icon']
            if request.POST['screenshot_path_1']:
                game.screenshot_path_1 = request.POST['screenshot_path_1'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.screenshot_path_1 = request.POST['screenshot_path_1']
            if request.POST['screenshot_path_2']:
                game.screenshot_path_2 = request.POST['screenshot_path_2'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.screenshot_path_2 = request.POST['screenshot_path_2']
            if request.POST['screenshot_path_3']:
                game.screenshot_path_3 = request.POST['screenshot_path_3'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.screenshot_path_3 = request.POST['screenshot_path_3']
            if request.POST['screenshot_path_4']:
                game.screenshot_path_4 = request.POST['screenshot_path_4'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.screenshot_path_4 = request.POST['screenshot_path_4']
            if request.POST['screenshot_path_5']:
                game.screenshot_path_5 = request.POST['screenshot_path_5'].replace(settings.MEDIA_URL, '', 1)
            else:
                game.screenshot_path_5 = request.POST['screenshot_path_5']
            game.save()
            return HttpResponseRedirect('/')

    else:
        form = GameForm(instance=game)
    return render(request, "add_edit_game.html", { "form" : form, "tags" : Tag.objects.all() })

def delete_game(request, game_id=None):
    if game_id:
        game = get_object_or_404(Game, entity_ptr_id=game_id)
        if game is not None:
            game.delete()
            return HttpResponseRedirect("/")

def completed(request):
    return render(request, "completed.html")

