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
	start = forms.CharField(widget = forms.HiddenInput())
	end = forms.CharField(widget = forms.HiddenInput())
	startname = forms.CharField(widget = forms.HiddenInput())
	endname = forms.CharField(widget = forms.HiddenInput())

	class Meta:
		model = Home

class MessageForm(forms.Form):
	recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all());
	title = forms.CharField();
	message = forms.CharField();
