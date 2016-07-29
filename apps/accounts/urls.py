from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^home/$', views.home, name='home'),
	url(r'^logout/$', views.logout, name="logout"),
	url(r'^user/(?P<user_id>[^/]+)(?:/)*$', views.user, name="user"),
	url(r'^addfriend/(?P<user_id>[^/]+)(?:/)*$', views.addfriend, name="addfriend"),
	url(r'^deletefriend/(?P<user_id>[^/]+)(?:/)*$', views.deletefriend, name="deletefriend"),
]