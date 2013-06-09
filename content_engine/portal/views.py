# -*- coding: utf-8 -*-
import sys
import os
from urlparse import urlsplit

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Template,loader,Context
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
import logging, traceback, time, struct, socket

from taggit.models import Tag

from weixin.models import BaseDialog
from portal.models import Game, Redier, Collection, Problem,Entity,Weixin, Player,GameAdvices, Puzzle
from portal.tables import GameTable, RedierTable, CollectionTable, ProblemTable, WeixinTable,PlayerTable,GameAdvicesTable, DialogTable, PuzzleTable
from portal.forms import GameForm, RedierForm, CollectionForm, ProblemForm,WeixinForm,PlayerForm,GameAdvicesForm, PuzzleForm
from service import search_pb2

import django_tables2 as tables

def _redirect_back(request):
    next_url = request.GET.get('next', None)
    if next_url is None:
        return redirect('/')
    try:
        return redirect(next_url)
    except IndexError:
        return redirect('/')

def _search_game(query):
    q = search_pb2.Query()
    q.query = query
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + q.SerializeToString(), ("127.0.0.1", 8128))
    r = s.recv(4196)
    resp = search_pb2.Response()
    resp.ParseFromString(r)
    games = []
    if resp.result == 0:
        for related_game in resp.games:
            try:
                games.append(Game.objects.get(pk=related_game.gameId))
            except:
                continue
    return games

def _search_dialog(query):
    q = search_pb2.Query()
    q.query = query
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(q.SerializeToString(), ("127.0.0.1", 8038))
    r = s.recv(4196)
    resp = search_pb2.ResponseDialog()
    resp.ParseFromString(r)

    dialogs = []
    if resp.result == 0:
        for related_dialog in resp.dialogs:
            try:
                dialogs.append(BaseDialog.objects.get(pk=related_dialog.qId))
            except:
                continue
    return dialogs


def index(request):
    if request.GET.get('hg_q', None):
        games = GameTable(_search_game(request.GET.get('hg_q')),prefix='hg-')
    else:
        games = GameTable(Game.objects.all(),prefix="hg-")
    games.paginate(page=request.GET.get("hg-page",1), per_page=5)
    games.data.verbose_name = u"精品游戏推荐"

    rediers = RedierTable(Redier.objects.all(),prefix="gr-")
    rediers.paginate(page=request.GET.get("gr-page",1), per_page=5)
    rediers.data.verbose_name = u"小兵变大咖"

    collections = CollectionTable(Collection.objects.all(),prefix="co-")
    collections.paginate(page=request.GET.get("co-page",1), per_page=5)
    collections.data.verbose_name = u"游戏合集"

    problems = ProblemTable(Problem.objects.all(),prefix="pb-")
    problems.paginate(page=request.GET.get("pb-page",1), per_page=5)
    problems.data.verbose_name = u"宅，必有一技"

    weixin = WeixinTable(Weixin.objects.all(),prefix="wm-")
    weixin.paginate(page=request.GET.get("wm-page",1), per_page=5)
    weixin.data.verbose_name = u"微信消息"

    player = PlayerTable(Player.objects.all(),prefix="pr-")
    player.paginate(page=request.GET.get("pr-page",1), per_page=5)
    player.data.verbose_name = u"我是玩家"


    if request.GET.get('bd_q', None):
        dialog = DialogTable(_search_dialog(request.GET.get("bd_q")), prefix="dia-")
    else:
        dialog = DialogTable(BaseDialog.objects.all(), prefix="dia-")
    dialog.paginate(page=request.GET.get("dia-page",1), per_page=5)
    dialog.data.verbose_name = u"基本对话"


    gameAdvices = GameAdvicesTable(GameAdvices.objects.all(),prefix="ga-")
    gameAdvices.paginate(page=request.GET.get("ga-page",1), per_page=5)
    gameAdvices.data.verbose_name = u"游戏情报站"

    puzzles = PuzzleTable(Puzzle.objects.all(), prefix="pu-")
    puzzles.paginate(page=request.GET.get("pr-page",1), per_page=10)
    puzzles.data.verbose_name = u"趣题"

    return render(request, "index.html", {"games": games, "rediers":rediers, 'collections':collections, 'problems':problems, 'weixin':weixin,'player':player,'dialog': dialog, 'game_advices':gameAdvices, 'puzzles': puzzles})

