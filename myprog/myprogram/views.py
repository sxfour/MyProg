from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from myprogram.forms import AddPostForm, UploadFileForm
from myprogram.models import Program, Category, TagPost, UploadFiles

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


# http request
# def index(request):
#     posts = Program.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'program/index.html', context=data)


class ProgramHome(ListView):
    # model = Program
    template_name = 'program/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Program.published.all().select_related('cat')

    # template_name = 'program/index.html'
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts': Program.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Program.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #
    #     return context


# def handle_upload_file(f):
#     with open(f'uploads/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'program/about.html',
                  {'title': 'О Сайте', 'menu': menu, 'form': form})


# def show_post(request, post_slug):
#     post = get_object_or_404(Program, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'program/post.html', data)


class ShowPost(DetailView):
    # model = Program
    template_name = 'program/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Program.published, slug=self.kwargs[self.slug_url_kwarg])

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Program.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except Exception as ex:
#             #     form.add_error(None, f'Error: {ex}')
#
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form,
#     }
#     return render(request, 'program/addpage.html', data)


class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'program/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form,
#         }
#         return render(request, 'program/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form,
#         }
#         return render(request, 'program/addpage.html', data)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Войти')


def show_categories(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Program.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'program/index.html', context=data)


class ProgramCategory(ListView):
    template_name = 'program/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Program.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk

        return context


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center" style="color:rgb(169,169,169)"> '
                                '— Ну вот, я так и думал.'
                                ' С этой стороны ничуть не лучше...</h1>')


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Program.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'program/index.html', context=data)

class TagPostList(ListView):
    template_name = 'program/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None

        return context

    def get_queryset(self):
        return Program.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
