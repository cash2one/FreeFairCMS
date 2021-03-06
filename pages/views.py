from django.views.generic import DetailView
from bakery.views import BuildableDetailView

from .models.pages import Page, StatePage
from .forms import NewPageForm


class SinglePageView(BuildableDetailView):
    context_object_name = 'page'
    template_name = 'pages/page.html'
    queryset = Page.objects.prefetch_related('blocks').filter(pagetype="Regular", published=True)
    slug_url_kwarg = 'url'
    slug_field = 'url'


class IndexView(SinglePageView):
    def get_url(self, obj):
        return '/'

    def get_object(self):
        queryset = self.get_queryset()

        obj = queryset.filter(url="index").get()

        return obj


class StatePageView(SinglePageView):
    template_name = 'pages/state_page.html'
    queryset = StatePage.objects.prefetch_related('blocks').filter(published=True)
    slug_url_kwarg = 'state'
    slug_field = 'state'
