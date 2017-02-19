from django.conf.urls import url

from . import api_views as views

urlpatterns = [
    url(r'^admin/all/$', views.AllRegularPagesView.as_view()),
    url(r'^admin/new/$', views.AllRegularPagesView.as_view()),
    url(r'^admin/(?P<pk>\d+)/$', views.SinglePageView.as_view()),
    url(r'^admin/bulk/$', views.BulkPageUpdateView.as_view()),
    url(r'^admin/blocks/types/$', views.BlockTypeView.as_view()),
    url(r'^admin/blocks/new/$', views.NewBlockView.as_view()),
    url(r'^admin/blocks/(?P<pk>\d+)/$', views.BlockDeleteView.as_view()),
    url(r'^admin/blocks/accordions/new/$', views.NewAccordionView.as_view()),
    url(r'^admin/blocks/accordions/(?P<pk>\d+)/$', views.DeleteAccordionView.as_view()),
    url(r'^admin/blocks/info/category/new/$', views.NewInfoCategoryView.as_view()),
    url(r'^admin/blocks/info/category/(?P<pk>\d+)/$', views.DeleteInfoCategoryView.as_view()),
    url(r'^admin/blocks/info/content/new/$', views.NewInfoContentView.as_view()),
    url(r'^admin/blocks/info/content/(?P<pk>\d+)/$', views.DeleteInfoContentView.as_view()),
    url(r'^admin/publish/$', views.PublishView.as_view()),
]
