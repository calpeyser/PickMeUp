from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.db.models import Q
from create_account.forms import UserForm, RideForm, HomeForm, MessageForm, MessageFormRide, MessageFormConversation, MessageFormTarget, CancelRideForm
from create_account.models import User, Location, Ride, Message, Conversation, Passenger
from message_pruner import *

import datetime
from datetime import datetime
from datetime import date
from django.template import Context


global ROOT 
# ROOT = 'http://carshare.tigerapps.org/'
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
	return render(request, 'create_account/create_ride.html/', {
        'form': user_form,
    })

# view to show form to populate ride data
def ride(request):
	print request.session['netid']
	if request.method == 'POST': # If the form has been submitted...
		start = request.POST.get('startLoc', False)
		end = request.POST.get('endLoc', False)
		swath = request.POST.get('swaths', False)

		print start
		print end
		print swath

		origin = Location.objects.filter(coordinate=start)
		destination = Location.objects.filter(coordinate=end)
	
		if len(origin) > 1:
			raise MultipleObjectsReturned
		if len(destination) > 1:
			raise MultipleObjectsReturned

		ride_form = RideForm(request.POST)
		if ride_form.is_valid():
            # Process the data in form.cleaned_data - eventually populate this from what you get from the homepage
			new_ride = Ride(max_seats = ride_form.cleaned_data['max_seats'], 
				open_seats = ride_form.cleaned_data['open_seats'], 
				driver = User.objects.filter(netid=request.session['netid'])[0],
				start = origin[0], start_date = ride_form.cleaned_data['start_date'], 
				start_time = ride_form.cleaned_data['start_time'], 
				end = destination[0], 
				payment = ride_form.cleaned_data['payment'], 
				swath = swath);
			new_ride.save();
			return render(request, 'create_account/create_ride.html/', {
				'form': ride_form,
				'startLoc': start,
				'endLoc': end,
				'swaths': swath, 
			})
			#return HttpResponseRedirect('/create_ride/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form
	# pass form to HTML
	print "Why am I here?!"
	return render(request, 'create_account/create_ride.html/', {
        'form': ride_form,
        'startLoc': start,
		'endLoc': end,
		'swaths': swath, 
	})
    
# homepage
def home(request):
	global ROOT
	if request.method == 'POST':
		home_form = HomeForm(request.POST)
		if home_form.is_valid():
			origin = Location.objects.filter(coordinate=home_form.cleaned_data['start'])
			destination = Location.objects.filter(coordinate=home_form.cleaned_data['end'])
			
			if len(origin) == 0:
				origin = Location(coordinate = home_form.cleaned_data['start'], name = home_form.cleaned_data['startname'], address = "");
			else:
				origin = origin[0];
			if len(destination) == 0:
				destination = Location(coordinate = home_form.cleaned_data['end'], name = home_form.cleaned_data['endname'], address = "");
			else:
				destination = destination[0];
	
			origin.save();
			destination.save();
			
			request.session['start'] = origin.id
			request.session['end'] = destination.id
			
			option_drive = request.POST.get('drive', False);
			option_hitch = request.POST.get('hitch', False);
			if option_drive:
				return render(request, 'create_account/waiting.html/', {
					'start': origin.coordinate,
					'end': destination.coordinate,
				})
			elif option_hitch:
				return redirect(ROOT + 'find_ride/');
			else:
				raise Http404;
	else:
		home_form = HomeForm()
	return render(request, 'create_account/home.html/', {
		'form': home_form,
	})

