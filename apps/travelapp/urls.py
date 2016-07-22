from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name="travel_start"),
	url(r'^register$', views.register, name="travel_register"),
	url(r'^login$', views.login, name="travel_login"),
	url(r'^logout$', views.logout, name="travel_logout"),
	url(r'^travels$', views.home, name="travel_home"),
	url(r'^travels/add$', views.add, name="travel_add"),
	url(r'^travels/create$', views.create, name="travel_create"),
	url(r'^travels/join/(?P<id>\d+)$', views.update, name="travel_update"),
	url(r'^travels/show/(?P<id>\d+)$', views.show, name="travel_show"),
]