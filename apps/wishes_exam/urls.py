from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$',views.logout),
    url(r'^process$', views.add),
    url(r'^wishes$',views.wishes),
    url(r'^wishes/new$',views.new),
    url(r'^wishes/new/add$',views.create),
    url(r'^wishes/edit/(?P<wish_id>\d+)$',views.edit),
    url(r'^wishes/update/(?P<wish_id>\d+)$',views.update),
    url(r'^wishes/remove/(?P<wish_id>\d+)$',views.delete),
    url(r'^wishes/grant/(?P<wish_id>\d+)$',views.grant),
    url(r'^wishes/stats$',views.stats),
    url(r'^like/(?P<wish_id>\d+)/(?P<user_id>\d+)$', views.like)
]