from django.conf.urls import patterns, include, url
from create_account.views import user

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_ride/', 'create_account.views.ride'),
    url(r'^profile/', 'create_account.views.profile')
)
