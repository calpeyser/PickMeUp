from django.shortcuts import render
from django.http import HttpResponseRedirect
from create_account.forms import UserForm, RideForm, HomeForm
from create_account.models import Location
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
			new_ride = Ride(max_seats = ride_form.cleaned_data['max_seats'], open_seats = ride_form.cleaned_data['open_seats'], driver = User.objects.all()[0], start = Location.objects.all()[0], start_date = ride_form.cleaned_data['start_date'], start_time = ride_form.cleaned_data['start_time'], end = Location.objects.all()[1], payment = ride_form.cleaned_data['payment']);
			new_ride.save();
			return render(request, 'create_account/create_ride.html', {'form': ride_form,})
			#return HttpResponseRedirect('/create_ride/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'create_account/create_ride.html', {
        'form': ride_form,
    })
    
def home(request):
	if request.method == 'POST':
		home_form = HomeForm(request.POST)
		if home_form.is_valid():
			start = Location(home_form.fields['start'], None, None)
			end = Location(home_form.fields['end'], None, None)
			try:
				request.POST['drive']
			except NameError:
				try:
					request.POST['hitch']
				except NameError:
					raise Http404
				return render(request, 'find_ride', {
					start,
					end
				})
			return render(request, 'create_ride', {
				start,
				end
			})
	else:
		home_form = HomeForm()
	return render(request, 'create_account/home.html', {
		'form': home_form,
	})

def authenticate(request):
	# C = CASClient.CASClient()
	# netid = C.Authenticate()
	netid = "peyser"
	request.session["netid"] = netid
	return render(request, '/home')
