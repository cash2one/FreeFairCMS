from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^state/(?P<state>[\w]+)/$', views.StatePageView.as_view(), name="state-page"),
    url(r'^(?P<url>[\w-]+)/$', views.SinglePageView.as_view(), name="single-page"),
]
