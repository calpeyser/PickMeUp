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
	url(r'^confirm/', 'create_account.views.confirm'),
	url(r'^add_me/', 'create_account.views.add_passenger'),
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
    url(r'^about/', 'create_account.views.about'),
    url(r'^choose_passenger/', 'create_account.views.choose_passenger'),
    url(r'^boot_passenger/', 'create_account.views.boot_passenger'),
    url(r'^leave_ride/', 'create_account.views.leave_ride'),
    url(r'^logout/', 'create_account.views.logout'),
    url(r'^new_user/', 'create_account.views.new_user'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
