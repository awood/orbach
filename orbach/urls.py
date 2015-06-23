from django.conf.urls import include, url
from django.contrib import admin

from orbach.gallery.views import gallery, text_file

urlpatterns = [
    url(r'^$', gallery, name="gallery"),
    url(r'^(?P<filename>(robots.txt))$', text_file, name='text_file'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('orbach.core.urls', namespace='rest_framework')),
]
