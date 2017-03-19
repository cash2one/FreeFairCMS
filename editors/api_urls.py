from django.conf.urls import url

from . import api_views as views


urlpatterns = [
    url(r'^admin/all/$', views.AllEditorsView.as_view()),
    url(r'^admin/new/$', views.AllEditorsView.as_view()),
    url(r'^admin/roles/$', views.AllRolesView.as_view()),
    url(r'^admin/(?P<pk>\d+)/$', views.SingleEditorView.as_view()),
]
