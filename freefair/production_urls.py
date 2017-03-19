from django.conf.urls import include, url
from django.contrib import admin

from editors.api_views import EditorLoginView

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^rest-auth/editor-login/', EditorLoginView.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api/pages/', include('pages.api_urls')),
    url(r'^api/editors/', include('editors.api_urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^', include('pages.urls', namespace="pages")),
    url(r'^', include('django.contrib.auth.urls')),
]
