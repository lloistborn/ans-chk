from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login_view, name='login_view'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),

	url(r'^memulai/$', views.memulai, name='memulai'),
	url(r'^get_skor/$', views.get_skor, name='get_skor'),	
]