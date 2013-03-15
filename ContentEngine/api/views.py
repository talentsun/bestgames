# -*- coding: utf-8 -*-
import sys
import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader,Context
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from taggit.models import Tag

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

def logout(request):
    auth.logout(request)
    return redirect('/')

#@login_required
def add_edit_redier(request, redier_id=None):
    if redier_id:
        redier = get_object_or_404(Redier, entity_ptr_id=redier_id)
    else:
        redier = None

    if request.method == "POST":
        form = RedierForm(request.POST, request.FILES,instance=redier)
        if form.is_valid():
            redier = form.save()
            if request.POST['redier_image']:
                redier.redier_image = request.POST['redier_image'].replace(settings.MEDIA_URL, '', 1)
            else:
                redier.redier_image = request.POST['redier_image']
            redier.save()
            return redirect('/')

    else:
        if redier is None:
            form = RedierForm(instance=redier, initial={'presenter' : request.user.username})
        else:
            form = RedierForm(instance=redier)
        
    return render(request, "add_edit_redier.html", { "form" : form, "tags" : Tag.objects.all() })

@login_required
def delete_redier(request, redier_id=None):
    if redier_id:
        redier = get_object_or_404(Redier, entity_ptr_id=redier_id)
        if redier is not None:
            redier.delete()
            return redirect("/")

#@login_required
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
            game.save()
            return redirect('/')

    else:
        if game is None:
            form = GameForm(instance=game, initial={'presenter' : request.user.username})
        else:
            form = GameForm(instance=game)
        
    return render(request, "add_edit_game.html", { "form" : form, "tags" : Tag.objects.all() })

@login_required
def delete_game(request, game_id=None):
    if game_id:
        game = get_object_or_404(Game, entity_ptr_id=game_id)
        if game is not None:
            game.delete()
            return redirect("/")

