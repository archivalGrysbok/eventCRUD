from django.conf.urls.defaults import *
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from views import run_detail, larp_detail, larp_add, run_add, run_add_cast,  character_detail, search, series_detail, con_detail, user_detail, gm_add, npc_add, resume_new, myhome
from models import Run, Larp, UserProfile
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

people_info = {
	'queryset': UserProfile.objects.all(),
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
	(r'run/(?P<object_id>\d+)/npc_add/$', npc_add),
	
	(r'run/add/(?P<object_id>\d+)/$', run_add),

	(r'games/$',  list_detail.object_list, larp_info),
	(r'games/[-\d]+/(?P<id>\d+)/[-\w]*$', run_detail),
	(r'games/(?P<object_id>\d+)/[-\w]*$', larp_detail),
	(r'larp/add/$', larp_add),
	(r'games/add/$', larp_add),

	(r'convention/(?P<object_id>\d+)/$', con_detail),
#	(r'convention/$', list_detail.object_list, con_info),

	(r'character/(?P<id>\d+)/$', character_detail),

	(r'series/(?P<object_id>\d+)/$', series_detail),
	(r'campaign/(?P<object_id>\d+)/$', series_detail),

	(r'people/$',  list_detail.object_list, people_info),
	(r'people/(?P<username>\w+)/resume/$', resume_new),
	(r'people/(?P<username>\w+)/resume_new/$', resume_new),

	(r'people/(?P<username>\w+)/$', user_detail),	
	
	(r'home/$', myhome),

#	(r'^feed/$', UpcomingRunsFeed()),

	(r'^$', myhome),
)
