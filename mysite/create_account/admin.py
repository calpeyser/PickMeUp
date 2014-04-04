from django.contrib import admin
from create_account.models import User
from create_account.models import Ride
from create_account.models import Location

admin.site.register(User);
admin.site.register(Ride);
admin.site.register(Location);
