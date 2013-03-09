# -*- coding: utf-8 -*-
import sys
import os

from django.template import loader,Context
from django.http import HttpResponse
from api.models import HotGamesView
from sina.sinaAuth import SinaAuth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse

def HotGamesViewFunc(request):
    hotgames = HotGamesView.objects.all()
    t = loader.get_template("index.html")
    c = Context({'hotgames':hotgames})
    return HttpResponse(t.render(c))

def Auth(request):
    auth = SinaAuth()
    return HttpResponseRedirect(auth.getAuthorizeUrl())

def login(request):
    code = request.GET.get('code')
    print code
    auth = SinaAuth()
    print auth.getToken(code)
    if auth is None:
        return HttpResponseRedirect("www.bestgames7.com")
    else:
        return HttpResponseRedirect(reverse("home"))




@staff_member_required
def report(request):
    return render_to_response(
        "admin/hotgamesadmin.html",
        {'book_list' : HotGamesView.objects.all()},
        RequestContext(request, {}),
    )