def logout(request):
    auth.logout(request)
    return redirect('/')

def _auth_user(request):
    user = auth.get_user(request)
    if user.is_staff != 1:
        noauth = {'hint': '您不是管理员'}
        t = Template('{{noauth.hint}}, 必须是管理员才能更改')
        c = Context({'noauth':noauth})
        return HttpResponse(t.render(c))

@login_required
def add_edit_problem(request, problem_id=None):
    _auth_user(request)
    sync_timestamp1 = ''
    if problem_id:
        problem = get_object_or_404(Problem, entity_ptr_id=problem_id)
        sync_timestamp = problem.sync_timestamp1
    else:
        problem = None

    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES, instance=problem)
        if form.is_valid():
            problem = form.save()
            if request.POST['problem_image']:
                problem.problem_image = request.POST['problem_image'].replace(settings.MEDIA_URL, '', 1)
            else:
                problem.problem_image = request.POST['problem_image']
            if sync_timestamp1 != problem.sync_timestamp1:
                if sync_timestamp1 != '':
                    problem.status1 = Entity.STATUS_PENDING
            problem.save()
            return _redirect_back(request)
    else:
        if problem is None:
            form = ProblemForm(instance=problem, initial={'presenter' : request.user.username})
        else:
            form = ProblemForm(instance=problem)

    return render(request, 'add_edit_problem.html', {'form' : form})

@login_required
def delete_problem(request, problem_id=None):
    _auth_user(request)
    if problem_id:
        problem = get_object_or_404(Problem, entity_ptr_id=problem_id)
        if problem is not None:
            problem.delete()
            return _redirect_back(request)

@login_required
def add_edit_weixin(request, weixin_id=None):
    _auth_user(request)
    sync_timestamp2 =''
    if weixin_id:
        weixin = get_object_or_404(Weixin, entity_ptr_id=weixin_id)
        sync_timestamp2 = weixin.sync_timestamp2
    else:
        weixin = None

    if request.method == 'POST':
        form = WeixinForm(request.POST, request.FILES, instance=weixin)
        if form.is_valid():
            weixin = form.save()
            if request.POST['cover']:
                weixin.cover = request.POST['cover'].replace(settings.MEDIA_URL, '', 1)
#            else:
#                weixin.cover = request.POST['cover']
            if sync_timestamp2 != weixin.sync_timestamp2:
                if sync_timestamp2 != '':
                    weixin.status2 = Entity.STATUS_PENDING
            weixin.save()
            return _redirect_back(request)
    else:
        if weixin is None:
            form = WeixinForm(instance=weixin, initial={'presenter' : request.user.username})
        else:
            form = WeixinForm(instance=weixin)

    return render(request, 'add_edit_weixin.html', {'form' : form})

@login_required
def delete_weixin(request, weixin_id=None):
    _auth_user(request)
    weixin = get_object_or_404(Weixin, entity_ptr_id=weixin_id)
    weixin.delete()
    return _redirect_back(request)

def preview_weixin(request, weixin_id=None):
    weixin = get_object_or_404(Collection, entity_ptr_id=weixin_id)
    return render(request, 'preview_weixin.html', { 'weixin' : weixin })

