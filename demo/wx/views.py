from django.shortcuts import render
from django.http.response import HttpResponse

from wechat_django.models import Wechat

wechat = Wechat.objects.first()


def wechat(request, *args, **kwargs):
    print(dir(request))
    print(args, kwargs)
    print(dir(request.GET))
    print(request.GET.items())
    print(request.GET.keys())
    print(wechat)
    return HttpResponse("ok")
