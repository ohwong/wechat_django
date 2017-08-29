
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wechatpy.parser import parse_message
from wechat_django.models import Wechat
from xmltodict import expat

try:
    wechat = Wechat.objects.first()
except Exception:
    pass


@csrf_exempt
def wx(request, callback=None, *args, **kwargs):
    if request.method == 'GET':
        nonce = request.GET.get("nonce")
        echostr = request.GET.get("echostr")
        timestamp = request.GET.get("timestamp")
        signature = request.GET.get("signature")
        wechat.check_signature(signature, timestamp, nonce)
        if callback:
            return HttpResponse(echostr)
    elif request.method == 'POST':
        try:
            message = parse_message(request.body)
            if callback:
                callback(message)
        except expat.ExpatError:
            pass
    return HttpResponse("")


@wechat.oauth.oauth_required
def hello(request):
    return HttpResponse("HELLO WORLD")

