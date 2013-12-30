from django.contrib.syndication.views import Feed
from django.conf import settings
from django.http import Http404
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.safestring import mark_safe 

from models import Post, Category

class ExtendedRSSFeed(Rss201rev2Feed):
    """
    RSS Feed with content encoded elements
    Adopted from:
        https://djangosnippets.org/snippets/2202/
    """
    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class PostFeed(Feed):
    feed_type = ExtendedRSSFeed

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
            return Post.objects.filter(status__gte=Post.PUBLISHED).order_by("-post_date")[:10]
        return Post.objects.filter(tags__in=[obj.tag]).exclude(status__lte=Post.DRAFT).order_by("-post_date")[:10]

    title_template = 'feeds/post_item_title.html'
    description_template = 'feeds/post_item_description.html'
    
    def item_link(self, item):
        return item.get_absolute_url()

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_pubdate(self, item):
        return item.post_date

    def item_content_encoded(self, item):
        return item.text



class AtomPostFeed(PostFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)
