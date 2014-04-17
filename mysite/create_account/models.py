from django.db import models

class User(models.Model):
	netid          = models.CharField(max_length = 50, unique = True);
	phone_number   = models.CharField(max_length = 12); # eventually, validate with regexp
	rating         = models.BinaryField(null = True);

	def __unicode__(self):
		return unicode(self.netid)

class Location(models.Model):
	coordinate     = models.CharField(max_length = 100); # replace 50 with actual coordinate length, validate with regexp
	name           = models.CharField(max_length = 50, null = True);
	address        = models.CharField(max_length = 100, null = True);
	
	def __unicode__(self):
		return unicode(self.name)

class Ride(models.Model):
	max_seats      = models.IntegerField();
	open_seats     = models.CommaSeparatedIntegerField(max_length = 16); # ideally, the max length should be max_seats
	driver         = models.ForeignKey(User, related_name='driver_of'); # foreignkey = manyToOne
	passengers     = models.ManyToManyField(User, related_name='passengers_of'); 
	start          = models.ForeignKey(Location, related_name='start_of');
	start_date     = models.DateField(null = True); 
	start_time     = models.TimeField(null = True);
	end            = models.ForeignKey(Location, related_name='end_of');
	swath          = models.CharField(max_length = 1000); # might want to tweak this but eh?
	payment        = models.IntegerField(null = True);

	def __unicode__(self):
		return unicode(self.swath)

	#--------------PLACEHOLDER METHOD--------------------#
	def generate_swath(self):
		return []
		
class Home(models.Model):
	start = models.CharField(max_length = 50);
	end = models.CharField(max_length = 50);
	
	def __unicode__(self):
		return unicode('start')

class Message(models.Model):
	sender         = models.ForeignKey(User, related_name='sender_of');
	recipient      = models.ForeignKey(User, related_name='recipient_of');
	title          = models.CharField(max_length = 500);
	message        = models.CharField(max_length = 10000);
	timestamp      = models.DateTimeField();
	unread         = models.BooleanField(default=True);

	def __unicode__(self):
		return unicode('title');

class Conversation(models.Model):
	initiator     = models.ForeignKey(User, related_name='initiator_of');
	responder     = models.ForeignKey(User, related_name='responder-of');
	messages      = models.ManyToManyField(Message, related_name='messages_of');

	def __unicode__(self):
		return "Conversation between " + unicode('initiator') + " and " + unicode('responder');

