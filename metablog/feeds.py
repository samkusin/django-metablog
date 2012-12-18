from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import text, html

from models import Post, Category


class PostFeed(Feed):

    def get_object(self, request, category_id):
        if category_id is None:
            return None 
        return get_object_or_404(Category, pk=category_id)

    def title(self, obj):
        return "%s - %s" % (settings.CK_SITE_TITLE, obj.long_name)

    def title(self):
        return "%s" % (settings.CK_SITE_TITLE)

    def description(self, obj):
        return "(Heavily editorialized) articles related to %s." % obj.long_name

    def description(self):
        return "(Heavily editorialized) articles related to gaming, coding, and everything in between."

    def link(self, obj):
        return obj.get_absolute_url()

    link = '/'

    def items(self, obj):
        return Post.objects.filter(tags__in=obj.tag).order_by("-post_date")[:10]

    def items(self):
        return Post.objects.all().order_by("-post_date")[:10]

    title_template = 'feeds/post_item_title.html'
    description_template = 'feeds/post_item_description.html'

    def item_link(self, item):
        return item.get_absolute_url()
