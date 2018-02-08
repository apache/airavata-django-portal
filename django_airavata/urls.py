"""django_airavata_gateway URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include('django_airavata.apps.admin.urls')),
    url(r'^auth/', include('django_airavata.apps.auth.urls')),
    url(r'^workspace/', include('django_airavata.apps.workspace.urls')),
    url(r'^api/', include('django_airavata.apps.api.urls')),
    url(r'^groups/', include('django_airavata.apps.groups.urls')),
    url(r'^resourceallocation/', include('django_airavata.apps.resourceallocation.urls')),
    url(r'^$', views.home, name='home')
]
