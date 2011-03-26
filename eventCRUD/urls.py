from django.conf.urls.defaults import *
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from views import run_detail, larp_detail, larp_add, run_add, run_add_cast, author_add, author_delete, character_detail, search, series_detail, con_detail, user_detail, gm_add, gm_delete, npc_add, npc_delete, player_delete, resume_new, myhome, convention_add, location_add, run_edit, larp_edit
from models import Run, Larp, UserProfile, Convention
from django.template.defaultfilters import slugify
from django.views.generic.simple import direct_to_template
#from feeds import UpcomingRunsFeed

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

run_info = {
	'queryset': Run.objects.order_by("startdate").reverse(),
	'template_object_name': 'run',
}

larp_info = {
	'queryset': Larp.objects.order_by('title'),
	'template_object_name': 'larp',
}

convention_info = {
	'queryset': Convention.objects.order_by('title'),
	'template_object_name': 'convention',
}

location_info = {
	'queryset': Convention.objects.order_by('name'),
	'template_object_name': 'location',
}

people_info = {
	'queryset': UserProfile.objects.order_by('displayName'),
	'template_object_name': 'userProfile',
	'template_name':'eventCRUD/userProfile_list.html'
}

#con_info = {
#	'queryset': Convention.objects.all(),
#	'template_object_name': 'con',
#}

urlpatterns = patterns('',
#	(r'run/$',  list_detail.object_list, run_info),
#	(r'run/(?P<id>\d+)/[-\w]*$', run_detail),
	(r'run/(?P<run_id>\d+)/add_cast/$', run_add_cast),
	(r'run/(?P<object_id>\d+)/gm_add/$', gm_add),
	(r'run/(?P<object_id>\d+)/gm_delete/(?P<gm_id>\d+)/$', gm_delete),
	(r'games/(?P<object_id>\d+)/author_add/$', author_add),
	(r'games/(?P<object_id>\d+)/author_delete/(?P<author_id>\d+)/$', author_delete),
	(r'run/(?P<object_id>\d+)/npc_add/$', npc_add),
	(r'run/(?P<object_id>\d+)/npc_delete/(?P<npc_id>\d+)/$', npc_delete),
	(r'run/(?P<object_id>\d+)/player_delete/(?P<player_id>\d+)/$', player_delete),
	(r'run/(?P<object_id>\d+)/edit/$', run_edit),
	(r'run/(?P<id>\d+)/[-\w]*$', run_detail),

	(r'run/add/(?P<object_id>\d+)/$', run_add),

	(r'games/$',  list_detail.object_list, larp_info),
	(r'games/[-\d]+/(?P<id>\d+)/[-\w]*$', run_detail),
	(r'games/(?P<object_id>\d+)/[-\w]*$', larp_detail),
	(r'larp/add/$', larp_add),
	(r'games/add/$', larp_add),
	(r'larp/(?P<object_id>\d+)/edit/$', larp_edit),
	(r'games/(?P<object_id>\d+)/edit/$', larp_edit),

	(r'location/add/$', location_add),
	(r'locations/add/$', location_add),
	(r'locations/add/$', list_detail.object_list, location_info),
	(r'conventions/$', list_detail.object_list, convention_info),
	(r'conventions/add/$', convention_add),
	(r'conventions/(?P<object_id>\d+)/$', con_detail),
	(r'convention/(?P<object_id>\d+)/$', con_detail),
#	(r'convention/$', list_detail.object_list, con_info),

	(r'character/(?P<id>\d+)/$', character_detail),

	(r'series/(?P<object_id>\d+)/$', series_detail),
	(r'campaign/(?P<object_id>\d+)/$', series_detail),

	(r'people/$',  list_detail.object_list, people_info),
	(r'people/(?P<username>\w+)/resume/$', resume_new),
	(r'people/(?P<username>\w+)/resume_new/$', resume_new),

#	(r'people/(?P<username>\w+)/$', user_detail),	
	(r'people/(?P<username>\w+)/$', resume_new),
	
	(r'home/$', myhome),

#	(r'^feed/$', UpcomingRunsFeed()),

	(r'^$', myhome),
)
