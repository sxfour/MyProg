from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse


# http request
def index(request):
    return render(request, 'program/index.html')


def about(request):
    return render(request, 'program/about.html')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)

    return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('sport',))
        return redirect(uri)

    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center" style="color:rgb(169,169,169)"> '
                                '— Ну вот, я так и думал.'
                                ' С этой стороны ничуть не лучше...</h1>')
