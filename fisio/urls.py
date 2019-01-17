"""fisio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # new
from django.conf.urls import url # new
from django.views.generic.base import TemplateView # new
from boards import views
from django.contrib.auth import views as auth_views

from akun import views as akun_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # new
    path('accounts/', include('accounts.urls')), # new
    path('home/', TemplateView.as_view(template_name='home.html'), name='homese'), # new

    url(r'^$', views.homes, name='home'),
    url(r'^board/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^board/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    url(r'^signup/$', akun_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='loginAkun.html'), name='login'),

] 