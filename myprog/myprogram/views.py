from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse

menu = [
    {'title': 'Site', 'url_name': 'about'},
    {'title': 'Create post', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
        ]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


# http request
def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'program/index.html', context=data)


def about(request):
    return render(request, 'program/about.html', {'title': 'О Сайте'})


def show_post(request, post_id):
    return HttpResponse(f'id = {post_id}')


def addpage(request):
    return HttpResponse('Create blog')


def contact(request):
    return HttpResponse('Contact us')


def login(request):
    return HttpResponse('Login')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center" style="color:rgb(169,169,169)"> '
                                '— Ну вот, я так и думал.'
                                ' С этой стороны ничуть не лучше...</h1>')
