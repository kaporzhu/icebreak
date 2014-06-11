from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^buildings/', include('buildings.urls', 'buildings', 'buildings')),
    url(r'^shops/', include('shops.urls', 'shops', 'shops')),

    url(r'^admin/', include(admin.site.urls)),
)
