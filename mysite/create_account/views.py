from django.shortcuts import render
from django.http import HttpResponseRedirect
from create_account.forms import UserForm, RideForm
from create_account.models import User
from create_account.models import Ride
from create_account.models import Location


def user(request):
	if request.method == 'POST': # If the form has been submitted...
		user_form = UserForm(request.POST)
		if user_form.is_valid():
            # Process the data in form.cleaned_data
			user_form.save()
			return HttpResponseRedirect('create_account/') # Redirect after POST -- do we want this?
	else:
		user_form = UserForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'create_account/create_ride.html', {
        'form': user_form,
    })

def ride(request):
	if request.method == 'POST': # If the form has been submitted...
		ride_form = RideForm(request.POST)
		if ride_form.is_valid():
            # Process the data in form.cleaned_data - eventually populate this from what you get from the homepage
			ride_form.driver     = d;
			ride_form.passengers = User.objects.all()[1];
			ride_form.start      = Location.objects.all()[0];
			ride_form.end        = Location.objects.all()[1];
			ride_form.save();

			return render(request, 'create_account/create_ride.html', {'form': ride_form,})			
			#return HttpResponseRedirect('/create_ride/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'create_account/create_ride.html', {
        'form': ride_form,
    })

