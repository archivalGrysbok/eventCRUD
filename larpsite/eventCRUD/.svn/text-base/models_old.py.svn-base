# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	  * Rearrange models' order
#	  * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor import generic
from django import forms
from django.forms import ModelForm

#class Lengthlookup(models.Model):
#	id = models.IntegerField(primary_key=True,)
#	unit = models.CharField(max_length=135, db_column='Unit')
#
#	def __unicode__(self):
#		return self.unit
#
#	class Meta:
#		db_table = u'LengthLookup'


class Location(models.Model):
	city = models.CharField(max_length=135, blank=True, null=True)
	state = models.CharField(max_length=135, blank=True, null=True)
	country = models.CharField(max_length=135, blank=True, null=True)
	def __unicode__(self):
		return u'%s, %s' % (self.city,self.state)

class Larp(models.Model):
	id = models.AutoField(primary_key=True,)
	name = models.CharField(max_length=135, blank=True)
	subtitle = models.CharField(max_length=135, blank=True)
	url = models.URLField(max_length=135, blank=True)
	blurb = models.TextField(max_length=5000, blank=True, null=True)
	description = models.TextField(max_length=15000, blank=True, null=True)
	minsize = models.IntegerField(null=True, blank=True)
	maxsize = models.IntegerField(null=True, blank=True)
	length = models.IntegerField(null=True, blank=True) 
	LENGTH_UNIT_CHOICES = (
		('mi', 'minute'),
		('hr', 'hour'),
		('dy', 'day'),
		('wl', 'weekend-long'),
	)
	unit = models.CharField(max_length=2, choices=LENGTH_UNIT_CHOICES,null=True, blank=True)
	def __unicode__(self):
		return self.name

class Conseries(models.Model):
	name = models.CharField(max_length=135,)
	def __unicode__(self):
		return u'%s' % (self.name)

class Convention(models.Model):
	name = models.CharField(max_length=135,)
	location = models.ForeignKey(Location, max_length=135, blank=True, null=True)
	Conseries = models.ForeignKey(Conseries, max_length=135, blank=True, null=True)
	start_date = models.DateTimeField(null=True, blank=True)
	end_date = models.DateTimeField(null=True, blank=True)
	def __unicode__(self):
		return u'%s' % (self.name)
	
class Event(models.Model):
	id = models.AutoField(primary_key=True,)
	larpid = models.ForeignKey(Larp,)
	date = models.DateTimeField(null=True, blank=True)
	time_given = models.BooleanField(default="0")
	public = models.BooleanField(default=True)
	convention = models.ForeignKey(Convention, max_length=135, null=True, blank=True)
	location = models.ForeignKey(Location, max_length=135, blank=True, null=True,)
	notes = models.CharField(max_length=135, blank=True)
	def __unicode__(self):
		value = u''
		if self.convention is None:
			value = value+u' %s' % (self.larpid.name)
		else:
			value = value+u' %s' % (self.larpid.name)
			value = value+u' @ %s' % (self.convention)
#		try:
#			value = value+u': %s' % (self.date.hour)
#			except:
#				pass
#		elif self.date:
#			value = value+u' %s,' % (self.date.date().strftime("%B %d, %Y"))
#		else:
#			if self.date:
#				value = value+u' %s:' % (self.date.date().strftime("%B %d, %Y"),)
#		value = value+u' %s' % (self.larpid.name)
		return value

class Event2(models.Model):
	id = models.AutoField(primary_key=True,)
	larpid = models.ForeignKey(Larp,)
	start_date = models.DateTimeField(null=True, blank=True)
	end_date = models.DateTimeField(null=True, blank=True)
	time_given = models.BooleanField(default="0")
	public = models.BooleanField(default=True)
	convention = models.ForeignKey(Convention, max_length=135, null=True, blank=True)
	location = models.ForeignKey(Location, max_length=135, blank=True, null=True,)
	notes = models.CharField(max_length=135, blank=True)
	def __unicode__(self):
		value = u''
		if self.convention is None:
			value = value+u' %s' % (self.larpid.name)
		else:
			value = value+u' %s' % (self.larpid.name)
			value = value+u' @ %s' % (self.convention)
#		try:
#			value = value+u': %s' % (self.date.hour)
#			except:
#				pass
#		elif self.date:
#			value = value+u' %s,' % (self.date.date().strftime("%B %d, %Y"))
#		else:
#			if self.date:
#				value = value+u' %s:' % (self.date.date().strftime("%B %d, %Y"),)
#		value = value+u' %s' % (self.larpid.name)
		return value

class Person(models.Model):
	id = models.AutoField(primary_key=True,)
	givenname = models.CharField(max_length=135, blank=True,)
	familyname = models.CharField(max_length=135, null=True, blank=True,)
	events_played = models.ManyToManyField(Event, blank=True, null=True, through="Playerevent", related_name="gmedevent_set")
	events_gmedp = models.ManyToManyField(Event, blank=True, null=True, through="Gmevent", related_name="playedevent_set") 
	def __unicode__(self):
		return u'%s. %s.' %  (self.givenname[0], self.familyname[0])

class UserProfile(models.Model):
	url = models.URLField(blank=True)
	phone_number = models.CharField(max_length=135, blank=True)
	user = models.ForeignKey(User, unique=True, primary_key=True)
	personid = models.ForeignKey(Person, unique=True)
	def get_absolute_url(self):
		return ('profiles_profile_detail', (), { 'username': self.user.username })
	get_absolute_url = models.permalink(get_absolute_url)
	def __unicode__(self):
		return self.user.username

class Larpchar(models.Model):
	larp = models.ForeignKey(Larp,)
	name = models.CharField(max_length=135,)
	spoiler = models.BooleanField()
	aka = models.ManyToManyField("self", blank=True, null=True,) 
	main = models.BooleanField()
	TYPE_CHOICES = (
		('pc','Player Character'),
		('np','Non-Player Character'),
		('ho','Horde'),
	)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="pc")
	GENDER_CHOICES = (
		('m','male'),
		('f','female'),
		('n','neutral'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)
	def __unicode__(self):
		return u'%s' %  (self.name)

class Gmevent(models.Model):
	person = models.ForeignKey(Person,)
	event = models.ForeignKey(Event,)
	title = models.CharField(max_length=135, null=True, blank=True)
#	spoiler = models.BooleanField()
	def __unicode__(self):
		return u'%s, %s' %  (self.person, self.title)


class Playerevent(models.Model):
	person = models.ForeignKey(Person,)
	event = models.ForeignKey(Event,)
	larpchar = models.ForeignKey(Larpchar, null=True, blank=True,)
#	spoiler = models.BooleanField()
	def __unicode__(self):
		return u'%s' %  (self.person)

class Larpperson(models.Model):
	larp = models.ForeignKey(Larp,)
	person = models.ForeignKey(Person,)
	ROLE_CHOICES = (
		('au','Author'),
		('co','Co-author'),
		('ed','Editor'),
	)
	role = models.CharField(max_length=2, choices=ROLE_CHOICES, null=True, blank=True)
	def __unicode__(self):
		return u'%s, %s' %  (self.person, self.role)