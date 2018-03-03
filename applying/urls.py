from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from applying import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^apply/(?P<username>[\w\-]+)/$', views.apply, name='apply'),
    url(r'^result_general/', views.result_general_admin, name='result_general'),
    url(r'^result_econ/', views.result_econ_admin, name='result_econ'),
    url(r'^result2/', views.result_by_ministry, name='result2'),
    url(r'^result3_general/', views.simulate_overall_general_admin, name='result3_general'),
    url(r'^result3_econ/', views.simulate_overall_econ_admin, name='result3_econ'),
]
