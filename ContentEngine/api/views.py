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
from django.shortcuts import render

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
        return HttpResponseRedirect("www.bestgames7.com")
    else:
        username = 'admin'
        password = 'admin'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print 'login success'
                return HttpResponseRedirect("http://127.0.0.1/hotgames")

def add_rediers(request):
    form = RedierForm()
    return render(request, "add_rediers.html", { "form": form })

def add_games(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        print 'save'
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/completed')

    else:
        form = GameForm()
    return render(request, "add_hotgames.html", { "form" : form })

def completed(request):
    return render(request, "completed.html")

