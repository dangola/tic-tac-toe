from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_name, name='index'),
    url(r'^play$', views.get_move),
]
