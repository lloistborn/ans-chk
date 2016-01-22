from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login_view, name='login_view'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),

	url(r'^memulai/$', views.memulai, name='memulai'),
	# url(r'^tampil_hasil/$', views.tampil_hasil, name='tampil_hasil'),	
]