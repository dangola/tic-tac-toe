from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^play$', views.play, name='play'),
    url(r'^adduser$', views.adduser, name='adduser'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^verify$', views.verify_user, name='verify'),
    url(r'^listgames$', views.listgames, name='listgames'),
    url(r'^getgame$', views.getgame, name='getgame'),
    url(r'^getscore$', views.getscore, name='getscore'),

]
