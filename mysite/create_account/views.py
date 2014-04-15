from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from create_account.forms import UserForm, RideForm, HomeForm
from create_account.models import User
from create_account.models import Ride
from create_account.models import Location
import datetime
from datetime import datetime
from django.template import Context


global ROOT 
ROOT = 'http://127.0.0.1:8000/'

# view to show form to populate user data
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

# view to show form to populate ride data
def ride(request):
	start = request.session['start']
	end = request.session['end']
	
	origin = Location.objects.filter(id=start)
	destination = Location.objects.filter(id=end)
	
	#print "startCoord: " + str(startCoord);
	#print "endCoord:   " + str(endCoord);
	
	if len(origin) > 1:
		raise MultipleObjectsReturned
	if len(destination) > 1:
		raise MultipleObjectsReturned

	if len(origin[0].coordinate) == 0:
		##print len(Location.objects.filter(coordinate=startCoord))
		Location.save(origin)
	if len(destination[0].coordinate) == 0:
		Location.save(destination)
	
	if request.method == 'POST': # If the form has been submitted...
		ride_form = RideForm(request.POST)
		if ride_form.is_valid():
            # Process the data in form.cleaned_data - eventually populate this from what you get from the homepage
			new_ride = Ride(max_seats = ride_form.cleaned_data['max_seats'], open_seats = ride_form.cleaned_data['open_seats'], driver = User.objects.all()[0], start = origin, start_date = ride_form.cleaned_data['start_date'], start_time = ride_form.cleaned_data['start_time'], end = destination, payment = ride_form.cleaned_data['payment']);
			new_ride.save();
			print "bound form"
			return render(request, 'create_account/create_ride.html', {'form': ride_form,})
			#return HttpResponseRedirect('/create_ride/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form

	# put the actual html here, probably?
	return render(request, 'create_account/create_ride.html', {
        'form': ride_form,
    })
    
# homepage
def home(request):
	global ROOT
	if request.method == 'POST':
		home_form = HomeForm(request.POST)
		if home_form.is_valid():
			origin = Location(coordinate = home_form.cleaned_data['start'], name = "Test 1", address = "");
			origin.save();
			destination = Location(coordinate = home_form.cleaned_data['end'], name = "Test 2", address = "");
			destination.save();
			
			request.session['start'] = origin.id
			request.session['end'] = destination.id
			
			# This seems to work better than the below for directing to pages. ~Cal
			option_drive = request.POST.get('drive', False);
			option_hitch = request.POST.get('hitch', False);
			if option_drive:
				return redirect(ROOT + 'create_ride/');
			elif option_hitch:
				return redirect(ROOT + 'find_ride/');
			else:
				raise Http404;

			#try:
			#	request.POST['drive']
			#except NameError:
			#	try:
			#		request.POST['hitch']
			#	except NameError:
			#		raise Http404
			#	return redirect('find_ride/')
			#return redirect(ROOT + 'create_ride/')
	else:
		home_form = HomeForm()
	return render(request, 'create_account/home.html', {
		'form': home_form,
	})

# view to show all rides that match a query, hopefully?
def show_rides(request):
	# actually process request, for now hard-code
	start = request.session['start']
	end = request.session['end']
	
	origin = Location.objects.filter(id=start)
	destination = Location.objects.filter(id=end)
	
	#print "startCoord: " + str(startCoord);
	#print "endCoord:   " + str(endCoord);
	
	if len(origin) > 1:
		raise MultipleObjectsReturned
	if len(destination) > 1:
		raise MultipleObjectsReturned
	query = Ride.objects.filter(start_date__gt=datetime.now()).values()
	results = []
	# make list of acceptable rides
	for ride in query:
		i = 0
		found_start = False
		found_end = False
		# if we dont' have reasonable swaths, then match by radius from dest.
		swat = ride['swath'].split(',')
		while (i in range(len(swat)) and (not found_end or not found_start)):
			x1 = float(swat[i])
			y1 = float(swat[i+1])
			x2 = float(swat[i+2])
			y2 = float(swat[i+3])
			if x1 <= destination[0] <= x2 and y1 <= destination[1] <= y2:
				found_end = True
			if x1 <= origin[0] <= x2 and y1 <= origin[1] <= y2:
				found_start = True
			i += 4
		if found_start and found_end:
			# find start and end of this ride:
			start_id = ride['start_id']
			coord_obj = Location.objects.filter(pk=start_id).values()[0]
			coordS = coord_obj['coordinate'].split(',')
			x_dist_origin = abs(origin[0] - float(coordS[0]))
			y_dist_origin = abs(origin[1] - float(coordS[1]))
			x_dist_dest = abs(destination[0] - float(coordS[0]))
			y_dist_dest = abs(destination[1] - float(coordS[1]))
			origin_dist = x_dist_origin*x_dist_origin + y_dist_origin*y_dist_origin
			dest_dist = x_dist_dest*x_dist_dest + y_dist_dest*y_dist_dest
			if origin_dist <= dest_dist:
				results.append(ride)
	result_list = []
	for item in sorted(results, key=lambda ride: ride['start_date']):
		start_id = item['start_id']
		start_obj = Location.objects.filter(pk=start_id).values()[0]
		end_id = item['end_id']
		end_obj = Location.objects.filter(pk=end_id).values()[0]
		result_list.append((start_obj['name'], end_obj['name']))
	C = Context({'list': result_list})
	return render(request, 'create_account/searchrides.html',
		C)

def authenticate(request):
	# C = CASClient.CASClient()
	# netid = C.Authenticate()
	netid = "peyser"
	request.session["netid"] = netid
	return redirect('home/')