# view to show all rides that match a query, hopefully?
def show_rides(request):
	# actually process request
	start = request.session['start']
	end = request.session['end']
	
	originLoc = Location.objects.filter(id=start)
	destinationLoc = Location.objects.filter(id=end)
	pass_user = User.objects.filter(netid=request.session['netid'])

	if len(originLoc) > 1:
		raise MultipleObjectsReturned
	if len(destinationLoc) > 1:
		raise MultipleObjectsReturned

	new_passenger = Passenger(person=pass_user[0], 
		start_loc=originLoc[0], 
		end_loc=destinationLoc[0])

	new_passenger.save();
	
	originList = originLoc.values()[0]['coordinate'].split(',')
	destinationList = destinationLoc.values()[0]['coordinate'].split(',')

	origin = map(float, originList)
	destination = map(float, destinationList)
	
	query = Ride.objects.filter(start_date__gt=datetime.now())
	results = []
	# make list of acceptable rides
	for ride in query:
		openNum = int(ride.open_seats)
		# this is playing w/ pending passengers for testing
		# should be switched to actual passengers after merge w/ Cal
		if ride.passengers.all():
			numPass = len(ride.passengers.all())
		else:
			numPass = 0

		if ((openNum - numPass) <= 0):
			continue

		i = 0
		found_start = False
		found_end = False
		# TODO: if we dont' have reasonable swaths, then match by radius from dest.
		swat = ride.swath.split(',')
		while (i in range(len(swat)) and (not found_end or not found_start)):
			x1 = float(swat[i])
			y1 = float(swat[i+1])
			x2 = float(swat[i+2])
			y2 = float(swat[i+3])

			if x1 <= destination[0] <= x2 and y1 <= destination[1] <= y2:
				found_end = True
				# print "Found end"
			if x1 <= origin[0] <= x2 and y1 <= origin[1] <= y2:
				found_start = True
				# print "Found start"
			i += 4
		if found_start and found_end:
			# find start and end of this ride:
			start_id = ride.start_id
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
	for item in sorted(results, key=lambda ride: ride.start_date):
		start_id = item.start_id
		start_obj = Location.objects.filter(pk=start_id).values()[0]
		end_id = item.end_id
		end_obj = Location.objects.filter(pk=end_id).values()[0]
		resVal = "Ride from " + str(start_obj) + " and going to " + str(end_obj)
		resKey = item.id
		result_list.append({resKey : resVal})
	C = Context({'list': result_list, 'passenger': new_passenger.id})
	return render(request, 'create_account/searchrides.html', C)

def confirm(request):
	if request.method == 'POST':
		print request.POST
		ride_text = request.POST.get('ride_text', False)
		ride_id = request.POST.get('ride_id', False)
		passenger = request.POST.get('passenger', False)
		C = Context({'ride_text': ride_text, 'ride_id': ride_id, 'passenger': passenger})
	return render(request, 'create_account/confirm.html', C)

def add_passenger(request):
	if request.method == 'POST':
		ride_id = request.POST.get('ride_id', False)
		ride_text = request.POST.get('ride_text', False)
		pass_id = request.POST.get('passenger', False)
		ride = Ride.objects.filter(id=ride_id)
		user = Passenger.objects.filter(id=pass_id)
		if len(ride) > 1:
			raise MultipleObjectsReturned
		if len(user) > 1:
			raise MultipleObjectsReturned
		pass_list = ride[0].pending_passengers
		pass_list.add(user[0])
		C = Context({'ride_text': ride_text})
	return render(request, 'create_account/added.html', C)


