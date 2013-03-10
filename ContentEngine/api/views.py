# -*- coding: utf-8 -*-
import sys
import os

from django.template import loader,Context
from django.http import HttpResponse
from api.models import HotGamesView, HotGamesRedierView
from sina.sinaAuth import SinaAuth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login
from django.shortcuts import render
from api.tables import HotGamesTable,GameRediersTable

import django_tables2 as tables
from django_tables2 import RequestConfig

def HotGamesViewFunc(request):
    hotgames = HotGamesTable(HotGamesView.objects.all(),prefix="hg-")
    hotgames.paginate(page=request.GET.get("hg-page",1), per_page=10)
    hotgames.data.verbose_name = u"精品游戏推荐"

    gamerediers = GameRediersTable(HotGamesRedierView.objects.all(),prefix="gr-")
    gamerediers.paginate(page=request.GET.get("gr-page",1), per_page=10)
    gamerediers.data.verbose_name = u"小兵变大咖"

    return render(request, "index.html", {"hotgames": hotgames, "gamerediers":gamerediers})

def Auth(request):
    auth = SinaAuth()
    return HttpResponseRedirect(auth.getAuthorizeUrl())

def Sinalogin(request):
    code = request.GET.get('code')
    print code
    auth = SinaAuth()
    print auth.getToken(code)
    if auth is None:
        return HttpResponseRedirect("www.bestgames7.com")
    else:
#        user.backend='django.contrib.auth.backends.ModelBackend'
#        login(request, user)
        username = 'admin'
        password = 'admin'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print 'login success'
                return HttpResponseRedirect("http://127.0.0.1/hotgames")


@staff_member_required
def report(request):
    return render_to_response(
        "admin/hotgamesadmin.html",
        {'book_list' : HotGamesView.objects.all()},
        RequestContext(request, {}),
    )

