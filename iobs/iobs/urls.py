"""iobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from stops import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.start_view, name='home'),
    url(r'^leave$', views.leave, name='home'),
    url(r'^activate$', views.activate_view, name='home'),
    url(r'^sensor$', views.sensor_test, name='home'),
    url(r'^games/(?P<game_id>\d+)/poll$', views.game_poll, name='home'),
    url(r'^games/(?P<game_id>\d+)/edge$', views.game_edge, name='home'),
    url(r'^games/(?P<game_id>\d+)/cell$', views.game_cell, name='home'),
    url(r'^games/(?P<game_id>\d+)/endturn$', views.end_turn, name='home'),
]
