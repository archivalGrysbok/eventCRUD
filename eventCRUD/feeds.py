from django.contrib.syndication.views import Feed
from datetime import datetime
from models import Run

class UpcomingRunsFeed(Feed):
    title = "Upcoming Larps"
    link = "/feed/"
    description = "LARPs scheduled to run in the future."
    description_template = 'feeds/beat_description.html'

    def items(self):
        return Run.objects.filter(startdate__isnull=False).filter(startdate__gt=datetime.now).order_by("startdate")

    def item_title(self, item):
        return item.larp

    def item_description(self, item):
        return item.larp.description

