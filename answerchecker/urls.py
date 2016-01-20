from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login_view, name='login_view'),
	url(r'^login/$', views.login, name='login'),
	url(r'^mulai/$', views.mulai, name='mulai'),	
]