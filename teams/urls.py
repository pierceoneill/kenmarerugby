from django.conf.urls import url
from .views import teams

urlpatterns = [
    url(r'^$', teams, name='teams')
]