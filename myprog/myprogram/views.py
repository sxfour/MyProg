from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from myprogram.models import Program, Category, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
        ]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
        Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


# http request
def index(request):
    posts = Program.published.all()

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'program/index.html', context=data)


def about(request):
    return render(request, 'program/about.html', {'title': 'О Сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Program, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1.
    }

    return render(request, 'program/post.html', data)

def addpage(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Войти')


def show_categories(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Program.published.filter(cat_id=category.pk)

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'program/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center" style="color:rgb(169,169,169)"> '
                                '— Ну вот, я так и думал.'
                                ' С этой стороны ничуть не лучше...</h1>')


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Program.Status.PUBLISHED)

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'program/index.html', context=data)
