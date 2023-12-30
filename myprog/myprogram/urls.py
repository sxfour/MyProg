from django.urls import path, register_converter
from myprogram import views, converters

register_converter(converters.FourDigitYearConverter,'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>', views.show_categories, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]