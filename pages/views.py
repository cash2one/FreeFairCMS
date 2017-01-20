from django.views.generic import DetailView

from .models.pages import Page
from .forms import NewPageForm


class SinglePageView(DetailView):
    context_object_name = 'page'
    template_name = 'pages/page.html'
    queryset = Page.objects.prefetch_related('blocks')
    slug_url_kwarg = 'url'
    slug_field = 'url'


class IndexView(SinglePageView):
    def get_object(self):
        queryset = self.get_queryset()

        obj = queryset.filter(url="index").get()

        return obj
