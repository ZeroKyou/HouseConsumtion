from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/success/$', views.login_successful, name='login_successful'),
    url(r'^accounts/logout/success/$', views.logout_successful, name='logout_successful'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^meter/electricity/(?P<time_period>\w+)/$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/(?P<time_period>\w+)/values/$', views.electricity_values, name='electricity_values'),
    url(r'^meter/meter/reading/$', views.add_meter_reading, name='add_meter_reading'),
    url(r'^meter/water/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>\w+)/$', views.water_meter, name='water_meter'),
]
