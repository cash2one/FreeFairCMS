from django import template

from ..models.pages import Page


register = template.Library()

def menu(active):
    pages = Page.objects.filter(pagetype="Regular", published=True).exclude(url='index').values('url', 'title')

    return {
        'active': active,
        'pages': pages,
    }

register.inclusion_tag('pages/menu.html')(menu)