@login_required
def add_edit_collection(request, collection_id=None):
    _auth_user(request)
    sync_timestamp1 =''
    if collection_id:
        collection = get_object_or_404(Collection, entity_ptr_id=collection_id)
        sync_timestamp1 = collection.sync_timestamp1
    else:
        collection = None

    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES, instance=collection)
        if form.is_valid():
            collection = form.save()
            if request.POST['cover']:
                collection.cover = request.POST['cover'].replace(settings.MEDIA_URL, '', 1)
            else:
                collection.cover = request.POST['cover']
            if sync_timestamp1 != collection.sync_timestamp1:
                if sync_timestamp1 != '':
                    collection.status1 = Entity.STATUS_PENDING
            collection.save()
            return _redirect_back(request)
    else:
        if collection is None:
            form = CollectionForm(instance=collection, initial={'presenter' : request.user.username})
        else:
            form = CollectionForm(instance=collection)

    return render(request, 'add_edit_collection.html', {'form' : form})

@login_required
def delete_collection(request, collection_id=None):
    _auth_user(request)
    collection = get_object_or_404(Collection, entity_ptr_id=collection_id)
    collection.delete()
    return _redirect_back(request)

def preview_collection(request, collection_id=None):
    collection = get_object_or_404(Collection, entity_ptr_id=collection_id)
    return render(request, 'preview_collection.html', { 'collection' : collection })

@login_required
def add_edit_redier(request, redier_id=None):
    _auth_user(request)
    sync_timestamp1 = ''
    if redier_id:
        redier = get_object_or_404(Redier, entity_ptr_id=redier_id)
        sync_timestamp1 = redier.sync_timestamp1
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
            if sync_timestamp1 != redier.sync_timestamp1:
                if sync_timestamp1 != '':
                    redier.status1 = Entity.STATUS_PENDING
            redier.save()
            return _redirect_back(request)

    else:
        if redier is None:
            form = RedierForm(instance=redier, initial={'presenter' : request.user.username})
        else:
            form = RedierForm(instance=redier)
        
    return render(request, "add_edit_redier.html", { "form" : form})

@login_required
def delete_redier(request, redier_id=None):
    _auth_user(request)
    if redier_id:
        redier = get_object_or_404(Redier, entity_ptr_id=redier_id)
        if redier is not None:
            redier.delete()
            return _redirect_back(request)

@login_required
def add_edit_game(request, game_id=None):
    _auth_user(request)
    sync_timestamp1 = ''
    sync_timestamp3 = ''
    if game_id:
        game = get_object_or_404(Game, entity_ptr_id=game_id)
        sync_timestamp1 = game.sync_timestamp1
        sync_timestamp3 = game.sync_timestamp3
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
            if sync_timestamp1 != game.sync_timestamp1:
                if sync_timestamp1 != '':
                    game.status1 = Entity.STATUS_PENDING
            if sync_timestamp3 != game.sync_timestamp3:
                if sync_timestamp3 != '':
                    game.status3 = Entity.STATUS_PENDING
            game.save()
            return _redirect_back(request)

    else:
        if game is None:
            form = GameForm(instance=game, initial={'presenter' : request.user.username})
        else:
            form = GameForm(instance=game)
        
    return render(request, "add_edit_game.html", { "form" : form})

@login_required
def delete_game(request, game_id=None):
    _auth_user(request)
    game = get_object_or_404(Game, entity_ptr_id=game_id)
    game.delete()
    return _redirect_back(request)

def preview_game(request, game_id=None):
    game = get_object_or_404(Game, entity_ptr_id=game_id)
    return render(request, 'preview_game.html', {'game' : game})


@login_required
def add_edit_player(request, player_id=None):
    _auth_user(request)
    sync_timestamp1 =''
    if player_id:
        player = get_object_or_404(Player, entity_ptr_id=player_id)
        sync_timestamp1 = player.sync_timestamp1
    else:
        player = None

    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            player = form.save()
            if request.POST['player_image']:
                player.player_image = request.POST['player_image'].replace(settings.MEDIA_URL, '', 1)
            #            else:
            #                weixin.cover = request.POST['cover']
            if sync_timestamp1 != player.sync_timestamp1:
                if sync_timestamp1 != '':
                    player.status1 = Entity.STATUS_PENDING
            player.save()
            return _redirect_back(request)
    else:
        if player is None:
            form = PlayerForm(instance=player, initial={'presenter' : request.user.username})
        else:
            form = PlayerForm(instance=player)

    return render(request, 'add_edit_player.html', {'form' : form})

