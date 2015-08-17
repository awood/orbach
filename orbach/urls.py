from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('orbach.core.urls', namespace='rest_framework')),
    url(r'^gallery/', include('orbach.gallery.urls', namespace='gallery')),
]
