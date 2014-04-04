from django.forms import ModelForm

# Create the form class for users
class UserForm(ModelForm):
	class Meta:
		model = User

# Create the form class for rides
class RideForm(ModelForm):
	class Meta:
		model = Ride