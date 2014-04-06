from django.db import models

class User(models.Model):
	netid          = models.CharField(max_length = 50, unique = True);
	phone_number   = models.CharField(max_length = 12); # eventually, validate with regexp
	rating         = models.BinaryField(null = True);

class Location(models.Model):
	coordinate     = models.CharField(max_length = 50); # replace 50 with actual coordinate length, validate with regexp
	name           = models.CharField(max_length = 50, null = True);
	address        = models.CharField(max_length = 100, null = True);

class Ride(models.Model):
	max_seats      = models.IntegerField();
	open_seats     = models.CommaSeparatedIntegerField(max_length = 16); # ideally, the max length should be max_seats
	driver         = models.OneToOneField(User, related_name='driver_of');
	passengers     = models.ManyToManyField(User, related_name='passengers_of'); 
	start          = models.OneToOneField(Location, related_name='start_of');
	start_date     = models.DateField(null = True); 
	start_time     = models.TimeField(null = True);
	end            = models.OneToOneField(Location, related_name='end_of');
	payment        = models.IntegerField(null = True);
	
class Home(models.Model):
	start = models.CharField(max_length = 50);
	end = models.CharField(max_length = 50);


	#--------------PLACEHOLDER METHOD--------------------#
	def generate_swath(self):
		return [];
	#----------------------------------------------------#s