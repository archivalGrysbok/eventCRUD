from django.db import models
from django import forms
from django.forms import ModelForm, DateField, TimeField, BooleanField, CharField, ChoiceField
from django.forms.widgets import *
from eventCRUD.models import Larp, Run, Player, GM, NPC, UserProfile
from django.contrib.admin import widgets
from django.forms.extras.widgets import *
from django.forms.models import inlineformset_factory
import datetime

#time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
	
class LarpForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	class Meta:
		model=Larp
		exclude = ('larpseries','author')
	spoilerability  = forms.CharField(max_length=3,
                widget=forms.Select(choices=Larp.SPOILERABILITY_CHOICES), help_text="")


class RunForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	name = CharField(help_text='Usually blank (the title of the Larp will be used instead).', required=False)
	startdate = DateField(widget=SelectDateWidget(years=range(datetime.date.today().year - 10, datetime.date.today().year + 2 )), label='Start Date', required=False)
	starttime = TimeField(label='Start Time', required=False, input_formats=valid_time_formats)
	enddate=DateField(widget=SelectDateWidget(years=range(datetime.date.today().year - 10, datetime.date.today().year + 2 )), label='End Date', required=False)
	endtime = forms.TimeField(required=False, help_text='ex: 10:30am', input_formats=valid_time_formats)
	past = BooleanField(help_text="Please check this box if the run occured in the past, but you are unsure of the date", required=False)
	class Meta:
		model=Run
		exclude = ('larp','gm','npc','player')

class GmForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	class Meta:
		model=GM
		exclude = ('run','user')
		
class PlayerForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	characterName = CharField(help_text="If your character is not listed, enter the character name", required=False, label="Name")
	class Meta:
		model=Player
		exclude = ('run','user','publicDescription',)
		
class NpcForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	class Meta:
		model=NPC
		exclude = ('run','user')

class UserProfileForm(ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'
	class Meta:
		model=UserProfile
#		exclude = ('run','userProfile')