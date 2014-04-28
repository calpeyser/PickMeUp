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
    url(r'^home/', 'create_account.views.home'),
    url(r'^$', 'create_account.views.authenticate'),
	url(r'^create_ride/', 'create_account.views.ride'),
	url(r'^find_ride/', 'create_account.views.show_rides'),
	url(r'^inbox/', 'create_account.views.inbox'),
	url(r'^write_message/', 'create_account.views.write_message'),
	url(r'^delete_message/', 'create_account.views.delete_message'),
    url(r'^sent/', 'create_account.views.sent')
)
