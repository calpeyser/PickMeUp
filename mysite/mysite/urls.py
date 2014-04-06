from django.conf.urls import patterns, include, url
from create_account.views import user
import CASClient

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_account/', 'create_account.views.user'),
    url(r'^home/', 'create_account.views.home')
    url(r'^$', 'create_account.views.authenticate')
)
