from django.forms import ModelForm
from django import forms
from create_account.models import User, Ride, Location, Home, Message, Conversation


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

#Form class for the home page
class HomeForm(ModelForm):

	class Meta:
		model = Home

class MessageForm(forms.Form):
	recipient = forms.CharField();
	title = forms.CharField();
	message = forms.CharField();
