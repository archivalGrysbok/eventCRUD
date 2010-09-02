from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, TemplateDoesNotExist, RequestContext
from django.views.generic import list_detail
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template, HttpResponseRedirect

from forms import LarpForm, RunForm, PlayerForm, GmForm, NpcForm, UserProfileForm
from models import Run, Larp, Player, NPC, GM, Author, UserProfile, LarpSeries, Convention, Character

# Create your views here.

def run_detail(request, id):
	"""
	FIXME
	@param request:
	@type request:
	@param id:
	@type id:
	"""
	run = get_object_or_404(Run,pk=id)
	try:
		userProfile = UserProfile.objects.get(pk=request.user.id)
	except:
		userProfile = None
	return list_detail.object_detail(
		request,
		queryset = Run.objects.all(),
		object_id = id,
		template_object_name="run",
		extra_context = {
						'userProfile':userProfile,
						"gm_list":GM.objects.filter(run=id),
						"npc_list":NPC.objects.filter(run=id),
						"player_list":Player.objects.filter(run=id),
						},
		)
			
def larp_detail(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	larp = get_object_or_404(Larp, pk=object_id)
	# Show the detail page
	return list_detail.object_detail(
		request,
		queryset = Larp.objects.all(),
		object_id = object_id,
		template_name="eventCRUD/larp_detail.html",
		template_object_name="larp",
		extra_context= {
						"run_list":larp.run_set.order_by("startdate"),
						"author_list":Author.objects.filter(larp=object_id),
						"character_list":Character.objects.filter(larp=object_id),
		},
	)

def con_detail(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	con = get_object_or_404(Convention,pk=object_id)
	try:
		userProfile = UserProfile.objects.get(pk=request.user.id)
	except:
		userProfile = None
	return list_detail.object_detail(
		request,
		queryset = Convention.objects.all(),
		object_id = object_id,
		template_object_name="convention",
		extra_context = {
						'userProfile':userProfile,
						"run_list":Run.objects.filter(convention=object_id).order_by("startdate"),
						},
		)

#@login_required
def user_detail(request, username):
	"""
	FIXME
	@param request:
	@type request:
	@param username:
	@type username:
	"""
	user = User.objects.get(username=username)
	profile = get_object_or_404(User,pk=user.id)
	return list_detail.object_detail( 
		request,
		object_id=user.id,
		template_name = "eventCRUD/userProfile_detail.html",
		queryset = User.objects.all(),
		template_object_name="aUser",
		)
	

@login_required
def larp_add(request):
	"""
	FIXME
	@param request:
	@type request:
	"""
	if request.method == "POST":
		form = LarpForm(request.POST)
		if form.is_valid():
			larp=form.save()
			return HttpResponseRedirect(larp.get_absolute_url())
	else:
		form = LarpForm()
	
	return render_to_response('eventCRUD/larp_add.html', {
		'form':form, 
		},
		context_instance=RequestContext(request)
	)

@login_required
def run_add(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	larp = get_object_or_404(Larp, pk=object_id)
	aRun = Run(larp=larp)
	if request.method == "POST":
		form = RunForm(request.POST,instance=aRun)
		if form.is_valid():
			run=form.save()
			return HttpResponseRedirect(run.get_absolute_url())
	else:
		form = RunForm()
		form.larp=object_id
	
	return render_to_response('eventCRUD/run_add.html', {
		'form':form, 
		'larp':larp,
		},
		context_instance=RequestContext(request)
	)

@login_required
def run_add_cast(request, run_id):
	"""
	FIXME
	@param request:
	@type request:
	@param run_id:
	@type run_id:
	"""
	run = get_object_or_404(Run, pk=run_id)
	aPlayer = Player(run=run, user=request.user)
	if request.method == "POST":
		form = PlayerForm(request.POST, instance=aPlayer)
		if form.is_valid():
			if request.POST['character']:
				print 'char:'
				print request.POST['character']
				aChar=get_object_or_404(Character, pk=request.POST['character'])
			else:
				print 'huh?'
				print request.POST['character']
				print request.POST['characterName']
				aChar=Character(larp=run.larp, name=request.POST["characterName"])
				aChar.save()
			aPlayer=Player(run=run, user=request.user, character=aChar, characterName=request.POST['characterName'])
			aPlayer.save()
			return HttpResponseRedirect(run.get_absolute_url())
	else:
		form = PlayerForm()
		form.run=run_id
		if run.is_past:
			form.fields["character"].queryset = Character.objects.filter(larp=run.larp)
		else:
			if run.larp.spoilerability != 'ch':
				form.fields["character"].queryset = Character.objects.filter(larp=run.larp).filter(spoiler=False)
			else:
				form.fields["character"].queryset = Character.objects.none()
	return render_to_response('eventCRUD/cast_add.html', {
		'form':form, 
		'run':run,
		},
		context_instance=RequestContext(request)
	)

@login_required
def gm_add(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	run = get_object_or_404(Run, pk=object_id)
	aGM = GM(run=run, user=request.user)
	if request.method == "POST":
		form = GmForm(request.POST,instance=aGM)
		if form.is_valid():
			run=form.save()
			return HttpResponseRedirect(aGM.run.get_absolute_url())
	return HttpResponseRedirect(run.get_absolute_url())
	
@login_required
def npc_add(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	run = get_object_or_404(Run, pk=object_id)
	aNPC = NPC(run=run, user=request.user)
	if request.method == "POST":
		form = NpcForm(request.POST,instance=aNPC)
		if form.is_valid():
			run=form.save()
			return HttpResponseRedirect(aNPC.run.get_absolute_url())
	return HttpResponseRedirect(run.get_absolute_url())

def resume_new(request, username):
	"""
	FIXME
	@param request:
	@type request:
	@param username:
	@type username:
	"""
	try:
		activeUser = User.objects.get(pk=request.user.id)
		activeUserPlayed=activeUser.userProfile.get_larps()
	except:
		activeUser = None
		activeUserPlayed=[]
	resumeUser = User.objects.get(username=username)
	list=[]
	tempList=resumeUser.player_set.select_related(depth=2).order_by("-run__startdate")
	for item in tempList:
		shared=False
		show=True
		if item.character.spoiler:
			show=False
		if item.run.larp in activeUserPlayed:
			shared=True
			show=True
		list.append({'type':'Played', 'cast':item, 'show':show, 'shared':shared})
	tempList=resumeUser.npc_set.select_related(depth=2).order_by("-run__startdate")
	for item in tempList:
		played=False
		if item.run.larp in activeUserPlayed:
			played=True
		list.append({'type':'NPCed', 'cast':item, 'played':played,})
	tempList=resumeUser.gm_set.select_related(depth=2).order_by("-run__startdate")
	for item in tempList:
		played=False
		if item.run.larp in activeUserPlayed:
			played=True
		list.append({'type':'GMed', 'cast':item, 'played':played,})
	tempList=resumeUser.author_set.select_related(depth=2).order_by("larp__title")
	for item in tempList:
		played=False
		if item.run.larp in activeUserPlayed:
			played=True
		list.append({'type':'Authored', 'cast':item, 'played':played,})
		
	return list_detail.object_detail(
		request,
		template_name='eventCRUD/resume_new.html',
		queryset = User.objects.all(),
		object_id=resumeUser.id,
		extra_context=
		{'resumeUser': resumeUser, 
		'cast_list': list,}
		)	

def character_detail(request, id):
	"""
	FIXME
	@param request:
	@type request:
	@param id:
	@type id:
	"""
	character = get_object_or_404(Character,pk=id)
	try:
		userProfile = UserProfile.objects.get(pk=request.user.id)
	except:
		userProfile = None
	return list_detail.object_detail(
		request,
		queryset = Character.objects.all(),
		object_id = id,
		template_object_name="character",
		extra_context = {
						'userProfile':userProfile,
						"player_list":Player.objects.filter(character=character).order_by('character')
						},
		)
		
def search(request):
	"""
	FIXME
	@param request:
	@type request:
	"""
	return direct_to_template(
		request,
		template = "eventCRUD/search.html",
			)
			
def series_detail(request, object_id):
	"""
	FIXME
	@param request:
	@type request:
	@param object_id:
	@type object_id:
	"""
	series = get_object_or_404(LarpSeries, pk=object_id)
	# Show the detail page
	return list_detail.object_detail(
		request,
		queryset = LarpSeries.objects.all(),
		object_id = object_id,
		template_name="eventCRUD/series_detail.html",
		template_object_name="series",
		extra_context= {"larp_list":series.larp_set.order_by('larp2larpseries__order')},
	)

def myhome(request):
	"""
	FIXME
	@param request:
	@type request:
	"""
	if request.user.is_authenticated():
		user = get_object_or_404(User, pk=request.user.id)
		return direct_to_template(
			request,
			template = "eventCRUD/home.html",
			extra_context = {
							'user':user,
							'run_list':Run.objects.filter(startdate__isnull=False).filter(startdate__gt=datetime.now).order_by("startdate")},
			)
	else:
		return direct_to_template(
			request,
			template = "eventCRUD/home.html",
			extra_context = {
			'run_list':Run.objects.filter(startdate__isnull=False).filter(startdate__gt=datetime.now).order_by("startdate")},
			)
