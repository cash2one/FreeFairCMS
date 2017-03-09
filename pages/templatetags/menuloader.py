from django import template

from ..models.pages import Page, StatePage


register = template.Library()

def menu(active):
    pages = Page.objects.filter(pagetype="Regular", published=True).exclude(url='index').values('url', 'title')
    states = StatePage.objects.filter(published=True)

    return {
        'active': active,
        'pages': pages,
        'states': states
    }

register.inclusion_tag('pages/menu.html')(menu)
