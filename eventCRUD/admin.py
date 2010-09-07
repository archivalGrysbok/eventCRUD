from django.contrib import admin
from models import Convention, Run, Larp, Location, Player, GM, NPC, Author, LarpSeries, Character, UserProfile, Larp2LarpSeries
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.forms.models import modelformset_factory

PlayerFormSet = modelformset_factory(Player)

#Player.character.role.larp = Run.larp
class PlayerInlineForm(forms.ModelForm):
    class Meta:
        model = Player
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if 'instance' in kwargs:
	        run = kwargs['instance'].run
            #larp = kwargs['instance'].character.role.larp
        else:
            run_id = tuple(i[0] for i in self.fields['run'].widget.choices)[1]
            run=Run.objects.get(id=run_id)
            run2=self.fields['run'].widget
            print run2
      #      print run2.id

        larp = Larp.objects.get(id=run.larp.id)
        self.fields['character'].queryset = Character.objects.filter(larp=larp)

class ConventionAdmin(admin.ModelAdmin):
	list_display = ('title','location','startdate','enddate',)
	pass
		
class PlayerInline(admin.TabularInline):
	model = Player
	extra = 3
#	form = PlayerInlineForm
#	formset = PlayerFormSet(queryset=Player.objects.filter(run=1))
   
class GMInline(admin.TabularInline):
	model = GM
	extra = 3

class NPCInline(admin.TabularInline):
	model = NPC
	extra = 3

class AuthorInline(admin.TabularInline):
	model = Author
	extra = 3

class Larp2LarpSeriesInline(admin.TabularInline):
	model = Larp2LarpSeries
	extra = 3

class RunAdmin(admin.ModelAdmin):
	list_display = ('larp','startdate','get_location','convention')
	list_filter = ('location','convention','startdate','larp') 
	ordering = ('startdate',)
	search_fields = ('startdate','location','notes','larp','convention')
	date_hierarchy = 'startdate'
	inlines = (GMInline, PlayerInline, NPCInline)
	readonly_fields = ('slug',)

class LarpAdmin(admin.ModelAdmin):
	list_display = ('title','length','unit','spoilerability',)
	list_filter = ('spoilerability','length','unit',) 
	inlines = (AuthorInline,)
#	prepopulated_fields = {"slug": ("title",)}
	readonly_fields =  ("slug",)

class LocationAdmin(admin.ModelAdmin):
	pass

class LarpSeriesAdmin(admin.ModelAdmin):
	list_display = ('name','type')
	inlines = (Larp2LarpSeriesInline,)

class UserProfileAdmin(admin.ModelAdmin):
#	inlines = (AuthorInline, GMInline, NPCInline, PlayerInline)
	pass
	
#class RoleAdmin(admin.ModelAdmin):
#	pass
	
class CharacterAdmin(admin.ModelAdmin):
	list_display = ('name','larp')
	list_filter = ('spoiler','larp',) 
	pass

admin.site.register(LarpSeries, LarpSeriesAdmin)

admin.site.register(Convention, ConventionAdmin)

admin.site.register(Run, RunAdmin)

admin.site.register(Larp, LarpAdmin)

#admin.site.register(Role, RoleAdmin)

admin.site.register(Character, CharacterAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
