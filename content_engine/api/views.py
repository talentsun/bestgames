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

from api.models import Game, Redier, Collection, Problem
from api.tables import GameTable, RedierTable, CollectionTable, ProblemTable
from api.forms import GameForm, RedierForm, CollectionForm, ProblemForm

import django_tables2 as tables

def index(request):
    games = GameTable(Game.objects.all(),prefix="hg-")
    games.paginate(page=request.GET.get("hg-page",1), per_page=10)
    games.data.verbose_name = u"精品游戏推荐"

    rediers = RedierTable(Redier.objects.all(),prefix="gr-")
    rediers.paginate(page=request.GET.get("gr-page",1), per_page=10)
    rediers.data.verbose_name = u"小兵变大咖"

    collections = CollectionTable(Collection.objects.all(),prefix="co-")
    collections.paginate(page=request.GET.get("co-page",1), per_page=10)
    collections.data.verbose_name = u"游戏合集"

    problems = ProblemTable(Problem.objects.all(),prefix="pb-")
    problems.paginate(page=request.GET.get("pb-page",1), per_page=10)
    problems.data.verbose_name = u"宅，必有一技"

    return render(request, "index.html", {"games": games, "rediers":rediers, 'collections':collections, 'problems':problems})

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def add_edit_problem(request, problem_id=None):
    if problem_id:
        problem = get_object_or_404(Problem, entity_ptr_id=problem_id)
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
            problem.save()
            return redirect('/')
    else:
        if problem is None:
            form = ProblemForm(instance=problem, initial={'presenter' : request.user.username})
        else:
            form = ProblemForm(instance=problem)

    return render(request, 'add_edit_problem.html', {'form' : form, 'tags' : Tag.objects.all()})

@login_required
def delete_problem(request, problem_id=None):
    if problem_id:
        problem = get_object_or_404(Problem, entity_ptr_id=problem_id)
        if problem is not None:
            problem.delete()
            return redirect('/')

@login_required
def add_edit_collection(request, collection_id=None):
    if collection_id:
        collection = get_object_or_404(Collection, entity_ptr_id=collection_id)
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
            collection.save()
            return redirect('/')
    else:
        if collection is None:
            form = CollectionForm(instance=collection, initial={'presenter' : request.user.username})
        else:
            form = CollectionForm(instance=collection)

    return render(request, 'add_edit_collection.html', {'form' : form, 'tags' : Tag.objects.all()})

@login_required
def delete_collection(request, collection_id=None):
    if collection_id:
        collection = get_object_or_404(Collection, entity_ptr_id=collection_id)
        if collection is not None:
            collection.delete()
            return redirect('/')

@login_required
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

@login_required
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

