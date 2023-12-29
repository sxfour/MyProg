from django import template
import myprogram.views as views
from myprogram.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('program/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('program/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}
