from django.db import models
from django.contrib.auth.models import User
import time
import datetime
from django.template.defaultfilters import slugify

# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True, primary_key=True)
	displayName = models.CharField(max_length=135, blank=True, null=True)
	def __unicode__(self):
		if self.displayName:
			return u'%s' % (self.displayName)
		else:
			return u'%s' % (self.user)
	def get_absolute_url(self):
		return u'/people/%s/' % (self.user )
	def get_larps(self):	#returns larps that the user has played in in the past, or has/will GM, for spoiler purposes
		gmSet=self.user.gm_set.all()
		npcSet=self.user.npc_set.all()
		playerSet=self.user.player_set.all()
		authorSet=self.user.author_set.all()
		list=[]
		for item in gmSet:
			list.append(item.run.larp)
		for item in npcSet:	
			list.append(item.run.larp)
		for item in playerSet:
 			if item.run.is_past:
				list.append(item.run.larp)
			else:
				pass
		for item in authorSet:
			list.append(item.larp)		
		return list
#	def get_name:
#		if displayName:
#			return displayName
#		else:
#			return user

User.userProfile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]) ##create userProfile if one isn't already in existance

class Location(models.Model):
	name = models.CharField(max_length=135, blank=True, null=True) 
	city = models.CharField(max_length=135, blank=True, null=True)
	state = models.CharField(max_length=135, blank=True, null=True)
	country = models.CharField(max_length=135, blank=True, null=True)
	def __unicode__(self):
		value=""
		prev=0
		if self.name:			#todo: pretify this
			value = value+u'%s' % (self.name)
			prev=1
		if self.city:
			if prev==1:
				value=value+u', '
			value = value+u'%s' % (self.city)
		else:
			prev=0
		if self.state:
			if prev==1:
				value=value+u', '
			value = value+u'%s' % (self.state)
		return value

class LarpSeries(models.Model):
	name = models.CharField(max_length=135)
	url = models.URLField(max_length=135, blank=True)
	TYPE_CHOICES = (
		('c', 'campaign'),
		('s', 'series'),
	)
	description = models.TextField(max_length=15000, blank=True, null=True)
	type = models.CharField(max_length=1, choices=TYPE_CHOICES,)
	def __unicode__(self):
		return u'%s, %s' % (self.name,self.get_type_display())
	def get_absolute_url(self):
		if self.type == 'c':
			return "/campaigns/%i/" % self.id
		
		if self.type == 's':
			return "/series/%i/" % self.id

class Larp(models.Model):
	title = models.CharField(max_length=135)
	SPOILERABILITY_CHOICES = (
		('no', 'normal'),
		('un', 'impossible to spoil'),
		('ch', 'easily spoiled'),
	)
	spoilerability = models.CharField(max_length=2, choices=SPOILERABILITY_CHOICES, default="no")
#	slug = models.SlugField(max_length=135, blank=True, null=True)
	subtitle = models.CharField(max_length=135, blank=True)
	larpseries = models.ManyToManyField(LarpSeries, max_length=135, blank=True, null=True, through="Larp2LarpSeries")
	url = models.URLField(max_length=135, blank=True)
	summary = models.TextField(max_length=5000, blank=True, null=True)
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
	author = models.ManyToManyField(User, blank=True, null=True, through="Author",)
#	def save(self, **kwargs):
#		self.slug = slugify(self.title)
#		super(Larp, self).save(**kwargs)
	def get_absolute_url(self):
	    return "/larp/%i/%s" % (self.id, self.slug)
	def __unicode__(self):
		if self.subtitle:
			return u'%s: %s' % (self.title, self.subtitle)
		else:
			return self.title
	def get_runs(self):
		return self.run_set
	def _get_length(self):
		if self.unit is None:
			return None
		else:
			if self.unit == 'wl':
				return "weekend-long"
			else:
				return u'%s-%s' % (self.length, self.get_unit_display())
	get_length=property(_get_length)
	def _slug(self):
		return slugify(self.title)
	slug=property(_slug)
	def get_absolute_url(self):
		return "/games/%i/%s" % (self.id, self.slug)
	class Meta:
		ordering = ['title']
		
class Convention(models.Model):
	title = models.CharField(max_length=135,)
	location = models.ForeignKey(Location, max_length=135, blank=True, null=True)
	startdate = models.DateField(null=True, blank=True)
	enddate = models.DateField(null=True, blank=True)
	def get_absolute_url(self):
		return u'/convention/%s/' % (self.id )
	def __unicode__(self):
		return u'%s' % (self.title)

