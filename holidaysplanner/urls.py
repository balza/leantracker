from django.conf.urls import *
from holidaysplanner.views import load


# Important: authentication, as often in django, It's a little bit alien for a java programmer,
# seems .html pages mix responsabilities with url.py
#   ref https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views


urlpatterns = patterns('',
                       url(r'^$', load, name="load"),
)

