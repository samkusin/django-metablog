from django.contrib.syndication.views import Feed
from django.conf import settings
from django.http import Http404
from django.utils.feedgenerator import Atom1Feed

from models import Post, Category


class PostFeed(Feed):

    def get_object(self, request, category_slug):
        if category_slug is None:
            return None
        categories = Category.objects.all()
        for category in categories:
            if category.tag.slug == category_slug:
                return category

        raise Http404

    def title(self, obj):
        if obj == None:
            return settings.CK_SITE_TITLE
        return "%s - %s" % (settings.CK_SITE_TITLE, obj.long_name)

    def description(self, obj):
        if obj == None:
            return "Articles related to gaming and software development."
        return "Articles related to %s." % obj.long_name

    def categories(self, obj):
        if obj == None:
            categories = Category.objects.all()
        else:
            categories = [obj]

        cat_strs = []
        for category in categories:
            cat_strs.append(category.long_name)

        return cat_strs

    def link(self, obj):
        if obj == None:
            return '/'
        return obj.get_absolute_url()

    def items(self, obj):
        if obj == None:
            return Post.objects.all().order_by("-post_date")[:10]
        return Post.objects.filter(tags__in=[obj.tag]).order_by("-post_date")[:10]

    title_template = 'feeds/post_item_title.html'
    description_template = 'feeds/post_item_description.html'

    def item_link(self, item):
        return item.get_absolute_url()


class AtomPostFeed(PostFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)
