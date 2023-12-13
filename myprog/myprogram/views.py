from django.http import HttpResponse
from django.shortcuts import render


# http request
def index(request):
    return HttpResponse('Страница myprogram')

def categories(request):
    return HttpResponse('<h1>Статьи по категориям</h1>')