def write_message(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	if request.method == 'POST': # form submitted
			message_form = MessageForm(request.POST);
			if message_form.is_valid():
				this_conversation = Conversation(title=message_form.cleaned_data['title']);
				this_conversation.save();
				this_participants = message_form.cleaned_data['recipients'];
				for u in this_participants:
					this_conversation.participants.add(u);
				new_message = Message(sender = current_user, title = message_form.cleaned_data['title'], message = message_form.cleaned_data['message'], unread = True, timestamp = datetime.now(), conversation = this_conversation); 
				new_message.save();
				for u in this_participants:
					new_message.recipients.add(u);
				return render(request, 'create_account/home.html')
	else:
		message_form = MessageForm();

	return render(request, 'create_account/write_message.html', {
        'form': message_form,
    })	

def write_message_ride(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	if request.method == 'POST':
		this_ride = Ride.objects.filter(id=request.GET.get('ride'))[0];
		this_participants = this_ride.passengers.all();
		message_form = MessageFormRide(request.POST);
		if message_form.is_valid():
			this_conversation = Conversation(title=message_form.cleaned_data['title']);
			this_conversation.save();
			for u in this_participants:
				this_conversation.participants.add(u);
			new_message = Message(sender=current_user, title=message_form.cleaned_data['title'], message=message_form.cleaned_data['message'], unread=True, timestamp=datetime.now(), conversation=this_conversation);
			new_message.save();
			for u in this_participants:
				new_message.recipients.add(u);
			return render(request, 'create_account/home.html')
	else:
		message_form = MessageFormRide();
	return render(request, 'create_account/write_message.html', {
        'form': message_form,
    })	

def write_message_conversation(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0];

	if request.method == 'POST':
		this_conversation = Conversation.objects.filter(id=request.GET.get('id'))[0];
		this_participants = this_conversation.participants.all();
		message_form = MessageFormConversation(request.POST);
		if message_form.is_valid():
			new_message = Message(sender=current_user, title=message_form.cleaned_data['title'], message=message_form.cleaned_data['message'], unread=True, timestamp=datetime.now(), conversation=this_conversation);
			new_message.save()
			for u in this_participants:
				new_message.recipients.add(u);
			return render(request, 'create_account/home.html')
	else:
		message_form = MessageFormConversation();
	return render(request, 'create_account/write_message.html/', {
        'form': message_form,
    })	

def write_message_target(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0];

	# get the target
	target_user = User.objects.filter(id=request.GET.get('user'))[0];

	if request.method == 'POST':
		message_form = MessageFormTarget(request.POST);
		if message_form.is_valid():
			this_conversation = Conversation(title=message_form.cleaned_data['title']);
			this_conversation.save();
			this_conversation.participants.add(target_user);
			new_message = Message(sender = current_user, title = message_form.cleaned_data['title'], message = message_form.cleaned_data['message'], unread = True, timestamp = datetime.now(), conversation = this_conversation); 
			new_message.save();
			new_message.recipients.add(target_user);
			return render(request, 'create_account/home.html')
	else:
		message_form = MessageFormTarget();
	return render(request, 'create_account/write_message.html', {
        'form': message_form,
    })	


def delete_message(request):
	if request.method == 'GET':
		message_to_delete = Message.objects.filter(id=request.GET.get('id'));
		message_to_delete.delete();

	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	messages = Message.objects.filter(Q(sender=current_user)|Q(recipient=current_user));

	return render(request, 'create_account/inbox.html/', {'messages': messages});


def inbox(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	# get conversations that involve the user.  Map those conversations to their first messages
	conversations_recieved = [];
	conversations_first_messages = [];

	# get messages that the user has recieved, ordered by timestamp
	messages_recieved = message_pruner([]);
	for m in Message.objects.extra(order_by = ['timestamp']):
		if current_user in m.recipients.all():
			messages_recieved.add(m);

	# get only the most recent in each converstaion
	messages_recieved.prune();
	messages_recieved = messages_recieved.return_list();

	return render(request, 'create_account/inbox.html', {'messages_recieved': messages_recieved});

def sent(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	# get conversations that involve the user.  Map those conversations to their first messages
	conversations_recieved = [];
	conversations_first_messages = [];

	# get messages that the user has sent, ordered by timestamp
	messages_recieved = message_pruner([]);
	for m in Message.objects.extra(order_by = ['timestamp']):
		if current_user == m.sender:
			messages_recieved.add(m);

	# get only the most recent in each converstaion
	messages_recieved.prune();
	messages_recieved = messages_recieved.return_list();

	return render(request, 'create_account/sent.html', {'messages_recieved': messages_recieved});

def driver_past(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids
	
	this_ride       = Ride.objects.filter(id=request.GET.get('id'))[0];
	this_passengers = this_ride.passengers.all();
	this_start      = this_ride.start.name;
	this_end        = this_ride.end.name;
	this_start_date = this_ride.start_date;
	this_start_time = this_ride.start_time;

	return render(request, 'create_account/driver_past.html', {'this_ride': this_ride, 'this_passengers': this_passengers, 'this_start': this_start, 'this_end': this_end, 'this_start_date': this_start_date, 'this_start_time': this_start_time, "ROOT":ROOT});


def driver_future(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids
	
	this_ride       = Ride.objects.filter(id=request.GET.get('id'))[0];
	this_passengers = this_ride.passengers.all();
	this_start      = this_ride.start.name;
	this_end        = this_ride.end.name;
	this_start_date = this_ride.start_date;
	this_start_time = this_ride.start_time;

	return render(request, 'create_account/driver_future.html', {'this_ride': this_ride, 'this_passengers': this_passengers, 'this_start': this_start, 'this_end': this_end, 'this_start_date': this_start_date, 'this_start_time': this_start_time, "ROOT":ROOT});

def passenger_past(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	this_ride       = Ride.objects.filter(id=request.GET.get('id'))[0];
	this_passengers = this_ride.passengers.all();
	this_driver     = this_ride.driver;
	this_start      = this_ride.start.name;
	this_end        = this_ride.end.name;
	this_start_date = this_ride.start_date;
	this_start_time = this_ride.start_time;

	return render(request, 'create_account/passenger_past.html', {'this_ride': this_ride, 'this_driver': this_driver, 'this_passengers': this_passengers, 'this_start': this_start, 'this_end': this_end, 'this_start_date': this_start_date, 'this_start_time': this_start_time, "ROOT":ROOT});

def passenger_future(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	this_ride       = Ride.objects.filter(id=request.GET.get('id'))[0];
	this_passengers = this_ride.passengers.all();
	this_driver     = this_ride.driver;
	this_start      = this_ride.start.name;
	this_end        = this_ride.end.name;
	this_start_date = this_ride.start_date;
	this_start_time = this_ride.start_time;

	return render(request, 'create_account/passenger_future.html', {'this_ride': this_ride, 'this_driver': this_driver, 'this_passengers': this_passengers, 'this_start': this_start, 'this_end': this_end, 'this_start_date': this_start_date, 'this_start_time': this_start_time, "ROOT":ROOT});

def cancel_ride(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	this_ride = Ride.objects.filter(id=request.GET.get('id'));

	if request.method == 'POST': # If the form has been submitted...
		cancel_form = CancelRideForm(request.POST)
		if cancel_form.is_valid():
			if (cancel_form.cleaned_data['cancel'] == True):
				this_ride.delete();
			return HttpResponseRedirect('/profile');
	else:
		cancel_form = CancelRideForm() # An unbound form

	return render(request, 'create_account/cancel_ride.html', {
        'form': cancel_form,
    })




def authenticate(request):
	# C = CASClient.CASClient()
	# netid = C.Authenticate()
	netid = "valya"
	# add user to DB if not added before
	test = User.objects.filter(netid=netid)
	if len(test) == 0:
		# for now, add default phone number
		user = User(netid=netid, phone_number="914-555-5555")
		user.save()
	request.session["netid"] = netid
	return redirect('home/')


def profile(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	# Get the rides that the user is currently driving
	current_rides_driving   = Ride.objects.filter(driver=current_user, start_date__gt=date.today());
	# Get the rides that the user is currently a passenger in
	current_rides_passenger = [];
	for ride in Ride.objects.filter(start_date__gt=date.today()):
		for passenger in ride.passengers.all():
			if current_user == passenger:
				current_rides_passenger.append(ride);

	# Get the rides that the user drove in the past
	past_rides_driving      = Ride.objects.filter(driver=current_user, start_date__lt=date.today());
	# Get the rides that the user was a passenger in in the past
	past_rides_passenger = [];
	for ride in Ride.objects.filter(start_date__lt=date.today()):
		for passenger in ride.passengers.all():
			if current_user == passenger:
				past_rides_passenger.append(ride);

	return render(request, 'create_account/profile.html', {'current_rides_driving': current_rides_driving, 'current_rides_passenger': current_rides_passenger, 'past_rides_driving': past_rides_driving, 'past_rides_passenger': past_rides_passenger, 'ROOT': ROOT});

