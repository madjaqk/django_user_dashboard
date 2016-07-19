from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^$', views.login_page, name="login_page"),
	url(r'^login$', views.login, name="login"),
	url(r'^register$', views.register, name="register"),
	url(r'^log_off$', views.log_off, name="log_off"),
	url(r'^dashboard$', views.dashboard, name="dashboard"),
	url(r'^show/(?P<id>\d+)', views.show, name="show"),
	url(r'^edit/(?P<id>\d+)', views.edit, name="edit"),
	url(r'^update/(?P<id>\d+)', views.update, name="update"),
]