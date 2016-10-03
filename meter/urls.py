from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/success/$', views.login_successful, name='login_successful'),
    url(r'^accounts/logout/success/$', views.logout_successful, name='logout_successful'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^meter/electricity/(?P<time_period>\w+)/$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/reading/$', views.add_electricity_reading, name='add_electricity_reading'),
    url(r'^meter/water/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>\w+)/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/reading/$', views.add_water_reading, name='add_water_reading'),
    url(r'^meter/total/(?P<time_period>\w+)/$', views.total_consumption, name='total_consumption'),
]
