# Create your views here.
# -*- coding: utf-8 -*-
import sys
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
import json
import time
import socket
import random

def getPic(request):
    root_path = os.path.dirname(os.path.dirname(os.path.normpath(__file__))) + '/scrapy_itunes/auto_get_pic'
    download_url = request.GET.get('download_url')
    response_data = {}
    if download_url:
      curtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randint(1, 1000))

      print curtime
      command = 'cd ' + root_path +  '&&scrapy crawl parse_ituns -a  url="' + download_url + '" -a pic_prefix=' + curtime
      print command
      os.system(command)

      server_url =  "http://" + "cow.bestgames7.com" + "/pic/"


      response_data['icon'] = server_url + 'icon' + curtime + ".jpg"
      response_data['desc1'] = server_url + 'desc1' + curtime + ".jpg"
      response_data['desc2'] = server_url + 'desc2' + curtime + ".jpg"
      response_data['desc3'] = server_url + 'desc3' + curtime + ".jpg"
      response_data['desc4'] = server_url + 'desc4' + curtime + ".jpg"

      #return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    return render(request, "get_pic/get_pic.html", response_data)

def previewImage(request,filename):
    if filename:
        image_data = open(os.getcwd() + '/scrapy_itunes/auto_get_pic/games/' + filename, "rb").read()
        return HttpResponse(image_data, mimetype="image/png")



