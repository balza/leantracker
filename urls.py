from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib import admin
from projects.views import ProjectViewSet

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login', name="home"),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^timesheet/', include('timesheet.urls', namespace='timesheet', app_name='timesheet')),
    url(r'^holidaysplanner/', include('holidaysplanner.urls', namespace='holidaysplanner', app_name='holidaysplanner')),
    url(r'^projects/', include('projects.urls', namespace='projects', app_name='projects')),
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
