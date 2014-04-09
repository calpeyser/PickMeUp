from django.forms import ModelForm
from django import forms
from create_account.models import User
from create_account.models import Ride
from create_account.models import Location

# Create the form class for users
class UserForm(ModelForm):
	class Meta:
		model = User

# Create the form class for rides
class RideForm(ModelForm):
	class Meta:
		model = Ride;
		fields = ['max_seats', 'start_date', 'start_time'];

# Create the form class for rides
class RideForm2(forms.Form):

	#--------PLACEHOLDER LOCATIONS!!!!---------#
	location1 = Location.objects.all()[0];
	location2 = Location.objects.all()[1];
	#------------------------------------------#
	max_seats = forms.CharField(max_length = 100);
	start_date = forms.CharField(max_length = 100);
	end_date = forms.CharField(max_length = 100);
	start = location1;
	end = location2;