class Character(models.Model): # formerly Role
	name = models.CharField(max_length=135)
	#larp = models.ManyToManyField(Larp)
	larp = models.ForeignKey(Larp)
	publicDescription = models.CharField(max_length=500, blank=True, null=True)
	spoiler = models.BooleanField(default=False)
	def get_absolute_url(self):
	    return "/character/%i/" % self.id
	def __unicode__(self):
		return u'%s' % (self.name)
	def _get_spoiler(self):
		if self.larp.spoilerability=='ch':
			return True
		else:
			return self.spoiler
	is_spoiler=property(_get_spoiler)

#class Character(models.Model):
#	name = models.CharField(max_length=135)
#	role = models.ForeignKey(Role)
#	def __unicode__(self):
#		return u'%s' % (self.name)

class Run(models.Model):
#	name = models.CharField(max_length=135, blank=True) #event name
#	slug = models.SlugField(max_length=135, blank=True, null=True)
	url = models.URLField(max_length=135, blank=True)
	location= models.ForeignKey(Location, max_length=135, blank=True, null=True,)
	convention = models.ForeignKey(Convention, max_length=135, null=True, blank=True)
	notes = models.TextField(max_length=15000, blank=True, null=True)
	startdate = models.DateField(null=True, blank=True)
	starttime=models.TimeField(null=True, blank=True)
	enddate = models.DateField(null=True, blank=True,)
	endtime=models.TimeField(null=True, blank=True)
	past = models.BooleanField(default=True)
	larp = models.ForeignKey(Larp,)
	tentative = models.BooleanField(default=False)
	public = models.BooleanField(default=True)
	gm = models.ManyToManyField(User, blank=True, null=True, through="GM",  related_name="gms")
	player = models.ManyToManyField(User, blank=True, null=True, through="Player", related_name="players")
	npc = models.ManyToManyField(User, blank=True, null=True, through="NPC",  related_name="npcs")
#	def save(self, **kwargs):
#		self.slug = slugify(self.name)
#		super(Run, self).save(**kwargs)
	def __unicode__(self):
		value = u''
#		if self.name == "":
#			value=value+u'%s' % (self.larp)
#		else:
		value = value+u' %s ' % (self.larp)
		if self.convention is None:
			if self.location is None:
				pass
			else:
				value = value+u' @ %s' % (self.location.name)
		else:
			value = value+u' @ %s' % (self.convention)
		return value
#	def title(self):
#		value = u''
#		if self.name == "":
#			value=value+u'%s' % (self.larp)
#		else:
#			value = value+u' %s ' % (self.name)
#		return value
	def _is_past(self):
		try:
			if (datetime.date.today()-self.startdate.date()).days>0:	##errors out if item.run.stardate not defined, hence the try/except. Todo: fix this
				return True
		except:
			if self.past:
				return True
		else:
			return False
	is_past = property(_is_past)
	def _time_given(self):
		if self.starttime:
			return True
		return False
	time_given = property(_time_given)
	def _get_location(self):
		if self.location:
			return self.location
		else:
			if self.convention.location:
				return self.convention.location
			else:
				return "unknown location"
	get_location = property(_get_location)
	def _slug(self):
		return slugify(self.larp.name)
	slug=property(_slug)
	def get_absolute_url(self):
#		t= slugify(self.name)
		return "/games/%i/%i/%s" % (self.larp.id, self.id, self.larp.slug)
	class Meta:
		ordering = ['startdate']

class Author(models.Model):
	larp = models.ForeignKey(Larp, related_name="authorlarp_set")
	user = models.ForeignKey(User, blank=True, null=True)
	displayName = models.CharField(max_length=135, blank=True, null=True)
	def __unicode__(self):
		if self.displayName:
			return u'%s' % (self.displayName)
		else:
			return u'%s' % (self.user.userProfile)


class Cast(models.Model):
	run=models.ForeignKey(Run, related_name="%(app_label)s_%(class)s_related")
	user = models.ForeignKey(User, blank=True, null=True)
	class Meta:
		abstract = True
	def __unicode__(self):
		return u'%s' % (self.user.userProfile)

class GM(Cast):
	pass
		
class NPC(Cast):
	pass

class Player(Cast):
	character = models.ForeignKey(Character, blank=True, null=True)
	characterName = models.CharField(max_length=135, blank=True, null=True)
#	quote = models.CharField(max_length=135, blank=True)
	def get_name(self):
		if self.characterName:
			return self.characterName
		else:
			return self.character.name
		
class Larp2LarpSeries(models.Model):
	larpSeries=models.ForeignKey(LarpSeries,)
	larp = models.ForeignKey(Larp, unique=True)
	order = models.PositiveIntegerField(null=True, blank=True) 
	def __unicode__(self):
		return u'%s' % (self.larp)
