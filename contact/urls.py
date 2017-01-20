from django.conf.urls import url

from .views import ContactFormView

urlpatterns = [
    url(r'^send/$', ContactFormView.as_view()) 
]
