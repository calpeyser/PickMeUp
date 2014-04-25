from django.contrib import admin
from create_account.models import User, Ride, Location, Message, Conversation

admin.site.register(User);
admin.site.register(Ride);
admin.site.register(Location);
admin.site.register(Message);
admin.site.register(Conversation);