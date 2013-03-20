# Create your views here.
from django.http import HttpResponse
import hashlib

def index(request):
    if request.method == 'GET':
        if 'signature' not in request.GET or 'timestamp' not in request.GET or 'nonce' not in request.GET or 'echostr' not in request.GET:
            return HttpResponse('bad request %s' % str(request.GET))
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        infos = [signature, timestamp, nonce]
        infos.sort()
        m = hashlib.sha1()
        m.update(''.join(infos))
        caledSig = m.hexdigest()

        return HttpResponse(echostr)
