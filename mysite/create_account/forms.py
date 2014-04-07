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

class RideForm(forms.Form):
	max_seats = forms.IntegerField();
	open_seats = forms.IntegerField();
	start_date = forms.DateField();
	start_time = forms.TimeField();
	payment = forms.IntegerField();


"""class RideForm2(ModelForm):
	class Meta:
		model = Ride;
		fields = ['max_seats', 'start_date', 'start_time'];"""




