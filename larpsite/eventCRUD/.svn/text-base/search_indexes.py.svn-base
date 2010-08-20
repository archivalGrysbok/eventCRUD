import datetime
from haystack.indexes import *
from haystack import site
from eventCRUD.models import Run, Larp, LarpSeries, Convention

class RunIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
#	convention = CharField(model_attr="convention", faceted=True)
	def get_queryset(self):
		"""Used when the entire index for model is updated."""
		return Run.objects.all()

class LarpIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	def get_queryset(self):
		"""Used when the entire index for model is updated."""
		return Larp.objects.all()

class ConventionIndex(SearchIndex):
	text = CharField(document=True, use_template=True)

	def get_queryset(self):
		"""Used when the entire index for model is updated."""
		return Convention.objects.all()

class LarpSeriesIndex(SearchIndex):
	text = CharField(document=True, use_template=True)

	def get_queryset(self):
		"""Used when the entire index for model is updated."""
		return LarpSeries.objects.all()

site.register(Run, RunIndex)

site.register(Larp, LarpIndex)

site.register(Convention, ConventionIndex)

site.register(LarpSeries, LarpSeriesIndex)