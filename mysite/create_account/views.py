from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.db.models import Q
from create_account.forms import UserForm, RideForm, HomeForm, MessageForm
from create_account.models import User, Location, Ride, Message, Conversation


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
	if request.method == 'POST': # If the form has been submitted...
		start = request.POST.get('startLoc', False)
		end = request.POST.get('endLoc', False)
		swath = request.POST.get('swaths', False)

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
			return render(request, 'create_account/create_ride.html', {
				'form': ride_form,
				'startLoc': start,
				'endLoc': end,
				'swaths': swath, 
			})
			#return HttpResponseRedirect('/create_ride/') # Redirect after POST -- do we want this?
	else:
		ride_form = RideForm() # An unbound form
	# pass form to HTML
	return render(request, 'create_account/create_ride.html', {
        'form': ride_form,
		'startLoc': str(start),
		'endLoc': str(end),
		'swaths': str(swath),
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
				return render(request, 'create_account/waiting.html', {
					'start': origin.coordinate,
					'end': destination.coordinate,
				})
			elif option_hitch:
				return redirect(ROOT + 'find_ride/');
			else:
				raise Http404;
	else:
		home_form = HomeForm()
	return render(request, 'create_account/home.html', {
		'form': home_form,
	})

# view to show all rides that match a query, hopefully?
def show_rides(request):
	# actually process request
	start = request.session['start']
	end = request.session['end']
	
	originLoc = Location.objects.filter(id=start).values()
	destinationLoc = Location.objects.filter(id=end).values()

	if len(originLoc) > 1:
		raise MultipleObjectsReturned
	if len(destinationLoc) > 1:
		raise MultipleObjectsReturned
	
	originList = originLoc[0]['coordinate'].split(',')
	destinationList = destinationLoc[0]['coordinate'].split(',')

	origin = map(float, originList)
	destination = map(float, destinationList)
	
	query = Ride.objects.filter(start_date__gt=datetime.now()).values()
	results = []
	# make list of acceptable rides
	for ride in query:
		i = 0
		found_start = False
		found_end = False
		# TODO: if we dont' have reasonable swaths, then match by radius from dest.
		swat = ride['swath'].split(',')
		while (i in range(len(swat)) and (not found_end or not found_start)):
			x1 = float(swat[i])
			y1 = float(swat[i+1])
			x2 = float(swat[i+2])
			y2 = float(swat[i+3])

			# print x1
			# print y1
			# print x2
			# print y2
			# print "Test!"
			# print origin[0]
			# print origin[1]
			# print destination[0]
			# print destination[1]
			# print "Test finished?"

			# print x1 <= destination[0] <= x2
			# print y1 <= destination[1] <= y2
			# print "Really end test..."

			if x1 <= destination[0] <= x2 and y1 <= destination[1] <= y2:
				found_end = True
				# print "Found end"
			if x1 <= origin[0] <= x2 and y1 <= origin[1] <= y2:
				found_start = True
				# print "Found start"
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
		res = "Ride from " + str(start_obj) + " and going to " + str(end_obj)
		result_list.append(res)
	C = Context({'list': result_list})
	return render(request, 'create_account/searchrides.html',
		C)

def write_message(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	if request.method == 'POST': # If the form has been submitted...
		message_form = MessageForm(request.POST)
		if message_form.is_valid():
			# if this is a not a new conversation, this goes to the given conversation
			if request.method == 'GET':
				this_conversation = Conversation.objects.filter(id=request.GET.get('id'));
				this_participants = this_conversation.participants;
			else:
				this_conversation = Conversation(title=message_form.cleaned_data['title']);
				this_conversation.save();
				this_participants = message_form.cleaned_data['recipients'];
				for u in this_participants:
					this_conversation.participants.add(u);
			new_message = Message(sender = current_user, title = message_form.cleaned_data['title'], message = message_form.cleaned_data['message'], unread = True, timestamp = datetime.now(), conversation = this_conversation); 
			new_message.save();
			for u in this_participants:
				new_message.recipients.add(u);
			return render(request, 'create_account/write_message.html', {'form': message_form,})
	else:
		message_form = MessageForm() # An unbound form

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

	return render(request, 'create_account/inbox.html', {'messages': messages});


def inbox(request):
	netid = request.session['netid'];
	current_user = User.objects.filter(netid=netid)[0]; # assume unique netids

	# get conversations that involve the user.  Map those conversations to their first messages
	conversations_recieved = [];
	conversations_first_messages = [];

	for c in Conversation.objects.all():
		if current_user in c.participants.all():
			messages = Message.objects.filter(conversation=c);
			messages = messages.order_by('timestamp');
			conversations_recieved.append((c));



	return render(request, 'create_account/inbox.html', {'conversations_recieved': conversations_recieved, 'first_messages': conversations_first_messages});

def sent(request):
	netid             = request.session['netid'];
	current_user      = User.objects.filter(netid=netid)[0]; # assume unique netids

	messages_sent     = Message.objects.filter(sender=current_user);

	return render(request, 'create_account/sent.html', {'messages_sent': messages_sent});


def authenticate(request):
	# C = CASClient.CASClient()
	# netid = C.Authenticate()
	netid = "daniel"
	# add user to DB if not added before
	test = User.objects.filter(netid=netid)
	if len(test) == 0:
		# for now, add default phone number
		user = User(netid=netid, phone_number="609-555-5555")
		user.save()
	request.session["netid"] = netid
	return redirect('home/')




