"""kenmarerugby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from home.views import index
from .settings import MEDIA_ROOT
from django.contrib.auth import views
from accounts import urls as urls_accounts
from accounts import url_reset
from blog import urls as urls_blog
from teams import urls as urls_teams
from contact import urls as urls_contact
from about import urls as urls_about
from django.contrib.auth import views
from django.views import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(urls_accounts)),
    url(r'^$', index, name='index'),
    url(r'^blog/', include(urls_blog)),
    url(r'^teams/', include(urls_teams)),
    url(r'^contact/', include(urls_contact)),
    url(r'^about/', include(urls_about)),
    url(r'^media/(?P<path>.*)$', static.serve,{'document_root': MEDIA_ROOT}),
     url(r'^password-reset/', include(url_reset))
]
