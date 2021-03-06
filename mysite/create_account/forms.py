from django.forms import ModelForm, ValidationError
from django import forms
from django.core import urlresolvers
from django.db import models
from create_account.models import User, Ride, Location, Home, Message, Conversation
import autocomplete_light

autocomplete_light.autodiscover()

MAX_MAX_SEATS = 10000

#------------------------------------------------------------------------------------------------------
# PUT CUSTOM FORM ELEMENTS HERE

# This is a modelform which will allow comma seperated values.  It's taken from StackOverflow:
# http://stackoverflow.com/questions/5608576/django-enter-a-list-of-values-form-error-when-rendering-a-manytomanyfield-as-a
class ModelCommaSeparatedChoiceField(forms.ModelMultipleChoiceField):
    widget = forms.Textarea
    def clean(self, value):
        if value is not None:
            value = [item.strip() for item in value.split(",")] # remove padding
        return super(ModelCommaSeparatedChoiceField, self).clean(value)

#------------------------------------------------------------------------------------------------------


# Create the form class for users
class UserForm(forms.Form):
    first_name = forms.CharField(label="First name");
    last_name = forms.CharField(label="Last name");
    phone_number = forms.CharField(label="Phone number");


# Create the form class for rides

class RideForm(forms.Form):
	max_seats = forms.IntegerField(label="How many seats are in your car?                ");
	open_seats = forms.IntegerField(label="How many of those seats are available?         ");
	start_date = forms.DateField(label="On what date are you leaving? (mm/dd/yyyy)     ");
	start_time = forms.TimeField(label="What time are you leaving? (HH:MM 24-Hour Format)     ");
	payment = forms.CharField(label="How would you like to be reimbursed, per passenger?");

        def clean(self):
            cleaned_data = super(RideForm, self).clean()
            errors = []
            
            if cleaned_data['max_seats'] < 0:
                errors.append(ValidationError('Please enter a valid number for Maximum Seats'))
            if cleaned_data['max_seats'] > MAX_MAX_SEATS:
                errors.append(ValidationError('Is your car really that big?'))
            if cleaned_data['open_seats'] < 0:
                errors.append(ValidationError('Please enter a valid number for Open Seats'))
            if cleaned_data['open_seats'] > cleaned_data['max_seats']:
                errors.append(ValidationError('Open Seats cannot be larger than Max Seats'))

            if errors:
                raise ValidationError(errors)
            
            return cleaned_data

#Form class for the home page
class HomeForm(ModelForm):
	start = forms.CharField(widget = forms.HiddenInput())
	end = forms.CharField(widget = forms.HiddenInput())
	startname = forms.CharField(widget = forms.HiddenInput())
	endname = forms.CharField(widget = forms.HiddenInput())

	class Meta:
		model = Home

class MessageForm(forms.Form):

	recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'));
	#recipients = ModelCommaSeparatedChoiceField(queryset=User.objects.all(), to_field_name='netid');
	title = forms.CharField();
	message = forms.CharField(widget=forms.Textarea);

class MessageFormRide(forms.Form):
	title = forms.CharField();
	message = forms.CharField(widget=forms.Textarea);

class MessageFormConversation(forms.Form):
	title = forms.CharField();
	message = forms.CharField(widget=forms.Textarea);

class MessageFormTarget(forms.Form):
	title = forms.CharField();
	message = forms.CharField(widget=forms.Textarea);

class CancelRideForm(forms.Form):
	cancel = forms.BooleanField();



