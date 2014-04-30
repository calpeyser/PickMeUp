from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import CASClient
import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

from create_account.views import User


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
    url(r'^write_message_ride/', 'create_account.views.write_message_ride'),    
    url(r'^write_message_conversation/', 'create_account.views.write_message_conversation'),    
    url(r'^write_message_target/', 'create_account.views.write_message_target'),    
	url(r'^delete_message/', 'create_account.views.delete_message'),
    url(r'^sent', 'create_account.views.sent'),
    url(r'^profile/', 'create_account.views.profile'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^driver_future/', 'create_account.views.driver_future'),
    url(r'^driver_past/', 'create_account.views.driver_past'),
    url(r'^passenger_future/', 'create_account.views.passenger_future'),
    url(r'^passenger_past/', 'create_account.views.passenger_past'),
    url(r'^cancel_ride/', 'create_account.views.cancel_ride'),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
