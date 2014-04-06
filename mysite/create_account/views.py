import CASClient, os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from create_account.forms import UserForm, RideForm, HomeForm
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
	return render(request, 'create_account/index.html', {
        'form': user_form,
    })

def ride(request):
	if request.method == 'POST': # If the form has been submitted...
		ride = RideForm(request.POST)
		if ride_form.is_valid():
            # Process the data in form.cleaned_data
			ride_form.save()
			return HttpResponseRedirect('/thanks/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'contact.html', {
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
	C = CASClient.CASClient()
	netid = C.Authenticate()
	print "Hello %s" % netid
