from django.conf.urls import *
from projects.views import ProjectViewSet
from rest_framework import routers


# Important: authentication, as often in django, It's a little bit alien for a java programmer,
# seems .html pages mix responsabilities with url.py
#   ref https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                      )

