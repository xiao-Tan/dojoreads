from django.conf.urls import url
from . import views   

urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.book_home),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.add_book),
    url(r'^new_book$', views.new_book),
    url(r'^books/(?P<num>\d+)$', views.one_book),
    url(r'^delete_review/(?P<num>\d+)$', views.delete_review),
    url(r'^add_review/(?P<num>\d+)$', views.add_review),
    url(r'^users/(?P<num>\d+)$', views.user_page),
]