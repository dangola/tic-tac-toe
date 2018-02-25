from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^play$', views.play, name='play'),
    url(r'^adduser$', views.adduser, name='adduser'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^verify$', views.verify, name='verify')
]
