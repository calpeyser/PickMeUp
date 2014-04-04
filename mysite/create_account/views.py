from django.shortcuts import render
from django.http import HttpResponseRedirect
import forms

def user(request):
	if request.method == 'POST': # If the form has been submitted...
		user_form = UserForm(request.POST)
		if user_form.is_valid():
            # Process the data in form.cleaned_data
            user_form.save()
			return HttpResponseRedirect('/thanks/') # Redirect after POST -- do we want this?
	else:
		user_form = UserForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'contact.html', {
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

# Create your views here.
def test_view(request):
	return render(request, 'create_account/index.html');
