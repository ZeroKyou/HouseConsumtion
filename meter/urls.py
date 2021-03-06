from django.conf.urls import url
from meter import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/success/$', views.login_successful, name='login_successful'),
    url(r'^accounts/logout/success/$', views.logout_successful, name='logout_successful'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/settings/$', views.settings, name='settings'),
    url(r'^meter/electricity/(?P<time_period>)$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/(?P<time_period>year)/$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/(?P<time_period>month)/$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/(?P<time_period>recent)/$', views.electricity_meter, name='electricity_meter'),
    url(r'^meter/electricity/(?P<time_period>year)/values/$', views.electricity_values, name='electricity_values'),
    url(r'^meter/electricity/(?P<time_period>month)/values/$', views.electricity_values, name='electricity_values'),
    url(r'^meter/electricity/(?P<time_period>recent)/values/$', views.electricity_values, name='electricity_values'),
    url(r'^meter/reading/$', views.add_meter_reading, name='add_meter_reading'),
    url(r'^meter/water/(?P<time_period>)$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>year)/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>month)/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>recent)/$', views.water_meter, name='water_meter'),
    url(r'^meter/water/(?P<time_period>year)/values/$', views.water_values, name='water_values'),
    url(r'^meter/water/(?P<time_period>month)/values/$', views.water_values, name='water_values'),
    url(r'^meter/water/(?P<time_period>recent)/values/$', views.water_values, name='water_values'),
]
