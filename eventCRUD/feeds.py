from django.contrib.syndication.views import Feed
from models import Run

class UpcomingRunsFeed(Feed):
    title = "Upcoming Larps"
    link = "/sitenews/"
    description = "LARPs scheduled to run in the future."

    def items(self):
        return Run.objects.filter(startdate__isnull=False).filter(startdate__gt=datetime.now).order_by("startdate")

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item.larp.description