@login_required
def delete_player(request, player_id=None):
    _auth_user(request)
    player = get_object_or_404(Player, entity_ptr_id=player_id)
    player.delete()
    return _redirect_back(request)

def preview_player(request, player_id=None):
    player = get_object_or_404(Player, entity_ptr_id=player_id)
    return render(request, 'preview_player.html', { 'player' : player })


@login_required
def add_edit_game_advice(request, game_advice_id=None):
    _auth_user(request)
    sync_timestamp1 =''
    if game_advice_id:
        game_advice = get_object_or_404(GameAdvices, entity_ptr_id=game_advice_id)
        sync_timestamp1 = game_advice.sync_timestamp1
    else:
        game_advice = None

    if request.method == 'POST':
        form = GameAdvicesForm(request.POST, request.FILES, instance=game_advice)
        if form.is_valid():
            game_advice = form.save()
            if request.POST['advice_image']:
                game_advice.advice_image = request.POST['advice_image'].replace(settings.MEDIA_URL, '', 1)
                #            else:
            #                weixin.cover = request.POST['cover']
            if sync_timestamp1 != game_advice.sync_timestamp1:
                if sync_timestamp1 != '':
                    game_advice.status1 = Entity.STATUS_PENDING
            game_advice.save()
            return _redirect_back(request)
    else:
        if game_advice is None:
            form = GameAdvicesForm(instance=game_advice, initial={'presenter' : request.user.username})
        else:
            form = GameAdvicesForm(instance=game_advice)

    return render(request, 'add_edit_game_advices.html', {'form' : form})

@login_required
def delete_game_advice(request, game_advice_id=None):
    _auth_user(request)
    game_advice = get_object_or_404(GameAdvices, entity_ptr_id=game_advice_id)
    game_advice.delete()
    return _redirect_back(request)

def preview_game_advice(request, game_advice_id=None):
    game_advice = get_object_or_404(GameAdvices, entity_ptr_id=game_advice_id)
    return render(request, 'preview_game_advices.html', { 'gameadvice' : game_advice })

@login_required
def add_edit_puzzle(request, puzzle_id=None):
    _auth_user(request)
    sync_timestamp1 =''
    if puzzle_id:
        puzzle = get_object_or_404(Puzzle, entity_ptr_id=puzzle_id)
        sync_timestamp1 = puzzle.sync_timestamp1
    else:
        puzzle = None

    if request.method == 'POST':
        form = PuzzleForm(request.POST, request.FILES, instance=puzzle)
        if form.is_valid():
            puzzle = form.save()
            if request.POST['picture1']:
                puzzle.picture1 = request.POST['picture1'].replace(settings.MEDIA_URL, '', 1)
            else:
                puzzle.picture1 = request.POST['picture1']
            if request.POST['picture2']:
                puzzle.picture2 = request.POST['picture2'].replace(settings.MEDIA_URL, '', 1)
            if request.POST['picture3']:
                puzzle.picture3 = request.POST['picture3'].replace(settings.MEDIA_URL, '', 1)
            if request.POST['picture4']:
                puzzle.picture4 = request.POST['picture4'].replace(settings.MEDIA_URL, '', 1)
            if sync_timestamp1 != puzzle.sync_timestamp1:
                if sync_timestamp1 != '':
                    puzzle.status1 = Entity.STATUS_PENDING
            puzzle.save()
            return _redirect_back(request)
    else:
        if puzzle is None:
            form = PuzzleForm(instance=puzzle, initial={'presenter' : request.user.username})
        else:
            form = PuzzleForm(instance=puzzle)

    return render(request, 'add_edit_puzzle.html', {'form' : form})

@login_required
def delete_puzzle(request, puzzle_id=None):
    _auth_user(request)
    puzzle = get_object_or_404(Puzzle, entity_ptr_id=puzzle_id)
    puzzle.delete()
    return _redirect_back(request)
